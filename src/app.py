from fastapi import FastAPI, APIRouter, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
import os
from redis_db import RedisDB_Manager
from data_loader import PDF_Reader
from knowledge_manager import KnowledgeManager
from config import Config
from api_models.chat_service_api import chatbot_api, langchain_eval_qa_api
from ai_agents import AI_Agents

config = Config()

app = FastAPI()
router = APIRouter()


@router.post(config.api_config.upload_pdf)
async def upload_pdf(
        userId: str = Form(...),
        file: UploadFile = File(...)
        ):
    try:

        # check if the user id is valid
        redis_key = f"{config.redis_config.key.prefix}{userId}{config.redis_config.key.sufix}"
        user_data = RedisDB_Manager.load_from_redis(redis_key)
        
        if not user_data:
            user_data = RedisDB_Manager.initialize_user_data(redis_key, userId)
        
        
        # Check if the file is a PDF
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

        reader = PDF_Reader(
            userId=userId,
            pdf_filename=file.filename,
            # pdf_path="test_pdf/pdf1.pdf",
            pdf_file = file.file,
            save_image=True,    # To check the image extraction; Later use to return the image
            save_pdf_text=True, # To check the text extraction
            summarize_image=True
        )

        extracted_info, main_title, list_titles = reader.process_pdf()
        
        pdf_titles_stored = [pdf["pdf_title"] for pdf in user_data["pdf"]]
        # if main_title not in pdf_titles_stored: # Check if the PDF is already uploaded - will implement this later
        user_data = RedisDB_Manager.add_pdf_info(redis_key, user_data, file.filename, main_title, list_titles, [])
        for text_split_method in config.rag_config.text_split_methods:
            Knowledge_Manager = KnowledgeManager(
                userId=userId,
                pdf_name=file.filename,
                embed_method=config.rag_config.embedding.embed_method,
                embed_model_name=config.rag_config.embedding.embed_model_name,
                text_split_method=text_split_method,
                vectors_store_type=config.rag_config.vectors_store_type
            )
        
        Knowledge_Manager.create_db(extracted_info)
            
        
        if config.rag_config.save_original_pdf:
            file_path = os.path.join(
                config.user_config.user_data_path,
                userId,
                "pdf",
                file.filename
            )
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            file.file.seek(0)  # Reset pointer to the beginning of the file
            with open(file_path, "wb") as f:
                content = file.file.read()  # Read the file content
                if not content.startswith(b"%PDF"):
                    raise Exception(f"Uploaded file {file.filename} is not a valid PDF.")
                f.write(content)

        
        return JSONResponse(content={"message": "File uploaded successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.post(config.api_config.chatbot)
async def chatbot_endpoint(request: chatbot_api):
    try:
        userId = request.userId
        
        redis_key = f"{config.redis_config.key.prefix}{userId}{config.redis_config.key.sufix}"
        user_data = RedisDB_Manager.load_from_redis(redis_key)
        if not user_data:
            user_data = RedisDB_Manager.initialize_user_data(redis_key, userId)
        
        
        user_query = request.user_query.strip()
        user_data = RedisDB_Manager.add_chat_history(redis_key, user_data, user_query=user_query)
        
        if not user_query:
            raise HTTPException(status_code=400, detail="User_query cannot be empty.")

        response_text = AI_Agents.chatbot_response(userId, user_query, user_data)
        user_data = RedisDB_Manager.add_chat_history(redis_key, user_data, response=response_text)

        return JSONResponse(content={"response": response_text})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get(config.api_config.clear_conversation)
async def clear_conversation(userId: str):
    try:
        redis_key = f"{config.redis_config.key.prefix}{userId}{config.redis_config.key.sufix}"
        user_data = RedisDB_Manager.load_from_redis(redis_key)
        if not user_data:
            user_data = RedisDB_Manager.initialize_user_data(redis_key, userId)
        
        
        user_data = RedisDB_Manager.clear_chat_history(redis_key, user_data)
        return JSONResponse(content={"message": "Conversation cleared successfully."})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.get(config.api_config.retrieve_conversation)
async def retrieve_conversation(userId: str):
    try:
        redis_key = f"{config.redis_config.key.prefix}{userId}{config.redis_config.key.sufix}"
        user_data = RedisDB_Manager.load_from_redis(redis_key)
        if not user_data:
            user_data = RedisDB_Manager.initialize_user_data(redis_key, userId)
        
        chat_history = user_data["chat_history"]
        return JSONResponse(content={"chat_history": chat_history})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    

@router.post(config.api_config.run_langchain_eval_qa)
async def run_langchain_eval_qa(request: langchain_eval_qa_api):
    try:
        userId = request.userId
        question_list = request.question
        answer_list = request.ref_answer
        assert len(question_list) == len(answer_list), "The number of questions and answers must be the same."
        
        redis_key = f"{config.redis_config.key.prefix}{userId}{config.redis_config.key.sufix}"
        user_data = RedisDB_Manager.load_from_redis(redis_key)
        if not user_data:
            user_data = RedisDB_Manager.initialize_user_data(redis_key, userId)
        
        if not user_data["pdf"]:
            raise HTTPException(status_code=400, detail="No PDFs uploaded yet.")
        
        response = AI_Agents.langchain_eval_qa(question_list, answer_list, user_data)
        
        return JSONResponse(content={"response": response})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# Include the router
app.include_router(router, prefix=config.api_config.prefix)


# if __name__ == "__main__":
    # import uvicorn
    # uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)