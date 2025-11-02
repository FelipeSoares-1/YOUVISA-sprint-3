# Stack Técnica — Escolhas, Prós/Contras e Justificativas

## Linguagem e Backend

- Escolha: Python 3.11 + FastAPI
  - Prós: produtividade alta, tipagem moderna, async nativo, ecossistema maduro (NLP, automação, web)
  - Contras: throughput bruto menor que Go/Java em cenários CPU-bound; mitigável com horizontal scaling
  - Alternativas: Node.js (prós: unifica JS; contras: tooling NLP mais fraco), Java Spring (prós: robustez; contras: curva inicial)
  - Justificativa: foco em agilidade e NLP; FastAPI atende com excelente DX e performance suficiente

## NLU (Processamento de Linguagem Natural)

- MVP: spaCy + embeddings + regras de menu
  - Prós: simplicidade, baixo custo de treino, rápido de colocar no ar
  - Contras: menor robustez a variações; depende de prompts guiados
- MRP: Rasa Open Source
  - Prós: intents, entidades, políticas, desambiguação, pipeline extensível
  - Contras: maior complexidade operacional; precisa dados rotulados
  - Alternativas: HuggingFace Transformers + fine-tuning leve; Dialogflow (SaaS, lock-in)
  - Justificativa: evolução progressiva sem lock-in de fornecedor

## Banco de Dados

- Escolha: Postgres
  - Prós: ACID, JSONB quando necessário, amplo suporte, fácil de operar
  - Contras: sharding nativo limitado; mitigável com particionamento
  - Alternativas: MongoDB (prós: flexível; contras: consistência), DynamoDB (prós: escala; contras: lock-in)
  - Justificativa: modelo relacional e integrações SQL simplificam relatórios e handoff

## Canais de Atendimento

- Telegram (MVP), WhatsApp Cloud API (MRP)
  - Prós Telegram: onboarding rápido, menos fricção de aprovação
  - Contras Telegram: base de usuários menor que WhatsApp
  - Justificativa: começar pelo canal mais rápido e expandir ao mais popular na etapa confiável

## Automação (RPA)

- Escolha: Playwright
  - Prós: estável, APIs modernas, melhor controle de rede
  - Contras: curva inicial se comparado ao Selenium em equipes legadas
  - Alternativas: Selenium (prós: comunidade; contras: flakiness), Robocorp (prós: ecossistema RPA; contras: curva)

## Infra/Deploy

- MVP: Docker Compose local ou PaaS (Railway/Fly/Render) para demo
- MRP: AWS (ECS Fargate), RDS Postgres, S3, CloudWatch/CloudWatch Logs
  - Prós: serviços gerenciados reduzem operação
  - Contras: custos; mitigável com sizing e autoscaling

## Observabilidade

- MVP: logs estruturados + contadores simples
- MRP: Prometheus/Grafana; tracing se necessário (OTel)

