# Arquitetura da Solução

Objetivo: plataforma multicanal com orquestração de diálogo, NLU, handoff humano, automação (RPA) e governança de dados.

---

## Diagrama (visão de componentes)

```mermaid
flowchart LR
  subgraph Canais
    TG[Telegram]
    WA[WhatsApp Cloud API]
    WEB[Web Widget]
  end

  TG --> GA[Gateway de Canais]
  WA --> GA
  WEB --> GA

  GA --> ORC[Orquestrador (FastAPI)]
  ORC --> NLU[Motor NLU (Rasa/Embeddings)]
  ORC --> KB[Base de Conhecimento/FAQ]
  ORC --> CTX[Store de Contexto (Postgres)]
  ORC --> RPA[RPA Workers]
  ORC --> DOC[Pipeline de Documentos (OCR/CV)]
  ORC --> HUM[Handoff Humano]

  CTX <--> DB[(Postgres)]
  DOC --> OBJ[(Object Storage)]
  ORC --> OBS[Observabilidade/Logs]
```

---

## Fluxo de Mensagem (sequência)

1) Usuário envia mensagem no canal (Telegram no MVP)  
2) Gateway normaliza o payload e chama `/messages` no Orquestrador  
3) Orquestrador consulta contexto da sessão e aciona NLU  
4) Decide ação: responder, pedir dados, chamar RPA, validar documento, ou handoff humano  
5) Persistência de eventos e métricas  
6) Resposta ao canal

---

## Decisões-chave

- Linguagem: Python 3.11; FastAPI (simplicidade + async)
- NLU: MVP com spaCy/regras; MRP com Rasa
- Banco: Postgres (sessions, messages, intents, tickets)
- Storage: S3-compatível (para anexos, se houver)
- Deploy MVP: Docker Compose (local) e/ou PaaS; MRP: AWS (ECS/Fargate)
- Observabilidade: logs estruturados + contadores; MRP: Prometheus/Grafana

---

## Dados e Modelagem (alto nível)

- usuarios(id, canal, user_ref, consentimento, criado_em)
- sessoes(id, usuario_id, status, canal, criado_em, atualizado_em)
- mensagens(id, sessao_id, direcao, texto, intent, score, criado_em)
- tickets(id, sessao_id, motivo, status, atribuido_a, criado_em)
- documentos(id, usuario_id, tipo, url_storage, status_validacao, criado_em)

---

## Handoff Humano

- Gatilhos: intenção “falar_humano”, baixa confiança, regra de negócio
- Conteúdo: histórico de sessão, última mensagem, metadados do usuário (minimizados)
- Canal: e-mail/desk no MVP; backoffice simples no MRP

---

## Segurança

- TLS fim-a-fim; secrets via env; minimização de dados
- Criptografia em repouso no MRP; IAM por função (least privilege)

---

## Trade-offs e Riscos

- Orquestrador único (pró: simplicidade; contra: acoplamento). Mitigação: contratos claros e camadas (adapter/gateway)
- Postgres para tudo (pró: consistência; contra: latência em alta escala). Mitigação: Redis para sessões quentes
- NLU leve no MVP (pró: rapidez; contra: ambiguidade). Mitigação: menus guiados e thresholds de confiança
- Integração WhatsApp (risco: aprovação/limites). Mitigação: começar por Telegram e manter gateway agnóstico

