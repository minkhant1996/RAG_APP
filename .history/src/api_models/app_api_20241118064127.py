from pydantic import BaseModel
from fastapi import FastAPI, APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os

app = FastAPI()
router = APIRouter()

# Directory to save uploaded files
UPLOAD_DIR = "uploaded_pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    # Check if a file is provided
    if not file:
        raise HTTPException(status_code=400, detail="No file was uploaded.")

    # Check if the file is a PDF
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail=f"Invalid file type: {file.content_type}. Only PDF files are allowed.")

    try:
        # Ensure the file has a name
        if not file.filename:
            raise HTTPException(status_code=400, detail="File must have a valid name.")

        # Save the uploaded PDF
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        # Check for potential directory traversal attack
        if not os.path.abspath(file_path).startswith(os.path.abspath(UPLOAD_DIR)):
            raise HTTPException(status_code=400, detail="Invalid file path detected.")

        # Write the file to the specified location
        with open(file_path, "wb") as f:
            f.write(await file.read())

        return JSONResponse(content={"message": "File uploaded successfully", "file_path": file_path})
    except PermissionError:
        raise HTTPException(status_code=500, detail="Permission error: Unable to write the file to the upload directory.")
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="File not found error: Upload directory may be missing or inaccessible.")
    except IsADirectoryError:
        raise HTTPException(status_code=500, detail="Invalid file path: Attempted to write to a directory instead of a file.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


# Create the FastAPI application
app = FastAPI()

# Include the router
app.include_router(router, prefix="/api/v1")
