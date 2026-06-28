import chromadb
import uuid 
from sentence_transformers import SentenceTransformer
from pathlib import Path
from typing import List,Any 

EMBED_MODEL = "all-MiniLM-L6-v2"
VECTOR_STORE_PATH = "data/vector_store"
COLLECTION_NAME = "asha_documents"

class RAGVectorStore : 
    def __init__(self):
        self.model = SentenceTransformer(EMBED_MODEL)
        print(f"Loaded Embedding Model : {EMBED_MODEL}")

        Path(VECTOR_STORE_PATH).mkdir(parents=True,exist_ok=True)
        self.client = chromadb.PersistentClient(path=VECTOR_STORE_PATH)
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"description" : "ASHA health documents"}
        )
        print(f"Vector Store ready. Documents in collection : {self.collection.count()}")

    def is_empty(self):
        return self.collection.count() == 0 
    
    def add_documents(self,chunks : List[Any]):
        texts = [c.page_content for c in chunks]
        print(f"Generating embeddings for {len(texts)} chunks...")

        embeddings = self.model.encode(texts,show_progress_bar=True)

        ids,metadatas,documents_txt,embeddings_list = [],[],[],[]

        for i,(chunk,embedding) in enumerate(zip(chunks,embeddings)):
            ids.append(f"doc_{uuid.uuid4().hex[:8]}_{i}")
            metadata = dict(chunk.metadata)
            metadata["content_length"] = len(chunk.page_content)
            metadatas.append(metadata)
            documents_txt.append(chunk.page_content)
            embeddings_list.append(embedding.tolist())
        
        self.collection.add(
            ids = ids,
            embeddings= embeddings_list,
            metadatas=metadatas,
            documents = documents_txt
        )
        print(f"✅ Added {len(chunks)} chunks to vector store")
    
    def query(self,query_text:str,top_k:int=5):
        query_embedding = self.model.encode([query_text])[0]

        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k
        )

        docs = []

        if results["documents"] and results["documents"][0]:
            for doc,metadata,distance in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0]
            ):
                docs.append({
                    "content":doc,
                    "source_file":metadata.get("source_file","Unknown"),
                    "page" : metadata.get("page","?"),
                    "score" : round(1-distance,3)
                })

            return docs