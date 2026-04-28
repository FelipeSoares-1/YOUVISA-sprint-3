import os
import uuid
import shutil
import logging

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.ai_service import ai_service
from app.services.cv_service import cv_service
from app.services.workflow_service import workflow_service, WorkflowEvent
from app.database import process_repo

logger = logging.getLogger("youvisa.documents")
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

        # 1. Initialise workflow (status = RECEBIDO, persisted in SQLite)
        workflow_service.create_process(file_id, file.filename)

        # 2. Computer Vision validation + field extraction
        cv_result = cv_service.validate_document_image(file_path)
        process_repo.update_cv_result(file_id, cv_result)

        # 3. AI document classification
        ai_result = ai_service.analyze_document(
            f"Filename: {file.filename}. CV Fields: {cv_result.get('extracted_fields', {})}"
        )
        process_repo.update_ai_result(file_id, ai_result)

        # 4. Auto-transition to EM_ANALISE
        workflow_service.transition(
            file_id,
            WorkflowEvent.START_ANALYSIS,
            "Upload e validação inicial concluídos. Iniciando análise técnica.",
        )

        process = workflow_service.get_process(file_id)
        return {
            "id": file_id,
            "filename": file.filename,
            "process": process,
            "cv_validation": cv_result,
            "ai_classification": ai_result,
        }
    except Exception as exc:
        logger.exception("Upload error: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/{doc_id}/transition")
async def transition_state(doc_id: str, event: str, reason: str = None):
    try:
        return workflow_service.transition(doc_id, event, reason)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/")
async def list_documents():
    return workflow_service.list_all()


@router.get("/{doc_id}")
async def get_document(doc_id: str):
    process = workflow_service.get_process(doc_id)
    if not process:
        raise HTTPException(status_code=404, detail="Processo não encontrado.")
    return process


@router.get("/{doc_id}/history")
async def get_document_history(doc_id: str):
    history = workflow_service.get_history(doc_id)
    if not history:
        raise HTTPException(status_code=404, detail="Histórico não encontrado.")
    return history
