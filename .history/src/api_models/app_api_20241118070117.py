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



@router.post("/upload-pdf/")
async def upload_pdf(
        userId: str = Form(...),
        file: UploadFile = File(...)
        ):
    
    # check if the user id is valid
    redis_key = f"{config.redis_config.key.prefix}{userId}{config.redis_config.key.sufix}"
    if RedisDB_Manager.load_from_redis(redis_key):
        RedisDB_Manager.initialize_user_data(redis_key, userId)
    
    
    # Check if the file is a PDF
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    
    try:
        UserData, redis_key = initialize_user_data(userId, file.filename)
        RedisDB_Manager.save_to_redis(redis_key, UserData)
        reader = PDF_Reader(
            userId=userId,
            pdf_filename=file.filename,
            pdf_path="test_pdf/pdf1.pdf",
            save_image=True,
            save_pdf_text=True,
            summarize_image=False
        )

        extracted_info, list_titles = reader.process_pdf()

        # Save the uploaded PDF
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        
        # with open(file_path, "wb") as f:
        #     f.write(file.file.read())
        
        return JSONResponse(content={"message": "File uploaded successfully", "file_path": file_path})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# Create the FastAPI application
app = FastAPI()

# Include the router
app.include_router(router, prefix="/api/v1")
