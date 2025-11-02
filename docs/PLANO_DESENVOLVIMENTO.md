# Plano de Desenvolvimento — MVP/MRP, Backlog, RACI e Cronograma

Este documento define o caminho para executar a solução a partir do planejamento desta Sprint.

---

## Definições

- MVP (Minimum Viable Product): menor conjunto funcional para validar a proposta.  
  Foco: Canal Telegram, NLU básico, menu guiado, persistência de sessão, handoff humano simples, logging e segurança mínima.

- MRP (Minimum Reliable Product): versão confiável para uso controlado.  
  Foco: Adicionar WhatsApp (Cloud API), melhorar NLU, validação inicial de documentos (OCR), RPA de tarefas repetitivas, observabilidade e hardening.

---

## Escopo do MVP (Próxima Sprint)

- Canal: Telegram com webhook configurado
- Backend: FastAPI (Python 3.11) com orquestrador de diálogo
- NLU: intents base (saudação, ajuda, menu, iniciar_solicitacao, status, falar_humano, fallback)
- Persistência: Postgres (usuários, sessões, mensagens, intents)
- Handoff humano: encaminhar para e-mail/desk com contexto mínimo (histórico da conversa)
- Segurança: HTTPS, secrets em variáveis de ambiente, minimização de PII
- Observabilidade: logs estruturados + métricas simples

Critérios de aceite do MVP:
- Receber mensagens do Telegram e responder menus funcionais
- Identificar pelo menos 6 intents com precisão >70% em dataset inicial
- Registrar sessões/mensagens e histórico de intent
- Permitir handoff humano sob comando ou fallback
- Documentar setup e execução local/cloud

Fora de escopo no MVP: WhatsApp, validação profunda de documentos, RPA, dashboard de analytics.

---

## Escopo do MRP (Sprint seguinte)

- Canal: adicionar WhatsApp Cloud API (Meta) e continuidade de contexto
- NLU: melhorar acurácia (>85%), adicionar entidades (nome, país, tipo_documento, data)
- Documentos: pipeline inicial de OCR (Tesseract + OpenCV) e checks básicos (qualidade, tipo)
- RPA: automação de uma tarefa repetitiva (ex.: consulta de status, preenchimento estruturado)
- Observabilidade: métricas, alertas e tracing; relatórios básicos (KPIs)
- Segurança: criptografia at-rest e IAM refinado

---

## Backlog por Épicos (com histórias e aceite)

1) Épico: Adaptação de Canais (Telegram/WhatsApp)
- História: Configurar bot Telegram e webhook → Aceite: webhook validado e recebendo updates
- História: Normalizar mensagens (texto, mídia, arquivos) → Aceite: payload unificado
- História (MRP): Integrar WhatsApp Cloud API → Aceite: troca de mensagens validada

2) Épico: Orquestração e NLU
- História: FastAPI com rota `/messages` → Aceite: responde 200 e ecoa mensagem
- História: NLU com intents base → Aceite: >70% acurácia no dataset de teste
- História: Fallback e handoff humano → Aceite: comando “falar com humano” cria ticket
- História (MRP): entidades e desambiguação → Aceite: extrai nome/país/tipo_documento

3) Épico: Dados e Persistência
- História: Modelar e criar tabelas (usuarios, sessoes, mensagens, intents) → Aceite: migrations aplicadas
- História: Persistir histórico por sessão → Aceite: reconstroi contexto no atendimento
- História (MRP): storage de anexos (S3) → Aceite: upload/download seguro

4) Épico: Segurança e LGPD
- História: HTTPS e secrets seguros → Aceite: sem secrets no repositório
- História: Minimização de dados e consentimento → Aceite: texto padrão e logs anonimizados
- História (MRP): IAM por função (least privilege) → Aceite: política revisada

5) Épico: Handoff Humano
- História: Encaminhar para e-mail/desk com contexto → Aceite: registro do ticket com histórico
- História (MRP): Backoffice simples para triagem → Aceite: visualizar tickets e marcar como atendido

6) Épico: Documentos e RPA (MRP)
- História: OCR básico e validação mínima de imagem → Aceite: extrai texto e valida formato
- História: Automação Playwright/Selenium para consulta/registro → Aceite: script idempotente

7) Épico: Observabilidade e Relatórios
- História: Logs estruturados e métricas básicas → Aceite: contador de mensagens/intents
- História (MRP): Dashboard de KPIs → Aceite: taxa de resolução, FCR, TMA, SLA de handoff

---

## RACI (Papéis e Responsabilidades)

- Product Owner (R/A): Fernando Miranda Segregio
- Tech Lead Backend (R): Wellington Nascimento de Brito
- DevOps/Cloud (R): Mário Roberto Silva de Almeida
- NLP/Chatbot (R): Caio Rodrigues Castro
- QA & Documentação (R): Felipe Soares Nascimento

Legenda: R = Responsible, A = Accountable, C = Consulted, I = Informed

---

## Cronograma sugerido (pós-Sprint 1)

- Semana 1: Setup repositório, FastAPI, bot Telegram, Postgres
- Semana 2: NLU base, persistência, handoff humano básico
- Semana 3: Hardening, testes e evidências; demo MVP
- Semana 4–5: WhatsApp, OCR inicial, 1 automação RPA
- Semana 6: Observabilidade e dashboard; MRP

Milestones:
- M1: Bot Telegram on-line (MVP)
- M2: NLU >70% + persistência + handoff
- M3: MRP com WhatsApp + OCR + 1 RPA

---

## Validações e Checkpoints

- Revisão técnica interna ao fim de cada semana (pareamento)
- Demonstração do MVP (script de demo com cenários felizes e de fallback)
- Auditoria de segurança básica: verificação de secrets e PII
- Freeze: criar tag `v1.0-sprint1` e checklist 100% marcado

---

## Definition of Done (DoD)

- Critérios de aceite atendidos e revisados por par
- Documentação atualizada e linkada no README
- Sem secrets em repositório; variáveis .env referenciadas
- Logs mínimos e evidências (prints, registros)

---

## Riscos e Mitigações

- Acesso à API do WhatsApp: risco de aprovação → Mitigação: começar por Telegram
- Qualidade do NLU: dataset pequeno → Mitigação: menu guiado + fallback
- LGPD/PII: risco de coleta excessiva → Mitigação: minimização e consentimento explícito
- Instabilidade de integrações: Mitigação: retrials e DLQ (futuro)
