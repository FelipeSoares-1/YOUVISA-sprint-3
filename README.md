# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# YOUVISA Sprint 3 - Plataforma de Acompanhamento Inteligente

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/in/caiorcastro/">Caio Rodrigues Castro</a> 
- <a href="https://www.linkedin.com/in/celeste-leite-dos-santos-66352a24b/">Celeste Leite dos Santos</a> 
- <a href="https://www.linkedin.com/in/digitalmanagerfelipesoares/">Felipe Soares Nascimento</a>
- <a href="https://www.linkedin.com/in//">Wellington Nascimento de Brito</a>

## �‍🏫 Professores:
### Tutor(a) 
- <a href="https://www.linkedin.com/in/leonardoorabona/">Leonardo Ruiz Orabona</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/in/profandregodoi/">André Godoi Chiovato</a>

---

## 📜 Descrição do Projeto (Sprint 3)

O **YOUVISA** evoluiu nesta Sprint 3 para se tornar uma plataforma inteligente de **Acompanhamento de Processos Consulares**. Além de validar documentos com Visão Computacional (Sprint 2), o sistema agora gerencia o ciclo de vida do pedido (Workflow), notifica o usuário a cada etapa e utiliza IA Generativa para explicar o status técnico em linguagem natural.

## 🚀 Funcionalidades Principais

### 1. Máquina de Estados (Workflow)
O sistema implementa uma máquina de estados finitos robusta para garantir a integridade do processo:
- **RECEBIDO**: Documento enviado pelo usuário.
- **EM ANÁLISE**: Equipe técnica inicia a validação.
- **PENDENTE**: Falta de documentos ou informações.
- **APROVADO / REPROVADO**: Decisão final.

### 2. Timeline Visual
Um componente de frontend (`StatusTimeline`) permite ao usuário visualizar exatamente onde seu processo está na esteira de aprovação.

### 3. Atendimento Inteligente (IA Contextual)
O Chatbot agora é "consciente do contexto". Se o usuário pergunta *"Como está meu pedido?"*, a IA consulta o estado atual no Workflow e responde de forma personalizada (ex: *"Seu pedido está em análise técnica, aguarde a validação..."*), respeitando **Guardrails** de segurança para não prometer prazos falsos.

### 4. Notificações Ativas
O sistema dispara eventos (simulados via log/console) sempre que um status muda, mantendo o usuário informado sem necessidade de refresh constante.

## 📁 Estrutura do Projeto
- `src/backend`: API FastAPI com serviços de Workflow, AI e Notificação.
- `src/frontend`: Aplicação React com Dashboard de Acompanhamento.
- `document`: Documentação técnica detalhada, diagramas e relatórios.

## 🔧 Como Executar

### Backend
```bash
cd src/backend
# Instalar dependências
pip install -r requirements.txt
# Rodar servidor
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd src/frontend
# Instalar dependências
npm install
# Rodar aplicação
npm run dev
```

## 📝 Licença
[Attribution 4.0 International](http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1)
