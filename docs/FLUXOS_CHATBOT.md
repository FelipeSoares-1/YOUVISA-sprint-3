# Fluxos do Chatbot (Telegram e WhatsApp)

## Menu Principal (MVP – Telegram)

```mermaid
flowchart TD
  A[Início] --> B{Menu}
  B --> C[Iniciar Solicitação]
  B --> D[Consultar Status]
  B --> E[FAQ / Informações]
  B --> F[Falar com Humano]
  C --> C1[Coletar dados mínimos]
  C1 --> C2[Confirmar]
  C2 --> C3[Protocolo criado]
  D --> D1[Solicitar identificador]
  D1 --> D2[Retornar status]
  E --> E1[Listar tópicos]
  E1 --> E2[Responder]
  F --> F1[Encaminhar para atendente]
```

Mensagens devem ser curtas, com botões quando possível.

---

## Fluxo de Handoff

1) Usuário escolhe “Falar com Humano” ou cai em fallback
2) Gerar ticket com histórico resumido (últimas N mensagens)
3) Encaminhar para e-mail/desk no MVP; backoffice no MRP
4) Registrar hora de abertura, SLA e atributo responsável

---

## WhatsApp (MRP)

- Adicionar canal WhatsApp Cloud API com as mesmas rotas do Telegram
- Manter consistência de mensagens e contexto compartilhado

