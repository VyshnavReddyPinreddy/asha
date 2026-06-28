from rag.loader import load_all_documents,split_documents
from rag.vectorstore import RAGVectorStore 
print("=== Building ASHA RAG Index ===\n")

docs = load_all_documents()
chunks = split_documents(docs)

store = RAGVectorStore()

if not store.is_empty() : 
    print(f"Vector store already has {store.collection.count()} chunks. Skipping.")
    print("Delete data/vector_store/ and re-run to rebuild.")
else : 
    store.add_documents(chunks)

print("\n✅ Index built successfully!")
