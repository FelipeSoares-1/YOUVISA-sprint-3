from __future__ import annotations
import logging
from enum import Enum
from typing import Optional

from app.database import process_repo

logger = logging.getLogger("youvisa.workflow")


class ProcessStatus(str, Enum):
    RECEBIDO      = "RECEBIDO"
    EM_ANALISE    = "EM_ANALISE"
    PENDENTE_DOCS = "PENDENTE_DOCS"
    APROVADO      = "APROVADO"
    REPROVADO     = "REPROVADO"
    FINALIZADO    = "FINALIZADO"


class WorkflowEvent(str, Enum):
    START_ANALYSIS = "START_ANALYSIS"
    APPROVE        = "APPROVE"
    REJECT         = "REJECT"
    REQUEST_DOCS   = "REQUEST_DOCS"
    RETRY_UPLOAD   = "RETRY_UPLOAD"
    FINALIZE       = "FINALIZE"


VALID_TRANSITIONS: dict[ProcessStatus, dict[WorkflowEvent, ProcessStatus]] = {
    ProcessStatus.RECEBIDO: {
        WorkflowEvent.START_ANALYSIS: ProcessStatus.EM_ANALISE,
    },
    ProcessStatus.EM_ANALISE: {
        WorkflowEvent.APPROVE:       ProcessStatus.APROVADO,
        WorkflowEvent.REJECT:        ProcessStatus.REPROVADO,
        WorkflowEvent.REQUEST_DOCS:  ProcessStatus.PENDENTE_DOCS,
    },
    ProcessStatus.PENDENTE_DOCS: {
        WorkflowEvent.RETRY_UPLOAD:  ProcessStatus.RECEBIDO,
    },
    ProcessStatus.APROVADO: {
        WorkflowEvent.FINALIZE:      ProcessStatus.FINALIZADO,
    },
}

_STATUS_MESSAGES = {
    ProcessStatus.EM_ANALISE:    "Seu documento está sendo analisado pela equipe técnica.",
    ProcessStatus.PENDENTE_DOCS: "Detectamos uma pendência na sua documentação. Reenvie o documento.",
    ProcessStatus.APROVADO:      "Parabéns! Sua documentação foi aprovada.",
    ProcessStatus.REPROVADO:     "Infelizmente, sua documentação foi reprovada. Contate o suporte.",
    ProcessStatus.FINALIZADO:    "Seu processo foi finalizado com sucesso!",
}


class WorkflowService:
    def create_process(self, doc_id: str, filename: str) -> dict:
        process = process_repo.create(doc_id, filename)
        logger.info("[AUDIT] process_created doc_id=%s filename=%s", doc_id, filename)
        return process

    def get_process(self, doc_id: str) -> dict | None:
        return process_repo.get(doc_id)

    def list_all(self) -> list[dict]:
        rows = process_repo.list_all()
        # Normalize: add 'id' key for backwards-compat with existing router code
        for r in rows:
            r.setdefault("id", r["doc_id"])
        return rows

    def transition(self, doc_id: str, event: str, reason: Optional[str] = None) -> dict:
        process = process_repo.get(doc_id)
        if not process:
            raise ValueError(f"Processo '{doc_id}' não encontrado.")

        current_status = ProcessStatus(process["status"])
        event_enum = WorkflowEvent(event)
        allowed = VALID_TRANSITIONS.get(current_status, {})
        next_status = allowed.get(event_enum)

        if not next_status:
            raise ValueError(
                f"Transição inválida: {current_status} --({event})--> ???. "
                f"Válidas de '{current_status}': {[e.value for e in allowed]}"
            )

        description = reason or f"Transição de {current_status.value} para {next_status.value}."
        updated = process_repo.update_status(doc_id, next_status.value, current_status.value, description)

        logger.info(
            "[AUDIT] transition doc_id=%s %s->%s event=%s",
            doc_id, current_status.value, next_status.value, event
        )

        self._notify_user(doc_id, current_status, next_status, description)
        return updated

    def get_history(self, doc_id: str) -> list:
        process = process_repo.get(doc_id)
        return process.get("history", []) if process else []

    def _notify_user(self, doc_id, from_status, to_status, message):
        from app.services.notification_service import notification_service
        notification_service.notify(
            recipient="user@youvisa.com",
            event_type=f"{from_status.value}_TO_{to_status.value}",
            message=_STATUS_MESSAGES.get(to_status, message),
            doc_id=doc_id,
        )


workflow_service = WorkflowService()
