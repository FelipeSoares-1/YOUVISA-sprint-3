# Relatório Técnico — Sprint 3: Acompanhamento Inteligente de Processos

## 1. Decisões de Arquitetura

### 1.1 Máquina de Estados Finitos (FSM)
Implementamos uma **Máquina de Estados Finitos determinística** no `WorkflowService` com um mapa de transições válidas (`VALID_TRANSITIONS`). Cada estado define explicitamente quais eventos são aceitos e para qual estado resultam, impedindo transições inválidas (ex: `RECEBIDO → APROVADO` sem análise).

**Estados definidos**: `RECEBIDO`, `EM_ANALISE`, `PENDENTE_DOCS`, `APROVADO`, `REPROVADO`, `FINALIZADO`.

**Persistência**: Os dados são armazenados em memória (dict Python) para este MVP, mas a estrutura de dados segue o padrão de um banco não-relacional (documentos JSON), facilitando futura migração para MongoDB ou DynamoDB.

### 1.2 Arquitetura Event-Driven
Cada transição de estado dispara automaticamente um **hook de notificação** para o `NotificationService`. Este padrão desacopla a lógica de workflow da lógica de comunicação — o serviço de workflow não precisa saber como notificar (email, SMS, webhook), apenas que deve notificar.

As notificações são **persistidas em lista auditável** com timestamp ISO 8601, canal, destinatário e doc_id, e são expostas via API REST (`GET /api/notifications/`).

### 1.3 Classificação de Intenções no Chatbot
O chatbot utiliza um **classificador de intenções baseado em keywords** com pontuação ponderada, cobrindo 5 categorias:
- **STATUS_QUERY**: "qual o status?", "como está?", "andamento"
- **MISSING_DOCS**: "falta documento?", "o que está faltando?"
- **NEXT_STEP**: "qual próximo passo?", "o que preciso fazer?"
- **DEADLINE**: "quanto tempo?", "prazo?"
- **GENERAL**: fallback contextualizado

O contexto da conversa é armazenado por `user_id`, mantendo coerência ao longo da sessão (últimas 20 mensagens).

### 1.4 Governança de IA (Guardrails)
Implementamos uma camada **dupla de proteção**:
1. **System Prompt Rígido**: Instruções explícitas que proíbem a IA de inventar prazos, garantir aprovações ou recomendar ações legais.
2. **Filtro Determinístico de Output** (`apply_guardrails`): Uma lista de **frases proibidas** (`BLOCKED_PHRASES`) é verificada contra a resposta da IA. Se qualquer frase proibida for detectada, a resposta é substituída por uma **mensagem pré-aprovada** (`SAFE_FALLBACK`), garantindo que nenhuma comunicação indevida chegue ao usuário.

Essa abordagem combina a flexibilidade da IA Generativa com a segurança de regras determinísticas.

### 1.5 Extração de Campos (Visão Computacional)
O `CVService` simula extração de campos padronizados de documentos: tipo, nome completo, número, data de validade, país de emissão e código MRZ. Quando o arquivo é uma imagem real, o OpenCV valida dimensões e formato. Essa extração alimenta o `AIService` para classificação mais precisa.

## 2. Rastreabilidade e Auditoria
Todas as transições de estado geram **logs estruturados em JSON** com campos: `doc_id`, `from_status`, `to_status`, `event`, `timestamp`, `description`. O histórico completo de cada processo é acessível via `GET /api/documents/{doc_id}/history`, atendendo ao requisito de **histórico auditável**.

## 3. Interface e Experiência do Usuário
O frontend React implementa:
- **Timeline Visual** com ícones, animação de pulso no step atual e log de transições inline.
- **Central de Notificações** com badge de contagem e painel expansível, consumindo a API de notificações em tempo real (polling a cada 3s).
- **Painel Admin** com botões contextuais (cada ação só aparece quando válida para o estado atual).

## 4. Conclusão
A Sprint 3 transformou a plataforma YOUVISA de um sistema reativo para um **agente ativo de comunicação**. O cliente tem visibilidade total do processo, recebe notificações automáticas e interage com um chatbot governado que explica cada etapa em linguagem simples, sem riscos de comunicação indevida.
