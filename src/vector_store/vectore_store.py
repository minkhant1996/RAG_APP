from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from datetime import datetime
import os
from config import Config

config = Config()

class VectorStore:
    @staticmethod
    def create_vector_store(documents, embedding, ids, vectors_store_type, vector_store_local_path):
        os.makedirs(os.path.dirname(vector_store_local_path), exist_ok=True)
        if vectors_store_type == "faiss":
            # if os.path.exists(f"{vector_store_local_path}/index.faiss"):
            #     vector_store = VectorStore.load_vector_store_local(embedding, vector_store_local_path, vectors_store_type)                
            # else:
            vector_store = FAISS.from_documents(documents, embedding, ids=ids)
                
            VectorStore.save_vector_store_local(vector_store, vector_store_local_path, vectors_store_type)
    
    @staticmethod
    def load_vector_store_local(embedding, vector_store_local_path, vectors_store_type):
        if vectors_store_type == "faiss":
            try:
                retvector_store = FAISS.load_local(
                            vector_store_local_path,
                            embedding, 
                            allow_dangerous_deserialization=True
                            )
                return retvector_store
            except Exception as e:
                return None
            
    @staticmethod  
    def save_vector_store_local(vector_store, vector_store_local_path, vectors_store_type):
        if vectors_store_type == "faiss":
            vector_store.save_local(vector_store_local_path)
            
            
    @staticmethod
    def get_embedding(embed_method, embed_model_name):
        if embed_method == "openai":
            return OpenAIEmbeddings(model=embed_model_name)
        else:
            raise NotImplementedError("Embedding method not implemented")