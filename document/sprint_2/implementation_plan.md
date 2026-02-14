# Plano de Implementação - Sprint 2: Plataforma Multicanal Inteligente

Este plano descreve o desenvolvimento da "Plataforma Inteligente Multicanal" (Sprint 2), criando um protótipo funcional com Backend (Python/FastAPI) e Frontend (React/Vite).

## Necessária Revisão do Usuário

> [!IMPORTANT]
> **Chaves de API**: O sistema requer Chaves de API para IA Generativa (ex: OpenAI) e SMTP (Email).
> *Estratégia*: capaz de rodar em **Modo Mock (Simulado)** se as chaves estiverem faltando no `.env`, garantindo que o professor possa testar sem configuração complexa.

> [!NOTE]
> **Seleção da Stack Tecnológica**:
> - **Backend**: FastAPI (Python 3.12+) - Escolhido pela velocidade, suporte assíncrono e fácil integração com bibliotecas de IA.
> - **Frontend**: React + Vite - Escolhido pela performance e DX moderna.
> - **Estilo**: CSS Puro com estética moderna "Glassmorphism" (conforme diretrizes).
> - **Banco de Dados**: Em memória ou SQLite para esta fase de protótipo (simplicidade).

## Mudanças Propostas

### Estrutura (Padrão FIAP)
Adotaremos a estrutura do template oficial:
- `/src/backend`: API Python, lógica de IA, OCR, Automação.
- `/src/frontend`: Web App React.
- `/document`: Documentação do projeto.
- `/assets`: Imagens e recursos estáticos.
- `/scripts`: Scripts de automação.

### Backend (Python/FastAPI)
#### [NOVO] `src/backend/pyproject.toml`
Gerenciamento de dependências.

#### [NOVO] `src/backend/app/main.py`
Ponto de entrada.

#### [NOVO] `src/backend/app/routers/`
- `documents.py`
- `chat.py`

#### [NOVO] `src/backend/app/services/`
- `ai_service.py`
- `cv_service.py`
- `automation_service.py`

### Frontend (React + Vite)
#### [NOVO] `src/frontend/`
Estrutura React + Vite.

#### [NOVO] `src/frontend/src/components/`
- `ChatInterface.jsx`
- `Dashboard.jsx`
- `FileUpload.jsx`

#### [NOVO] `src/frontend/src/styles/`
- `index.css`
- `App.css`

## Plano de Verificação

### Testes Automatizados
- **Testes de Backend (`pytest`):**
    - `tests/test_api.py`: Verificar se endpoints retornam 200 OK.
    - `tests/test_services.py`: Verificar se mocks de IA/CV retornam estrutura esperada.
    - Comando: `pytest backend/tests`

### Verificação Manual
1. **Iniciar Backend**: `cd src/backend && uvicorn app.main:app --reload`
2. **Iniciar Frontend**: `cd src/frontend && npm run dev`
3. **Teste de Fluxo**:
    - Abrir Web App.
    - Fazer upload de uma imagem (ex: passaporte fictício).
    - Chatbot deve confirmar recebimento.
    - Console/Logs devem mostrar simulação de "Email enviado".
    - Dashboard deve atualizar status para "Recebido" -> "Analisado".
