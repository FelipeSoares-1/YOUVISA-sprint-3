from datetime import datetime
from typing import List, Dict
import logging
import json
import uuid

logger = logging.getLogger("youvisa.notifications")

# Channel rotation rules per event type
CHANNEL_RULES = {
    "None_TO_RECEBIDO": ["email"],
    "RECEBIDO_TO_EM_ANALISE": ["email", "sms"],
    "EM_ANALISE_TO_PENDENTE_DOCS": ["email", "sms"],
    "EM_ANALISE_TO_APROVADO": ["email", "sms"],
    "EM_ANALISE_TO_REPROVADO": ["email", "sms"],
    "APROVADO_TO_FINALIZADO": ["email", "sms"],
    "PENDENTE_DOCS_TO_RECEBIDO": ["email"],
}

# Email subjects per status
EMAIL_SUBJECTS = {
    "None_TO_RECEBIDO": "YOUVISA — Documento Recebido com Sucesso",
    "RECEBIDO_TO_EM_ANALISE": "YOUVISA — Análise Técnica Iniciada",
    "EM_ANALISE_TO_PENDENTE_DOCS": "YOUVISA — Ação Necessária: Pendência Documental",
    "EM_ANALISE_TO_APROVADO": "YOUVISA — Parabéns! Documentação Aprovada",
    "EM_ANALISE_TO_REPROVADO": "YOUVISA — Documentação Reprovada",
    "APROVADO_TO_FINALIZADO": "YOUVISA — Processo Concluído com Sucesso",
    "PENDENTE_DOCS_TO_RECEBIDO": "YOUVISA — Documento Reenviado",
}

# SMS templates (short)
SMS_TEMPLATES = {
    "RECEBIDO_TO_EM_ANALISE": "YOUVISA: Seu documento entrou em análise técnica. Acompanhe pelo painel: app.youvisa.com",
    "EM_ANALISE_TO_PENDENTE_DOCS": "YOUVISA: Pendência detectada na documentação. Acesse o painel para reenviar.",
    "EM_ANALISE_TO_APROVADO": "YOUVISA: Documentação APROVADA! Acesse o painel para os próximos passos.",
    "EM_ANALISE_TO_REPROVADO": "YOUVISA: Documentação reprovada. Acesse o painel ou contate o suporte.",
    "APROVADO_TO_FINALIZADO": "YOUVISA: Processo CONCLUÍDO com sucesso! Obrigado por usar a YOUVISA.",
}


class NotificationService:
    def __init__(self):
        self._notifications: List[Dict] = []

    def notify(self, recipient: str, event_type: str, message: str, doc_id: str = None):
        """
        Registers and simulates sending notifications via email and SMS.
        Dispatches to one or both channels based on event rules.
        """
        channels = CHANNEL_RULES.get(event_type, ["email"])
        results = []

        for channel in channels:
            if channel == "email":
                notification = self._build_email(recipient, event_type, message, doc_id)
            else:
                notification = self._build_sms(recipient, event_type, message, doc_id)

            self._notifications.append(notification)

            log_entry = json.dumps(notification, ensure_ascii=False)
            logger.info(f"[NOTIFICATION:{channel.upper()}] {log_entry}")

            icon = "📧" if channel == "email" else "📱"
            print(f"{icon} [{channel.upper()}] Para: {notification['recipient']} | {notification.get('subject', notification['message'][:50])}")

            results.append(notification)

        return results[0] if len(results) == 1 else results

    def _build_email(self, recipient: str, event_type: str, message: str, doc_id: str) -> Dict:
        subject = EMAIL_SUBJECTS.get(event_type, f"YOUVISA — Atualização do Processo")
        return {
            "id": str(uuid.uuid4())[:8],
            "channel": "email",
            "recipient": recipient,
            "sender": "noreply@youvisa.com.br",
            "subject": subject,
            "body": message,
            "event_type": event_type,
            "doc_id": doc_id,
            "sent_at": datetime.now().isoformat(),
            "delivered": True,
            "provider": "SMTP (Simulado)"
        }

    def _build_sms(self, recipient: str, event_type: str, message: str, doc_id: str) -> Dict:
        sms_text = SMS_TEMPLATES.get(event_type, f"YOUVISA: {message[:120]}")
        phone = "+55 11 9****-7890"  # Masked phone mock
        return {
            "id": str(uuid.uuid4())[:8],
            "channel": "sms",
            "recipient": phone,
            "sender": "YOUVISA",
            "subject": None,
            "body": sms_text,
            "event_type": event_type,
            "doc_id": doc_id,
            "sent_at": datetime.now().isoformat(),
            "delivered": True,
            "provider": "Twilio (Simulado)"
        }

    def get_all(self) -> List[Dict]:
        return self._notifications

    def get_by_doc(self, doc_id: str) -> List[Dict]:
        return [n for n in self._notifications if n.get("doc_id") == doc_id]


notification_service = NotificationService()
