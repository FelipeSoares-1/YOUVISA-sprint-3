# Como Rodar o YOUVISA — Sprint 4

## Pré-requisitos

- Python 3.14 (`python3.14`)
- Node.js 18+ (`node`, `npm`)
- Arquivo `src/backend/.env` com `GEMINI_API_KEY=sua_chave`

## Passo a passo

### 1. Configurar a chave Gemini (só na primeira vez)

```bash
echo "GEMINI_API_KEY=sua_chave_aqui" > src/backend/.env
```

> O arquivo `.env` está no `.gitignore` — nunca sobe para o GitHub.

---

### 2. Instalar dependências do backend (só na primeira vez)

```bash
pip3 install google-genai fastapi uvicorn python-multipart python-dotenv opencv-python-headless
```

> O projeto usa Python 3.14 e pip3 associado a ele.

---

### 3. Iniciar o backend

```bash
cd src/backend
python3.14 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

O banco SQLite (`youvisa.db`) é criado automaticamente na primeira execução.

**Backend disponível em:** http://localhost:8000  
**Documentação interativa (Swagger):** http://localhost:8000/docs  

---

### 4. Instalar dependências do frontend (só na primeira vez)

Em outro terminal:

```bash
cd src/frontend
npm install
```

---

### 5. Iniciar o frontend

```bash
cd src/frontend
npm run dev
```

**Frontend disponível em:** http://localhost:5173

---

## Onde acessar cada coisa

| O que | URL |
|-------|-----|
| Interface principal | http://localhost:5173 |
| Painel de controle | http://localhost:5173 → aba "Painel de Controle" |
| Chat com Valéria (Gemini) | http://localhost:5173 → aba "Atendimento Inteligente" |
| Notificações | http://localhost:5173 → aba "Notificações" |
| Histórico de Interações | http://localhost:5173 → aba "Histórico de Interações" |
| API Swagger | http://localhost:8000/docs |
| Logs de interação (JSON) | http://localhost:8000/api/interactions/ |
| Stats de intents | http://localhost:8000/api/interactions/stats |
| Notificações (JSON) | http://localhost:8000/api/notifications/ |

---

## Estrutura de pastas

```
Youvisa 4/
├── src/
│   ├── backend/
│   │   ├── .env                  ← chave Gemini (NÃO vai pro GitHub)
│   │   ├── youvisa.db            ← banco SQLite (NÃO vai pro GitHub)
│   │   └── app/
│   │       ├── agents/           ← pipeline multiagente
│   │       ├── database/         ← repositórios SQLite
│   │       ├── routers/          ← endpoints da API
│   │       └── services/         ← lógica de negócio
│   └── frontend/
│       └── src/components/       ← React + Vite
├── fases_anteriores/             ← relatórios das sprints anteriores
├── evidence/                     ← evidências de teste (NÃO vai pro GitHub)
├── RELATORIO_SPRINT4.md
├── README.md
└── COMO_RODAR.md                 ← este arquivo
```
