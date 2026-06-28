from langchain_groq import ChatGroq
from rag.vectorstore import RAGVectorStore
from dotenv import load_dotenv
load_dotenv()
import os 

class RAGRetriever : 
    def __init__(self,vector_store:RAGVectorStore):
        self.vector_store = vector_store
        self.llm = ChatGroq(
            api_key = os.getenv("GROQ_API_KEY"),
            model="llama-3.3-70b-versatile",
            temperature=0.1,
            max_tokens=1024
        )
    
    def answer(self,query:str,top_k:int=5):
        results = self.vector_store.query(query,top_k=top_k)

        if not results : 
            return {
                "answer" : "I couldn't find relevant information in the documents.",
                "sources" : []
            }
        
        context = "\n\n".join([r["content"]for r in results])
        sources = list(set([r["source_file"] for r in results]))

        prompt = f"""You are a helpful assistant for ASHA (Accredited Social Health Activist) workers in India.
                    Use the following context from official health documents to answer the question clearly and concisely.
                    If the context doesn't contain enough information, say so honestly.

                    Context:
                    {context}

                    Question: {query}

                    Answer:
                    """

        response = self.llm.invoke(prompt)
        return {
            "answer" : response.content,
            "sources" : sources
        }