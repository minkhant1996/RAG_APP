from vector_store import VectorStore
from typing import Optional
from config import Config

config = Config()
class Retriever:
    def __init__(self, 
                 embed_method: str = "openai",
                 embed_model_name: str = "text-embedding-3-small",
                 vector_store_local_path: str = None, 
                 vectors_store_type: str = "faiss", 
                 retrieve_type: Optional[str] = None  # similarity_score_threshold, mmr
                 ):
        assert vector_store_local_path is not None, "Error in Retriever class: Vector Store Local Path is required"
                
        self.retrieve_type = retrieve_type
        embedding = VectorStore.get_embedding(embed_method, embed_model_name)
        self.vector_store = VectorStore.load_vector_store_local(embedding, vector_store_local_path, vectors_store_type)
        
    
    def similiarity_search(self, query):
        try:
            docs = self.vector_store.similarity_search(query, k = 5)
            return self.make_text_from_docs(docs)
        except Exception as e:
            raise Exception(f"Error in similiarity_search: {str(e)}")
        
    def get_retriever(self):
        try:
            if self.retrieve_type == "mmr":
                search_kwargs = {"k": 10, "fetch_k": 20, "lambda_mult": 0.5}
            elif self.retrieve_type == "similarity_score_threshold":
                search_kwargs={"k": 10,"score_threshold": 0.5}
            elif self.retrieve_type == "similarity":
                search_kwargs={"k": 10}
            else:
                raise NotImplementedError("Retrieval type not implemented")
            return self.vector_store.as_retriever(
                                    search_type=self.retrieve_type,
                                    search_kwargs=search_kwargs,
                                )
        except Exception as e:
            raise Exception(f"Error in get_retriever: {str(e)}")

    def retrieve(self, user_query):
        try:
            if self.retrieve_type:
                retriever = self.get_retriever()
                
            docs = retriever.invoke(user_query)
            return self.make_text_from_docs(docs)
        except Exception as e:
            raise Exception(f"Error in retrieve: {str(e)}")
        
    def make_text_from_docs(self, docs):
        try:
            extracted_knowledge = ""
            for doc in docs:
                extracted_knowledge += doc.page_content + "\n"
                
            return extracted_knowledge
        except Exception as e:
            raise Exception(f"Error in make_text_from_docs: {str(e)}")