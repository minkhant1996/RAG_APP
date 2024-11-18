# from data_loader import PDF_Reader
# from redis_db import RedisDB_Manager
# from datetime import datetime
# import pytz
# from knowledge_manager import KnowledgeManager
# from retriever import Retriever
# from config import Config

# config = Config()

# userId = "u12345"
# RedisPrefix = "MinKhant_"
# RedisSuffix = "_RAG"
# pdf_filename = "pdf1"
# user_query = "Hi, I am Min"

# UserData = {
#     "userId": userId,
#     "pdf": [
#             {
#                 "pdf_filename": pdf_filename,
#                 "pdf_title": None,
#                 "image_path": []        
#             }
#         ],
#     "chat_history": [
#         {
#             "query": user_query,
#             "response": None,
#             "timestamp":
#                 {
#                     "query": datetime.now(config.timezone).strftime("%Y-%m-%d %H:%M:%S"),
#                     "response": None
#                 },
#             "input_tokens": None,
#             "output_tokens": None,
#         }    
#     ],
# }
# redis_key = f"{RedisPrefix}{userId}{RedisSuffix}"
# RedisDB_Manager.save_to_redis(redis_key, UserData)


# user_data = RedisDB_Manager.load_from_redis(redis_key)
# print(user_data)

# user_data["chat_history"][-1]["response"] = "New response"
# user_data["chat_history"][-1]["timestamp"]["response"] = datetime.now(config.timezone).strftime("%Y-%m-%d %H:%M:%S")
# RedisDB_Manager.save_to_redis(redis_key, user_data)

# user_data = RedisDB_Manager.load_from_redis(redis_key)
# print(user_data)

# reader = PDF_Reader(
#     userId=userId,
#     pdf_filename=pdf_filename,
#     pdf_path="test_pdf/pdf1.pdf",
#     save_image=True,
#     save_pdf_text=True,
#     summarize_image=False
# )

# text, main_title, tiles = reader.process_pdf()

# userId = "u123452"
# pdf_filename = "Chang and Fosler-Lussier - 2023 - How to Prompt LLMs for Text-to-SQL A Study in Zer.pdf"

# with open(f"tmp/{userId}/{pdf_filename}.txt", "r") as f:
#     text = f.read()
    

# text_split_methods = ["semantic_chunker"]


# for text_split_method in text_split_methods:
#     Knowledge_Manager = KnowledgeManager(
#         userId=userId,
#         pdf_name=pdf_filename,
#         embed_method="openai",
#         embed_model_name="text-embedding-3-small",
#         text_split_method=text_split_method,
#         vectors_store_type="faiss"
#     )
    
#     Knowledge_Manager.create_db(text)
# # text_split_methods = ["semantic_chunker"]
# retrieve_type = "similarity"
# for text_split_method in text_split_methods:
    
#     user_query = "How does prompt construction impact the performance of LLMs?"
#     retriever = Retriever(
#         vector_store_local_path=f"tmp/{userId}/{text_split_method}/faiss_index",
#         vectors_store_type="faiss",
#         retrieve_type=retrieve_type
#     )
#     extracted_knowledge = retriever.retrieve(user_query)
#     print(extracted_knowledge)
    # extracted_knowledge = retriever.similiarity_search(user_query)

    # print(extracted_knowledge)
    # with open(f"tmp/{userId}/{text_split_method}/{retrieve_type}_extracted_knowledge.txt", "w") as f:
    #     f.write(extracted_knowledge)


# Command to run in terminal if tessdata error occur
# echo $TESSDATA_PREFIX
# ls $TESSDATA_PREFIX
# find / -name "eng.traineddata"

from pytesseract import image_to_string
from PIL import Image

text = image_to_string(
    Image.open("/rag_volume/test.png"),
    lang="eng",
    config="--tessdata-dir /usr/share/tesseract-ocr/4.00/tessdata"
)
print(text)
