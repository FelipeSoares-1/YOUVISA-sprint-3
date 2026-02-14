# Plano de Implementação - Sprint 3: Plataforma de Acompanhamento Inteligente

## Objetivo
Evoluir a plataforma para um sistema de **Acompanhamento de Processos**, com máquina de estados, notificações ativas e explicações via IA Generativa.

## Necessária Revisão do Usuário
> [!IMPORTANT]
> **Governança de IA**: Implementaremos "Guard Rails" rígidos para que a IA nunca invente prazos ou garanta aprovações.
> **Persistência**: Continuaremos usando persistência em memória (simulada) para agilidade do protótipo, mas estruturada como se fosse um banco real.

## Mudanças Propostas

### Backend (`src/backend`)
#### [NOVO/MODIFICADO] `app/services/workflow_service.py`
- Implementará a **Máquina de Estados Finitos (FSM)**.
- Estados: `RECEBIDO` -> `EM_ANALISE` -> `PENDENTE_DOCS` -> `APROVADO` / `REPROVADO`.
- Transições válidas e logs de eventos.

#### [MODIFICADO] `app/services/ai_service.py`
- Novo método `explain_status(status, context)`: Traduz o estado técnico para linguagem natural.
- Adição de `guardrails`: System prompts que proíbem promessas de datas.

#### [NOVO] `app/services/notification_service.py`
- Escuta eventos do Workflow.
- Dispara e-mails simulados quando o status muda.

#### [MODIFICADO] `app/routers/chat.py`
- Reconhecimento de intenção de "Consulta de Status".
- Respostas contextualizadas com o estado atual do processo do usuário.

### Frontend (`src/frontend`)
#### [NOVO] `components/StatusTimeline.jsx`
- Componente visual que mostra a linha do tempo do processo.
- Indica estado atual, passados e futuros.

#### [MODIFICADO] `components/Dashboard.jsx`
- Integração do `StatusTimeline` nos detalhes do documento.
- Botões para simular avanço de estapas (para fins de demonstração).

## Plano de Verificação

### Automatizada
- Teste unitário da FSM (garantir que não pode pular de `RECEBIDO` direto para `FINALIZADO` sem passar por análise).
- Teste de Guardrails da IA (verificar se recusa perguntas sobre datas exatas).

### Manual (Demo)
1.  **Upload**: Enviar documento -> Status: `RECEBIDO`.
2.  **Análise**: Sistema (simulado) transaciona para `EM_ANALISE` -> Notificação enviada.
3.  **Pendência**: Simular falta de documento via botão -> Status: `PENDENTE` -> Chat explica o que falta.
4.  **Consulta**: Perguntar no chat "Como está meu processo?" -> Resposta da IA com base no status real.
