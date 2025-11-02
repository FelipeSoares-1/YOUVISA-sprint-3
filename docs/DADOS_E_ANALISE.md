# Dados e Análise — Modelo, Retenção e Métricas

## Objetivo
Definir como coletamos, armazenamos e analisamos dados de interação para melhorar o serviço, respeitando LGPD.

---

## Modelo Lógico (MVP)

- usuarios(id, canal, user_ref, consentimento, criado_em)
- sessoes(id, usuario_id, canal, status, criado_em, atualizado_em)
- mensagens(id, sessao_id, direcao, texto, intent, score, criado_em)
- tickets(id, sessao_id, motivo, status, atribuido_a, criado_em)

MRP adiciona: documentos, anexos (object storage), eventos de RPA e métricas agregadas.

---

## Retenção e Privacidade

- PII mínima; anonimização de logs
- Retenção sugerida: 180 dias para mensagens e sessões; 30 dias para anexos de documentos temporários
- Consentimento explícito ao iniciar atendimento

---

## Métricas (KPIs)

- Volume de mensagens por canal
- Taxa de resolução no bot (sem handoff)
- Tempo médio de atendimento (TMA)
- Taxa de fallback e causas
- SLA de handoff humano

Dashboards definidos em `docs/ANALYTICS_RELATORIOS.md`.

---

## Classificação de Dados (LGPD)

- Público: documentação, FAQs, métricas agregadas
- Interno: logs operacionais sem PII
- Sensível: identificadores de sessão/usuário, anexos de documentos
- Tratamento: minimização por padrão; encriptação at-rest no MRP; acesso por perfil

---

## Trade-offs de Armazenamento

- Relacional (Postgres):
  - Prós: queries ricas, consistência, relatórios fáceis
  - Contras: escala horizontal é mais trabalhosa
- NoSQL (documentos):
  - Prós: flexível para histórico de mensagens volumoso
  - Contras: consultas analíticas mais difíceis
  - Decisão: Postgres como fonte única; avaliar data lake/dw no futuro
