from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.ai_service import ai_service
from app.services.cv_service import cv_service
from app.services.automation_service import automation_service
import shutil
import os
import uuid

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        # Save file
        file_id = str(uuid.uuid4())
        file_path = f"{UPLOAD_DIR}/{file_id}_{file.filename}"
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # 1. Computer Vision Validation
        cv_result = cv_service.validate_document_image(file_path)
        
        # 2. AI Analysis (Simulating text extraction for now)
        ai_result = ai_service.analyze_document(f"Content of {file.filename}")
        
        # 3. Trigger Automation (Email)
        email_status = automation_service.send_confirmation_email("user@example.com", file.filename)
        
        return {
            "id": file_id,
            "filename": file.filename,
            "status": "Processed",
            "cv_validation": cv_result,
            "ai_analysis": ai_result,
            "automation": email_status
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def list_documents():
    # In a real app, query database
    return [{"id": "1", "filename": "passport_mock.jpg", "status": "Processed"}]
