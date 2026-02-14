# Walkthrough - YOUVISA Sprint 2

## Visão Geral
Concluímos a implementação da **Sprint 2**, entregando uma plataforma funcional com Backend Python e Frontend React.

### Componentes Implementados

#### 1. Backend (FastAPI)
- **API Rest**: Endpoints `/api/chat` e `/api/documents/upload`.
- **IA Service**: Classifica documentos e responde no chat. (Modo Mock ativo por padrão para facilitar testes).
- **CV Service**: Simula validação de visão computacional.
- **Automation Service**: Simula envio de e-mail SMTP.

#### 2. Frontend (React)
- **Chat Interface**: Comunicação em tempo real com o bot.
- **Dashboard**: Visualização Kanban/Lista dos documentos processados.
- **Upload**: Área de drag-and-drop integrada.

## Como Testar

1. **Abra o Frontend**: Acesse o link fornecido no terminal (ex: `http://localhost:5173`).
2. **Dashboard**:
   - Arraste uma imagem qualquer para a área de upload.
   - Veja o status mudar para "Processado".
   - Verifique a "Confiança IA" e o status de "Email Enviado".
3. **Chat**:
   - Clique em "Atendimento Inteligente".
   - Digite "Olá" ou "Quero enviar um documento".
   - O bot responderá de acordo com o contexto.

## Demonstração de Código
### Endpoint de Upload
```python
@router.post("/upload")
async def upload_document(file: UploadFile):
    # Validação CV + Análise IA + Automação Email
    cv_result = cv_service.validate_document_image(file_path)
    ai_result = ai_service.analyze_document(...)
    automation_service.send_confirmation_email(...)
```
