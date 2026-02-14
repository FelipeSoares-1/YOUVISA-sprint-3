class AutomationService:
    def send_confirmation_email(self, to_email: str, doc_name: str):
        """
        Simulates sending an email via SMTP.
        """
        print(f"[SMTP MOCK] Sending email to {to_email} about {doc_name}")
        return {
            "sent": True,
            "recipient": to_email,
            "subject": f"Recebemos seu documento: {doc_name}",
            "body": "Seu documento foi recebido e está sendo analisado pela nossa IA."
        }

automation_service = AutomationService()
