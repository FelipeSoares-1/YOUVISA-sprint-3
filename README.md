# YOUVISA — Plataforma Inteligente de Atendimento Multicanal (Sprint 1)

Documentação de planejamento da Sprint 1 (proposta técnica) do Enterprise Challenge — FIAP.

Prazo: 05/11/2025 23:59 | Grupo: 21

---

## Visão Geral (Problema e Solução)

Empresas que lidam com serviços de vistos e consulares precisam escalar atendimentos, reduzir tarefas repetitivas e manter a continuidade da experiência entre canais (Telegram, WhatsApp, Web). Esta proposta define uma plataforma de atendimento multicanal, com NLP para entendimento de intenções, orquestração de diálogos, automação (RPA) e governança de dados (segurança e LGPD).

Nesta Sprint: planejamento e arquitetura inicial, sem código obrigatório. No próximo ciclo, o MVP implementará o canal Telegram com NLU básico e handoff humano.

---

## Conteúdo e Navegação

- Enunciado oficial: `docs/DESAFIO.md`
- Checklist de aderência: `docs/CHECKLIST_ADERENCIA.md`
- Plano de desenvolvimento (MVP/MRP, backlog, RACI, cronograma): `docs/PLANO_DESENVOLVIMENTO.md`
- Arquitetura (C4, componentes, sequências): `docs/ARQUITETURA.md`
- NLP e Chatbots (intents, entidades, fallback, handoff): `docs/NLP_CHATBOTS.md`
- Fluxos de Chatbot (Telegram/WhatsApp, menus): `docs/FLUXOS_CHATBOT.md`
- Dados e Análise (modelo lógico, retenção, métricas): `docs/DADOS_E_ANALISE.md`
- Segurança e Privacidade (LGPD, IAM, criptografia): `docs/SEGURANCA_PRIVACIDADE.md`
- RPA e Automação (processos candidatos): `docs/RPA_AUTOMACAO.md`
- Integrações (APIs, canais, webhooks): `docs/INTEGRACOES.md`
- Validação de Documentos (visão computacional): `docs/CV_VALIDACAO_DOCUMENTOS.md`
- Relatórios e Insights: `docs/ANALYTICS_RELATORIOS.md`
- Stack técnica e justificativas: `docs/TECH_STACK.md`
- Decisões técnicas (ADR): `docs/DECISOES_TECNICAS.md`

---

## Entregáveis desta Sprint

- Proposta técnica consolidada (este repositório)
- Arquitetura desenhada e justificada
- Plano inicial (MVP/MRP), backlog priorizado e RACI
- Estratégia de dados, segurança e integrações

Repositório privado; adicionar colaborador tutor: `leoruiz197`.

---

## Resumo Rapido

| Entregavel | Arquivo(s) | Status |
|---|---|---|
| Proposta tecnica | `README.md` | OK |
| Enunciado centralizado | `docs/DESAFIO.md` | OK |
| Arquitetura | `docs/ARQUITETURA.md`, `docs/diagrams/architecture.png` | OK |
| Tecnologias | `docs/TECH_STACK.md` | OK |
| NLP/Fluxos | `docs/NLP_CHATBOTS.md`, `docs/FLUXOS_CHATBOT.md` | OK |
| Dados/Seguranca | `docs/DADOS_E_ANALISE.md`, `docs/SEGURANCA_PRIVACIDADE.md` | OK |
| RPA/Integracoes | `docs/RPA_AUTOMACAO.md`, `docs/INTEGRACOES.md` | OK |
| Planejamento | `docs/PLANO_DESENVOLVIMENTO.md` | OK |
| Avaliacao simulada | `docs/AVALIACAO_SIMULADA.md` | OK |

---

## Equipe (Grupo 21)

- Fernando Miranda Segregio — segregio@gmail.com (PO / Coordenação)
- Wellington Nascimento de Brito — well334@hotmail.com (Tech Lead / Backend)
- Mário Roberto Silva de Almeida — marioalmeida1980@gmail.com (DevOps / Cloud)
- Caio Rodrigues Castro — caiorcastro@gmail.com (NLP / Chatbot)
- Felipe Soares Nascimento — consultor.casteliano@gmail.com (QA / Documentação)

---

## Governança de Entrega

- Congelamento: tag `v1.0-sprint1` no prazo final.
- Privacidade: privado até a avaliação. Se público, remover dados sensíveis.
- Acesso do tutor: enviar convite e confirmar aceite.

---

## Como avançar para o MVP (próxima Sprint)

1) Subir um backend Python (FastAPI) com endpoints de mensagens.  
2) Integrar o bot do Telegram ao backend (webhook).  
3) Implementar NLU básico (Rasa ou regra/embeddings) com intents do menu.  
4) Persistir sessões e mensagens em Postgres.  
5) Handoff humano via e-mail/desk quando solicitado ou em fallback.  
6) Logs e métricas mínimas (prometheus + dashboard simples).

Detalhes e critérios em `docs/PLANO_DESENVOLVIMENTO.md`.
