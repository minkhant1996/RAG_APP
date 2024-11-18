from langchain_experimental.text_splitter import SemanticChunker
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from datetime import datetime
import os
from config import Config
from vector_store import VectorStore
from typing import Optional

config = Config()

class KnowledgeManager:
    def __init__(self, 
                 userId: str,
                 pdf_name: str,
                 embed_method: str = "openai",
                 embed_model_name: str = "text-embedding-3-large",
                 text_split_method: str = "semantic_chunker",
                 vectors_store_type: str = "faiss"
                ):
        
        self.userId = userId
        self.pdf_name = pdf_name
        self.text_split_method = text_split_method
        self.embed_method = embed_method
        self.embed_model_name = embed_model_name
        self.vector_store = None
        self.vectors_store_type = vectors_store_type
        
        vector_store_types = ["faiss"]
        assert self.vectors_store_type in vector_store_types, "Error in KnowledgeManager class: Vector Store Type not supported"
        
        embed_methods = ["openai"]
        assert self.embed_method in embed_methods, "Error in KnowledgeManager class: Embeddeding Method not supported"
                
        text_split_methods = ["semantic_chunker", "recursive_character"]
        assert self.text_split_method in text_split_methods, "Error in KnowledgeManager class: Text Split Method not supported"
        
    
    def create_db(self, text_document: str):
        try:
            self.embedding = VectorStore.get_embedding(self.embed_method, self.embed_model_name)
            text_splitter = self.get_text_splitter()
            documents, ids = self.create_documents(text_splitter, text_document)
            
            vector_store_local_path = os.path.join(
                                            config.user_config.user_data_path, 
                                            self.userId,
                                            self.text_split_method,
                                            "faiss_index"
                                            )
            os.makedirs(vector_store_local_path, exist_ok=True)
            VectorStore.create_vector_store(documents, self.embedding, ids, self.vectors_store_type, vector_store_local_path)
        except Exception as e:
            raise Exception(f"Error in create_db: {str(e)}")
    
    def get_text_splitter(self):
        try:
            if self.text_split_method == "semantic_chunker":
                return SemanticChunker(
                                self.embedding,
                                breakpoint_threshold_type="percentile" # "percentile", "standard_deviation" or interquartile
                                )
            elif self.text_split_method == "recursive_character":
                return RecursiveCharacterTextSplitter(
                                chunk_size=1000,
                                chunk_overlap=200,
                                length_function=len,
                                is_separator_regex=False,
                                )
            
            else:
                raise NotImplementedError("Error in get_text_splitter: Text Split Method not implemented")
        except Exception as e:
            raise Exception(f"Error in get_text_splitter: {str(e)}")
        
    
    def create_documents(self, text_splitter, text_document):
        try:
            documents = []
            ids = []
            for i, doc in enumerate(text_splitter.create_documents([text_document])):
                documents.append(Document(
                                    page_content=doc.page_content, 
                                    metadata={
                                            "pdf_name": self.pdf_name,
                                            "datetime": str(datetime.now(config.timezone))
                                            }))
                ids.append(f"{self.pdf_name}_{str(i)}")
                
                
                if config.rag_config.save_split_text:
                    file_path = os.path.join(
                                        config.user_config.user_data_path,
                                         self.userId, 
                                         self.text_split_method
                                         )
                    os.makedirs(file_path, exist_ok=True)
                    with open(f"{file_path}/{ids[-1]}.txt", "w") as f:
                        f.write(doc.page_content)
                        
            return documents, ids
        except Exception as e:
            raise Exception(f"Error in create_documents: {str(e)}")
            


        
