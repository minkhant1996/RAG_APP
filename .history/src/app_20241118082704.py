from fastapi import FastAPI, APIRouter, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
import os
from redis_db import RedisDB_Manager
from data_loader import PDF_Reader
from config import Config

config = Config()

app = FastAPI()
router = APIRouter()

# Directory to save uploaded files
UPLOAD_DIR = "uploaded_pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)


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
            pdf_path="test_pdf/pdf1.pdf",
            save_image=True,
            save_pdf_text=True,
            summarize_image=False
        )

        extracted_info, main_title, list_titles = reader.process_pdf()
        
        user_data = RedisDB_Manager.add_pdf_info(redis_key, user_data, file.filename, main_title, list_titles, [])
        if main_tile == user_data["pdf"][-1]["pdf_title"]:
            user_data["pdf"][-1]["pdf_title"] = main_title
        else:
            user_data = RedisDB_Manager.add_pdf_info(redis_key, user_data, file.filename, main_title, list_titles, [])
        # Save the uploaded PDF
        # file_path = os.path.join(UPLOAD_DIR, file.filename)
        
        # with open(file_path, "wb") as f:
        #     f.write(file.file.read())
        
        return JSONResponse(content={"message": "File uploaded successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# Create the FastAPI application
app = FastAPI()

# Include the router
app.include_router(router, prefix=config.api_config.prefix)
