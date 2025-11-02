# Decisões Técnicas (ADR)

Formato: Contexto → Decisão → Alternativas → Consequências

## ADR-001 — Plataforma Cloud

- Contexto: precisamos de ambiente gerenciável para MRP; MVP pode rodar local/PaaS
- Decisão: AWS para MRP (ECS/RDS/S3/CloudWatch); MVP em Compose/PaaS
- Alternativas: GCP (GKE/CloudSQL), Azure (AKS/PG), on-prem
- Consequências: reduz operação (pró); custo sob demanda (contra); menor lock-in que serviços proprietários de NLP

## ADR-002 — Linguagem e Framework

- Contexto: foco em NLP e integração rápida
- Decisão: Python 3.11 + FastAPI
- Alternativas: Node/Express, Java/Spring
- Consequências: produtividade alta; performance adequada com escala horizontal; curva menor para time

## ADR-003 — NLU (Evolução)

- Contexto: dados rotulados escassos na Sprint 1
- Decisão: MVP com spaCy/embeddings+regras; MRP com Rasa
- Alternativas: Dialogflow (SaaS), HF Transformers custom
- Consequências: valida rápido (pró); aumenta complexidade no MRP (contra); sem lock-in

## ADR-004 — Canais

- Contexto: aprovação e time-to-first-message
- Decisão: Telegram primeiro; WhatsApp no MRP
- Alternativas: Web-only no MVP
- Consequências: onboarding rápido (pró); impacto menor de base (contra); adiciona WhatsApp quando já houver base funcional

## ADR-005 — Banco de Dados

- Contexto: sessões, mensagens e tickets pedem consistência
- Decisão: Postgres
- Alternativas: MongoDB, DynamoDB
- Consequências: SQL facilita relatórios; escala suficiente; sharding não nativo (mitigável)

## ADR-006 — Handoff Humano

- Contexto: precisamos validar processo sem criar sistema inteiro
- Decisão: e-mail/desk no MVP; backoffice simples no MRP
- Alternativas: integrar ferramenta de suporte (Zendesk/Freshdesk)
- Consequências: menor esforço inicial; adiciona esforço de backoffice no MRP

## ADR-007 — Documentos e OCR

- Contexto: checagens básicas de documentos e antifraude simples
- Decisão: Tesseract + OpenCV no MRP
- Alternativas: APIs SaaS (Google Vision/Azure OCR)
- Consequências: custo menor e offline (pró); mais tuning necessário (contra)

## ADR-008 — Topologia de Orquestração

- Contexto: coordenar NLU, contexto e integrações
- Decisão: orquestrador central (FastAPI) chamando serviços
- Alternativas: coreografia via filas; microserviços desde o início
- Consequências: simplicidade (pró); risco de acoplamento (mitigar com contratos e camadas)

## ADR-009 — Store de Sessão/Contexto

- Contexto: resgatar histórico por usuário/canal
- Decisão: Postgres no MVP/MRP; cache Redis futuro se necessário
- Alternativas: Redis-only; MongoDB
- Consequências: consistência (pró); latência aceitável; pode adicionar Redis para hot context

