from pydantic import BaseModel
from fastapi import FastAPI, APIRouter, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
import os
from config import Config

config = Config()

app = FastAPI()
router = APIRouter()

# Directory to save uploaded files
UPLOAD_DIR = "uploaded_pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def initialize_user_data(userId, pdf_filename):
    UserData = {
        "userId": userId,
        "pdf": [
                {
                    "pdf_filename": pdf_filename,
                    "pdf_title": None,
                    "image_path": []        
                }
            ],
        "chat_history": []
    }
    redis_key = f"{config.redis_config.key.prefix}{userId}{config.redis_config.key.sufix}"
    
    return UserData, redis_key

@router.post("/upload-pdf/")
async def upload_pdf(
        userId: str = Form(...),
        file: UploadFile = File(...)
        ):
    
    
    # Check if the file is a PDF
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    
    try:
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
