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
        file_id = str(uuid.uuid4())
        file_path = f"{UPLOAD_DIR}/{file_id}_{file.filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 1. Initialize Workflow (status = RECEBIDO)
        process = workflow_service.create_process(file_id, file.filename)

        # 2. Computer Vision Validation + Field Extraction
        cv_result = cv_service.validate_document_image(file_path)

        # 3. AI Document Classification
        ai_result = ai_service.analyze_document(
            f"Filename: {file.filename}. CV Fields: {cv_result.get('extracted_fields', {})}"
        )

        # 4. Auto-transition to EM_ANALISE
        workflow_service.transition(
            file_id,
            WorkflowEvent.START_ANALYSIS,
            "Upload e validação inicial concluídos. Iniciando análise técnica."
        )

        return {
            "id": file_id,
            "filename": file.filename,
            "process": workflow_service.get_process(file_id),
            "cv_validation": cv_result,
            "ai_classification": ai_result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{doc_id}/transition")
async def transition_state(doc_id: str, event: str, reason: str = None):
    try:
        new_state = workflow_service.transition(doc_id, event, reason)
        return new_state
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/")
async def list_documents():
    """Returns all processes with their doc_id included."""
    return workflow_service.list_all()


@router.get("/{doc_id}")
async def get_document(doc_id: str):
    process = workflow_service.get_process(doc_id)
    if not process:
        raise HTTPException(status_code=404, detail="Processo não encontrado.")
    return process


@router.get("/{doc_id}/history")
async def get_document_history(doc_id: str):
    """Returns the full audit trail for a specific process."""
    history = workflow_service.get_history(doc_id)
    if not history:
        raise HTTPException(status_code=404, detail="Histórico não encontrado.")
    return history
