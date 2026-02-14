# YOUVISA — Plataforma Inteligente de Atendimento Multicanal (Sprint 3)

## 👨‍🎓 Integrantes (Grupo 21)
- <a href="https://www.linkedin.com/in/caiorcastro/">Caio Rodrigues Castro</a>
- <a href="https://www.linkedin.com/in/digitalmanagerfelipesoares/">Felipe Soares Nascimento</a>
- <a href="https://www.linkedin.com/in/fernando-segregio/">Fernando Miranda Segregio</a>
- <a href="https://www.linkedin.com/in/mralmeida">Mario Roberto Silva de Almeida</a>
- Wellington Nascimento de Brito

## 👨‍🏫 Professores
### Tutor(a)
- <a href="https://www.linkedin.com/in/leonardoorabona/">Leonardo Ruiz Orabona</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/in/profandregodoi/">Andre Godoi</a>

## 📜 Descrição
Este projeto é a implementação da **Sprint 2** do Enterprise Challenge YOUVISA. Trata-se de uma plataforma que integra Chatbot, Visão Computacional e Inteligência Artificial para automação de atendimento consular.

O sistema recebe documentos (Passaportes, Vistos), valida sua integridade visualmente, classifica o conteúdo com IA Generativa e dispara automações de e-mail simuladas.

## 📁 Estrutura de Pastas (Padrão FIAP)
- **src/backend**: API em Python (FastAPI) contendo lógica de IA, Vision e Automação.
- **src/frontend**: Interface Web em React + Vite.
- **document**: Documentação técnica e arquitetura.
- **assets**: Imagens e recursos.

## 🔧 Como Executar

### Pré-requisitos
- Python 3.12+
- Node.js 18+

### Passo 1: Backend
```bash
cd src/backend
pip install -r requirements.txt  # ou pip install fastapi uvicorn openai opencv-python-headless python-dotenv
python -m uvicorn app.main:app --reload
```
O backend rodará em `http://localhost:8000`.

### Passo 2: Frontend
```bash
cd src/frontend
npm install
npm run dev
```
O frontend rodará em `http://localhost:5173`.

## 🚀 Funcionalidades (Sprint 3 - Acompanhamento)
- **Máquina de Estados**: Controle rigoroso do fluxo (`Recebido` -> `Análise` -> `Aprovado`).
- **Timeline Visual**: Interface gráfica para acompanhar o progresso.
- **Notificações**: Alertas automáticos a cada mudança de estado.
- **IA Explicativa**: O Chatbot explica o status atual em linguagem simples.

## 🤖 Funcionalidades (Sprint 2 - Automação)
- **Chat Inteligente**: Responde dúvidas sobre vistos usando NLP.
- **Validação de Documentos**: OpenCV verifica se o upload é uma imagem válida.
- **Classificação**: IA Generativa (Mock ou OpenAI Real) extrai dados do documento.
- **Automação**: Disparo simulado de e-mails de confirmação.

## 📝 Licença
MIT
