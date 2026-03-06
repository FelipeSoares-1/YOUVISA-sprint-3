import traceback
from app.services.notification_service import notification_service

try:
    notification_service.notify("test@test.com", "RECEBIDO_TO_EM_ANALISE", "Teste de mensagem")
except Exception:
    traceback.print_exc()
