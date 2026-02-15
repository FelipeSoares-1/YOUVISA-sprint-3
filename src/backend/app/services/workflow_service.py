from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
import logging
import json
import uuid

logger = logging.getLogger("youvisa.workflow")


class ProcessStatus(str, Enum):
    RECEBIDO = "RECEBIDO"
    EM_ANALISE = "EM_ANALISE"
    PENDENTE_DOCS = "PENDENTE_DOCS"
    APROVADO = "APROVADO"
    REPROVADO = "REPROVADO"
    FINALIZADO = "FINALIZADO"


class WorkflowEvent(str, Enum):
    START_ANALYSIS = "START_ANALYSIS"
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    REQUEST_DOCS = "REQUEST_DOCS"
    RETRY_UPLOAD = "RETRY_UPLOAD"
    FINALIZE = "FINALIZE"


# Valid transitions map (deterministic FSM)
VALID_TRANSITIONS = {
    ProcessStatus.RECEBIDO: {
        WorkflowEvent.START_ANALYSIS: ProcessStatus.EM_ANALISE
    },
    ProcessStatus.EM_ANALISE: {
        WorkflowEvent.APPROVE: ProcessStatus.APROVADO,
        WorkflowEvent.REJECT: ProcessStatus.REPROVADO,
        WorkflowEvent.REQUEST_DOCS: ProcessStatus.PENDENTE_DOCS
    },
    ProcessStatus.PENDENTE_DOCS: {
        WorkflowEvent.RETRY_UPLOAD: ProcessStatus.RECEBIDO
    },
    ProcessStatus.APROVADO: {
        WorkflowEvent.FINALIZE: ProcessStatus.FINALIZADO
    }
}


class WorkflowService:
    def __init__(self):
        self._db: Dict[str, Dict] = {}
        self._audit_log: List[Dict] = []

    def create_process(self, doc_id: str, filename: str):
        now = datetime.now()
        self._db[doc_id] = {
            "id": doc_id,
            "status": ProcessStatus.RECEBIDO,
            "filename": filename,
            "history": [
                {
                    "from_status": None,
                    "to_status": ProcessStatus.RECEBIDO,
                    "event": "UPLOAD",
                    "timestamp": now.isoformat(),
                    "description": "Documento recebido via upload."
                }
            ],
            "created_at": now.isoformat(),
            "updated_at": now.isoformat()
        }

        self._log_audit(doc_id, None, ProcessStatus.RECEBIDO, "UPLOAD", "Documento recebido.")
        return self._db[doc_id]

    def get_process(self, doc_id: str):
        return self._db.get(doc_id)

    def list_all(self):
        return [{"id": k, **v} for k, v in self._db.items()]

    def transition(self, doc_id: str, event: str, reason: Optional[str] = None):
        process = self._db.get(doc_id)
        if not process:
            raise ValueError(f"Processo '{doc_id}' não encontrado.")

        current_status = process["status"]
        event_enum = WorkflowEvent(event)

        # Validate transition
        allowed = VALID_TRANSITIONS.get(current_status, {})
        next_status = allowed.get(event_enum)

        if not next_status:
            raise ValueError(
                f"Transição inválida: {current_status} --({event})--> ???. "
                f"Transições válidas de '{current_status}': {list(allowed.keys())}"
            )

        now = datetime.now()
        description = reason or f"Transição automática de {current_status} para {next_status}."

        # Apply transition
        process["status"] = next_status
        process["updated_at"] = now.isoformat()
        process["history"].append({
            "from_status": current_status,
            "to_status": next_status,
            "event": event,
            "timestamp": now.isoformat(),
            "description": description
        })

        # Audit log (structured JSON)
        self._log_audit(doc_id, current_status, next_status, event, description)

        # Trigger notification (event-driven hook)
        self._notify_user(doc_id, current_status, next_status, description)

        return process

    def get_history(self, doc_id: str):
        process = self._db.get(doc_id)
        if not process:
            return []
        return process.get("history", [])

    def get_audit_log(self):
        return self._audit_log

    def _log_audit(self, doc_id, from_status, to_status, event, description):
        entry = {
            "doc_id": doc_id,
            "from_status": str(from_status) if from_status else None,
            "to_status": str(to_status),
            "event": event,
            "description": description,
            "timestamp": datetime.now().isoformat()
        }
        self._audit_log.append(entry)
        logger.info(f"[AUDIT] {json.dumps(entry, ensure_ascii=False)}")

    def _notify_user(self, doc_id, from_status, to_status, message):
        from app.services.notification_service import notification_service

        status_messages = {
            ProcessStatus.EM_ANALISE: "Seu documento está sendo analisado pela equipe técnica.",
            ProcessStatus.PENDENTE_DOCS: "Detectamos uma pendência na sua documentação. Reenvie o documento.",
            ProcessStatus.APROVADO: "Parabéns! Sua documentação foi aprovada.",
            ProcessStatus.REPROVADO: "Infelizmente, sua documentação foi reprovada. Contate o suporte.",
            ProcessStatus.FINALIZADO: "Seu processo foi finalizado com sucesso!",
        }

        notification_msg = status_messages.get(to_status, message)
        notification_service.notify(
            recipient="user@youvisa.com",
            event_type=f"{from_status.value if from_status else 'None'}_TO_{to_status.value}",
            message=notification_msg,
            doc_id=doc_id
        )


workflow_service = WorkflowService()
