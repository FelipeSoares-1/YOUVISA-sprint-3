# YOUVISA Sprint 4 — Relatório Técnico

**Grupo 41 · FIAP Enterprise Challenge**  
Caio Rodrigues Castro · Felipe Soares Nascimento · Fernando Miranda Segregio · Mario Roberto Silva de Almeida · Wellington Nascimento de Brito

---

## 1. Organização dos Agentes Inteligentes

A Sprint 4 introduz uma arquitetura de **orquestração multiagente sequencial**, onde o `OrchestratorAgent` coordena quatro agentes especializados em pipeline. Cada agente tem responsabilidade única e passa seu resultado como entrada para o próximo.

### Pipeline de execução

**OrchestratorAgent** recebe a mensagem do usuário e executa:

**① IntentClassifierAgent**  
Classifica a intenção da mensagem usando correspondência de padrões regex e lista de palavras-chave. Retorna o intent (`STATUS_QUERY`, `MISSING_DOCS`, `NEXT_STEP`, `DEADLINE`, `APPROVAL_STATUS`, `DOCUMENT_INFO`, `GREETING`, `HELP`, `GENERAL`) junto a um *confidence score* (0.0–1.0) calculado pela proporção de keywords correspondidas em relação ao tamanho do padrão. Não consome API externa — é determinístico e de latência zero.

**② EntityExtractorAgent**  
Extrai entidades estruturadas da mensagem em dois passes: primeiro um *regex pass* (UUID para `doc_id`, termos de tipo de documento, datas no formato `DD/MM/AAAA`) e, caso o resultado seja vazio e um cliente Gemini esteja disponível, um *Gemini structured pass* com schema Pydantic. Campos extraídos: `doc_id`, `document_type`, `date_mentioned`, `person_name`.

**③ KnowledgeAgent**  
Consulta o SQLite via `process_repo` usando o `doc_id` extraído (ou o processo mais recente como fallback). Monta um `KnowledgeContext` com: sumário do processo, histórico de transições e lista de fatos relevantes **filtrados pelo intent detectado** (ex.: para `MISSING_DOCS`, busca documentos pendentes por status; para `DEADLINE`, retorna a política de prazos).

**④ ResponseGeneratorAgent**  
Recebe o contexto montado e gera a resposta final via Gemini 2.5 Flash, com *system instruction* restritiva (Valéria). O texto gerado passa obrigatoriamente por `apply_guardrails()` antes de ser retornado. Em modo mock (sem API key), retorna respostas pré-aprovadas por intent.

Ao final, o `OrchestratorAgent` persiste o log completo da interação no SQLite, incluindo o *agent trace* (saída de cada agente) para auditoria.

---

## 2. Como as Perguntas dos Usuários São Interpretadas

O processo de interpretação é **bifásico e complementar**:

### Fase 1 — Classificação de Intenção (rule-based)

O `IntentClassifierAgent` mantém um mapa de 9 intents, cada um com lista de padrões regex. Para a mensagem "Qual o status do meu processo?", o algoritmo:

1. Normaliza o texto para minúsculas
2. Testa cada padrão de `STATUS_QUERY` (ex.: `r"status"`, `r"andamento"`, `r"como está"`)
3. Conta correspondências e calcula: `confidence = base_conf × (0.7 + 0.3 × ratio_correspondido)`
4. Retorna o intent com maior score

A abordagem rule-based garante comportamento **previsível, auditável e sem custo de API** para a etapa de classificação.

**Decisão de design — rule-based vs. probabilístico:** Consideramos o uso de modelos probabilísticos (Naive Bayes, BERT fine-tuned, Rasa NLU) para a classificação de intent. A opção rule-based foi adotada conscientemente pelos seguintes motivos: (1) volume de dados rotulados insuficiente no contexto da sprint para treinar um classificador supervisionado confiável; (2) o domínio consular é restrito e bem delimitado — 9 intents cobrem >95% dos casos de uso; (3) latência zero e total rastreabilidade (cada keyword correspondida é registrada no `agent_trace`). A evolução natural para um modelo probabilístico ocorreria no MRP, após acúmulo de logs reais de interação para treinamento.

### Fase 2 — Extração de Entidades

Após saber *o que* o usuário quer, o `EntityExtractorAgent` identifica *sobre o quê*. Um UUID na mensagem é capturado por regex e usado como `doc_id` para busca direta. Termos como "passaporte" ou "visto" populam `document_type`. Datas no formato `DD/MM/AAAA` são capturadas para contexto temporal.

### Fase 3 — Contextualização e Geração

Com intent e entidades definidos, o `KnowledgeAgent` seleciona **apenas os fatos relevantes** para aquele intent específico — evitando sobrecarregar o prompt com informações irrelevantes. O `ResponseGeneratorAgent` monta um prompt estruturado com: contexto do processo, fatos selecionados, histórico recente da conversa (últimas 8 mensagens) e a mensagem do usuário.

---

## 3. Registro das Interações no Sistema

Cada turno do chatbot gera um registro estruturado persistido em SQLite na tabela `interaction_logs`:

```
id                  TEXT  — UUID único do log
session_id          TEXT  — identificador do usuário/sessão
doc_id              TEXT  — processo associado (quando identificado)
user_message        TEXT  — mensagem original do usuário
detected_intent     TEXT  — intent classificado (ex: STATUS_QUERY)
intent_confidence   REAL  — score de confiança (0.0–1.0)
entities            TEXT  — JSON com entidades extraídas
agent_trace         TEXT  — JSON com output de cada agente (auditoria)
response            TEXT  — resposta final entregue ao usuário
timestamp           TEXT  — ISO-8601 UTC
```

O campo `agent_trace` armazena o output de cada agente na ordem de execução, permitindo reconstruir exatamente como qualquer resposta foi produzida — quais keywords foram encontradas, quais entidades foram extraídas, quais fatos do banco foram usados.

Os logs são acessíveis via:
- `GET /api/interactions/` — todos os logs paginados
- `GET /api/interactions/session/{id}` — histórico de uma sessão
- `GET /api/interactions/doc/{id}` — interações sobre um processo
- `GET /api/interactions/stats` — distribuição de intents e confiança média

No frontend, a aba **Histórico de Interações** exibe cada log com intent badge colorido, entidades extraídas e o agent trace expansível — permitindo ao operador visualizar o raciocínio do sistema para cada resposta.

---

## Considerações Finais

A Sprint 4 entregou os requisitos com decisões técnicas que equilibram sofisticação e praticidade: SQLite elimina a volatilidade sem introduzir infraestrutura extra; o classifier rule-based garante determinismo na etapa mais crítica; o Gemini fica reservado para as etapas onde geração de linguagem é necessária. O resultado é um sistema **rastreável, governado e pronto para produção** com banco real.
