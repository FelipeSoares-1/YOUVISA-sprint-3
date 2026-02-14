from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.ai_service import ai_service
from app.services.cv_service import cv_service
from app.services.workflow_service import workflow_service, WorkflowEvent
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
            
        # 1. Initialize Workflow
        process = workflow_service.create_process(file_id, file.filename)
        
        # 2. Computer Vision Validation (Async in real world)
        cv_result = cv_service.validate_document_image(file_path)
        
        # 3. Trigger Analysis Transition
        workflow_service.transition(file_id, WorkflowEvent.START_ANALYSIS, "Upload realizado com sucesso")
        
        return {
            "id": file_id,
            "process": process,
            "cv_validation": cv_result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{doc_id}/transition")
async def transition_state(doc_id: str, event: str, reason: str = None):
    try:
        # Debug endpoint to force transitions
        new_state = workflow_service.transition(doc_id, event, reason)
        return new_state
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
async def list_documents():
    # Return all processes from memory
    return list(workflow_service._db.values())
