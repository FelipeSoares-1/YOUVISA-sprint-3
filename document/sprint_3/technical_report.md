# Relatório Técnico - Sprint 3

## Decisões de Arquitetura

### 1. Máquina de Estados (FSM)
Implementamos uma **Máquina de Estados Finitos** no `WorkflowService` para garantir a integridade do processo.
- **Estados**: `RECEBIDO`, `EM_ANALISE`, `PENDENTE_DOCS`, `APROVADO`, `REPROVADO`.
- **Controle**: Transições são permitidas apenas através de eventos específicos (`START_ANALYSIS`, `APPROVE`, etc.), impedindo mudanças de estado inválidas (ex: de `RECEBIDO` para `APROVADO` sem análise).

### 2. Event-Driven Architecture (Simulada)
Adotamos um padrão de eventos onde cada transição de estado dispara um "hook" para o `NotificationService`.
- **Benefício**: Desacoplamento. O workflow não precisa saber *como* notificar (email, sms), apenas *que* deve notificar.

### 3. Governança de IA (Guardrails)
No `AIService`, implementamos barreiras de segurança (System Prompts Rígidos) para mitigar alucinações.
- **Regra Crítica**: A IA é explicitamente proibida de inventar prazos ou garantir aprovações que não estejam no estado do sistema.
- **Contexto**: A IA recebe o histórico do processo para gerar explicações personalizadas, mas limitadas aos fatos.

### 4. Frontend: Timeline Visual
Criamos o componente `StatusTimeline` para dar visibilidade imediata ao usuário.
- **UX**: Uso de indicadores visuais (steps) para reduzir a ansiedade do cliente e a necessidade de contato com suporte.

## Desafios e Soluções
- **Desafio**: Sincronizar o estado do frontend com o backend.
- **Solução**: Implementamos *polling* no Dashboard (a cada 2s) para garantir que o cliente veja a mudança de estado assim que ela ocorre no backend (simulando WebSocket para este MVP).

## Conclusão
A Sprint 3 elevou a maturidade da plataforma, transformando-a de um "recebedor de arquivos" para um "gerente de processos" ativo e transparente.
