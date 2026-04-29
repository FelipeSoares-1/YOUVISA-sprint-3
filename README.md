# YOUVISA — Sprint 4: Arquitetura Multiagente e Persistência Inteligente

> Plataforma de Acompanhamento Inteligente de Processos Consulares  
> FIAP · Enterprise Challenge · Grupo 41

## Repositório

**[https://github.com/FelipeSoares-1/YOUVISA-sprint-3](https://github.com/FelipeSoares-1/YOUVISA-sprint-3)**  
Branch principal: `main`

## Demo em Vídeo

[![Assistir no YouTube](https://img.shields.io/badge/YouTube-Demo%20Sprint%204-red?logo=youtube)](https://youtu.be/e4jnhz5muF4)

**[https://youtu.be/e4jnhz5muF4](https://youtu.be/e4jnhz5muF4)**

---

## Integrantes

| Nome | E-mail |
|------|--------|
| Caio Rodrigues Castro | caiorcastro@gmail.com |
| Felipe Soares Nascimento | consultor.casteliano@gmail.com |
| Fernando Miranda Segregio | segregio@gmail.com |
| Mario Roberto Silva de Almeida | marioalmeida1980@gmail.com |
| Wellington Nascimento de Brito | well334@hotmail.com |

**Professores:** Leonardo Ruiz Orabona (Tutor) · André Godoi Chiovato (Coordenador)

---

## O que foi entregue na Sprint 4

A Sprint 4 transformou o YOUVISA de uma plataforma reativa com estado em memória em um sistema **multiagente persistente**, capaz de interpretar intenções, extrair entidades, consultar contexto e gerar respostas controladas — tudo com rastreabilidade completa em banco de dados.

### Principais evoluções

| Área | Sprint 3 | Sprint 4 |
|------|----------|----------|
| Persistência | Dict/lista em memória | SQLite com 3 tabelas indexadas |
| Atendimento IA | Único método monolítico | Pipeline de 4 agentes orquestrados |
| Classificação de intenção | Implícita no prompt | IntentClassifierAgent explícito (rule-based, com score) |
| Extração de entidades | Nenhuma | EntityExtractorAgent (regex + Gemini structured) |
| Logs de interação | Ausentes | Tabela `interaction_logs` com intent, entidades e agent trace |
| Frontend | 3 abas | 4 abas (+Histórico de Interações) |
| API | 3 routers | 4 routers (+`/api/interactions`) |

---

## Arquitetura do Fluxo de Atendimento

```
Usuário
   │
   ▼
OrchestratorAgent
   ├── 1. IntentClassifierAgent
   │       Rule-based (regex + keywords)
   │       Retorna: intent + confidence score
   │
   ├── 2. EntityExtractorAgent
   │       Regex pass → Gemini structured output (fallback)
   │       Extrai: doc_id, tipo_documento, data, nome
   │
   ├── 3. KnowledgeAgent
   │       Consulta SQLite via process_repo
   │       Monta: KnowledgeContext com fatos relevantes por intent
   │
   ├── 4. ResponseGeneratorAgent
   │       Gemini 2.5 Flash com prompt engineering
   │       Aplica guardrails determinísticos pós-geração
   │
   └── 5. InteractionLog → SQLite (interaction_logs)
           session_id · intent · confidence · entities · agent_trace · response
```

---

## Stack Técnico

**Backend**
- Python 3.12 + FastAPI (async)
- SQLite 3 (built-in) — sem dependência extra
- Google Gemini 2.5 Flash (NLU, entity extraction, response generation)
- OpenCV (validação de documentos)

**Frontend**
- React 19 + Vite
- Axios para chamadas à API
- CSS nativo com design system glassmorphic

**Padrões**
- Service Layer + Repository Pattern
- Event-Driven Notifications (SMTP + Twilio simulados)
- Finite State Machine (FSM) para workflow de aprovação
- Prompt Engineering + Guardrails determinísticos

---

## Estrutura do Projeto

```
src/
├── backend/
│   └── app/
│       ├── database/               ← NOVO Sprint 4
│       │   ├── connection.py       # init_db(), get_connection()
│       │   ├── process_repo.py     # CRUD processos (SQLite)
│       │   ├── notification_repo.py
│       │   └── interaction_repo.py # Logs de interação
│       ├── agents/                 ← NOVO Sprint 4
│       │   ├── orchestrator.py     # Pipeline multiagente
│       │   ├── intent_classifier.py
│       │   ├── entity_extractor.py
│       │   ├── knowledge_agent.py
│       │   └── response_generator.py
│       ├── services/               (mantidos, migrados para SQLite)
│       │   ├── workflow_service.py
│       │   ├── notification_service.py
│       │   ├── ai_service.py
│       │   └── cv_service.py
│       ├── routers/
│       │   ├── documents.py
│       │   ├── chat.py             (atualizado: usa OrchestratorAgent)
│       │   ├── notifications.py
│       │   └── interactions.py     ← NOVO Sprint 4
│       └── main.py                 (atualizado: init_db no startup)
└── frontend/
    └── src/
        └── components/
            ├── InteractionHistory.jsx  ← NOVO Sprint 4
            ├── ChatInterface.jsx       (atualizado: exibe intent badge)
            ├── Dashboard.jsx
            ├── NotificationCenter.jsx
            └── StatusTimeline.jsx
```

---

## Como Executar

### Pré-requisitos
- Python 3.12+
- Node.js 18+
- (Opcional) Chave de API Gemini em `.env`

### Backend

```bash
cd src/backend

# Instalar dependências
pip install .

# Configurar IA (opcional — sem a chave entra em modo mock)
echo "GEMINI_API_KEY=sua_chave_aqui" > .env

# Iniciar servidor (o banco SQLite é criado automaticamente)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

O banco `youvisa.db` é criado automaticamente na primeira execução.

### Frontend

```bash
cd src/frontend
npm install
npm run dev
```

Acesse: `http://localhost:5173`

---

## Endpoints da API (Sprint 4)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/documents/upload` | Upload + validação + início do workflow |
| POST | `/api/documents/{id}/transition` | Transição de estado FSM |
| GET | `/api/documents/` | Lista todos os processos (SQLite) |
| GET | `/api/documents/{id}/history` | Histórico auditável |
| POST | `/api/chat/` | Chat com orquestrador multiagente |
| GET | `/api/chat/interactions/{user_id}` | Logs da sessão por usuário |
| GET | `/api/notifications/` | Notificações enviadas |
| **GET** | **`/api/interactions/`** | **Todos os logs de interação** |
| **GET** | **`/api/interactions/session/{id}`** | **Logs por sessão** |
| **GET** | **`/api/interactions/doc/{id}`** | **Logs por processo** |
| **GET** | **`/api/interactions/stats`** | **Estatísticas de intent** |

---

## Governança de IA

Cinco camadas de proteção:

1. **Rate Limiting** — máximo 10 mensagens/minuto por sessão (in-memory, janela deslizante)
2. **Input Filtering** — regex com 13 padrões PT/EN bloqueia tentativas de prompt injection antes de chegar ao LLM; limite de 2.000 caracteres por mensagem
3. **System Instruction** — Valéria tem escopo restrito: proibida de inventar prazos, garantias ou conselhos jurídicos; formatação plain text obrigatória
4. **Memory Windowing** — apenas as últimas 8 mensagens são enviadas ao LLM, eliminando context poisoning por histórico longo
5. **Guardrails determinísticos** — `BLOCKED_PHRASES` detecta frases proibidas pós-geração e substitui por `SAFE_FALLBACK` pré-aprovado; `_strip_markdown` sanitiza símbolos de formatação

---

## Banco de Dados (SQLite)

Três tabelas criadas automaticamente no startup:

```sql
processes         -- processos consulares + histórico FSM em JSON
notifications     -- emails e SMS simulados por evento
interaction_logs  -- cada turno do chat: intent, entidades, agent_trace, resposta
```

Índices em `session_id`, `doc_id` e `sent_at` para consultas eficientes.
