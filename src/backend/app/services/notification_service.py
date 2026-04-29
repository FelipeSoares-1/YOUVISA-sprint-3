from __future__ import annotations
import uuid
import logging
import json
from datetime import datetime, timezone

from app.database import notification_repo

logger = logging.getLogger("youvisa.notifications")

CHANNEL_RULES: dict[str, list[str]] = {
    "None_TO_RECEBIDO":             ["email"],
    "RECEBIDO_TO_EM_ANALISE":       ["email", "sms"],
    "EM_ANALISE_TO_PENDENTE_DOCS":  ["email", "sms"],
    "EM_ANALISE_TO_APROVADO":       ["email", "sms"],
    "EM_ANALISE_TO_REPROVADO":      ["email", "sms"],
    "APROVADO_TO_FINALIZADO":       ["email", "sms"],
    "PENDENTE_DOCS_TO_RECEBIDO":    ["email"],
}

EMAIL_SUBJECTS: dict[str, str] = {
    "None_TO_RECEBIDO":             "YOUVISA — Documento Recebido com Sucesso",
    "RECEBIDO_TO_EM_ANALISE":       "YOUVISA — Análise Técnica Iniciada",
    "EM_ANALISE_TO_PENDENTE_DOCS":  "YOUVISA — Ação Necessária: Pendência Documental",
    "EM_ANALISE_TO_APROVADO":       "YOUVISA — Parabéns! Documentação Aprovada",
    "EM_ANALISE_TO_REPROVADO":      "YOUVISA — Documentação Reprovada",
    "APROVADO_TO_FINALIZADO":       "YOUVISA — Processo Concluído com Sucesso",
    "PENDENTE_DOCS_TO_RECEBIDO":    "YOUVISA — Documento Reenviado",
}

SMS_TEMPLATES: dict[str, str] = {
    "RECEBIDO_TO_EM_ANALISE":       "YOUVISA: Seu documento entrou em análise técnica. Acompanhe: app.youvisa.com",
    "EM_ANALISE_TO_PENDENTE_DOCS":  "YOUVISA: Pendência detectada. Acesse o painel para reenviar.",
    "EM_ANALISE_TO_APROVADO":       "YOUVISA: Documentação APROVADA! Acesse o painel.",
    "EM_ANALISE_TO_REPROVADO":      "YOUVISA: Documentação reprovada. Contate o suporte.",
    "APROVADO_TO_FINALIZADO":       "YOUVISA: Processo CONCLUÍDO! Obrigado por usar a YOUVISA.",
}


class NotificationService:
    def notify(self, recipient: str, event_type: str, message: str, doc_id: str = None) -> list[dict]:
        channels = CHANNEL_RULES.get(event_type, ["email"])
        results = []

        for channel in channels:
            notif = (
                self._build_email(recipient, event_type, message, doc_id)
                if channel == "email"
                else self._build_sms(recipient, event_type, message, doc_id)
            )
            try:
                notification_repo.save(notif)
            except Exception as exc:
                logger.error("Failed to persist notification: %s", exc)

            icon = "📧" if channel == "email" else "📱"
            logger.info(
                "[NOTIFICATION:%s] %s",
                channel.upper(),
                json.dumps(notif, ensure_ascii=False)
            )
            print(f"{icon} [{channel.upper()}] {notif.get('recipient')} | {notif.get('subject') or notif.get('body','')[:50]}")
            results.append(notif)

        return results

    def _build_email(self, recipient: str, event_type: str, message: str, doc_id: str | None) -> dict:
        return {
            "id": str(uuid.uuid4()),
            "channel": "email",
            "recipient": recipient,
            "sender": "noreply@youvisa.com.br",
            "subject": EMAIL_SUBJECTS.get(event_type, "YOUVISA — Atualização do Processo"),
            "body": message,
            "event_type": event_type,
            "doc_id": doc_id or "",
            "sent_at": datetime.now(timezone.utc).isoformat(),
            "delivered": True,
            "provider": "SMTP (Simulado)",
        }

    def _build_sms(self, recipient: str, event_type: str, message: str, doc_id: str | None) -> dict:
        return {
            "id": str(uuid.uuid4()),
            "channel": "sms",
            "recipient": "+55 11 9****-7890",
            "sender": "YOUVISA",
            "subject": None,
            "body": SMS_TEMPLATES.get(event_type, f"YOUVISA: {message[:120]}"),
            "event_type": event_type,
            "doc_id": doc_id or "",
            "sent_at": datetime.now(timezone.utc).isoformat(),
            "delivered": True,
            "provider": "Twilio (Simulado)",
        }

    def get_all(self) -> list[dict]:
        return notification_repo.list_all()

    def get_by_doc(self, doc_id: str) -> list[dict]:
        return notification_repo.list_by_doc(doc_id)


notification_service = NotificationService()
