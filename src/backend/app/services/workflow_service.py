from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
import uuid

# Definição dos Estados
class ProcessStatus(str, Enum):
    RECEBIDO = "RECEBIDO"
    EM_ANALISE = "EM_ANALISE"
    PENDENTE_DOCS = "PENDENTE_DOCS"
    APROVADO = "APROVADO"
    REPROVADO = "REPROVADO"

# Eventos de Transição
class WorkflowEvent(str, Enum):
    START_ANALYSIS = "START_ANALYSIS"
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    REQUEST_DOCS = "REQUEST_DOCS"
    RETRY_UPLOAD = "RETRY_UPLOAD"

class WorkflowService:
    def __init__(self):
        # Simulating DB with in-memory dict
        # Structure: { doc_id: { "status": str, "history": [], "updated_at": datetime } }
        self._db: Dict[str, Dict] = {}

    def create_process(self, doc_id: str, filename: str):
        self._db[doc_id] = {
            "status": ProcessStatus.RECEBIDO,
            "filename": filename,
            "history": [
                {"status": ProcessStatus.RECEBIDO, "timestamp": datetime.now(), "description": "Documento recebido."}
            ],
            "updated_at": datetime.now()
        }
        return self._db[doc_id]

    def get_process(self, doc_id: str):
        return self._db.get(doc_id)

    def transition(self, doc_id: str, event: WorkflowEvent, reason: Optional[str] = None):
        process = self._db.get(doc_id)
        if not process:
            raise ValueError("Processo não encontrado.")

        current_status = process["status"]
        next_status = None
        description = reason or "Mudança de estado automática."

        # FSM Logic (Valid Transitions)
        if current_status == ProcessStatus.RECEBIDO and event == WorkflowEvent.START_ANALYSIS:
            next_status = ProcessStatus.EM_ANALISE
        
        elif current_status == ProcessStatus.EM_ANALISE:
            if event == WorkflowEvent.APPROVE:
                next_status = ProcessStatus.APROVADO
            elif event == WorkflowEvent.REJECT:
                next_status = ProcessStatus.REPROVADO
            elif event == WorkflowEvent.REQUEST_DOCS:
                next_status = ProcessStatus.PENDENTE_DOCS
        
        elif current_status == ProcessStatus.PENDENTE_DOCS and event == WorkflowEvent.RETRY_UPLOAD:
            next_status = ProcessStatus.RECEBIDO

        # Apply Transition
        if next_status:
            process["status"] = next_status
            process["updated_at"] = datetime.now()
            process["history"].append({
                "status": next_status,
                "timestamp": datetime.now(),
                "description": description
            })
            
            # TRIGGER NOTIFICATION (Hook)
            self._notify_user(doc_id, next_status, description)
            
            return process
        else:
            raise ValueError(f"Transição inválida de {current_status} via {event}")

    def _notify_user(self, doc_id: str, status: str, message: str):
        from app.services.notification_service import notification_service
        # In a real app, we would fetch the user's email associated with doc_id
        notification_service.notify("user@example.com", status, message)

workflow_service = WorkflowService()
