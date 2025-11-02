# Integrações — Canais, Webhooks e Serviços

## Canais

- Telegram (MVP): Bot API com webhook HTTPS
- WhatsApp Cloud API (MRP): endpoints Meta para mensagens e mídia
- Web Widget (futuro): iframe ou SDK de chat

---

## Webhook (padrão de mensagem)

Request (normalizado):
```json
{
  "canal": "telegram",
  "usuario_ref": "12345",
  "mensagem": { "texto": "quero iniciar" },
  "metadados": { "lang": "pt-BR" }
}
```

Response (orquestrador → canal):
```json
{
  "resposta": {
    "texto": "Escolha uma opção:",
    "botoes": ["Iniciar Solicitação", "Consultar Status", "Falar com Humano"]
  }
}
```

---

## Serviços de Apoio

- Postgres (RDS/Aurora no MRP)
- Storage S3-compatível para anexos (MRP)
- E-mail/Desk para handoff humano (MVP)

---

## Segurança de Integração

- Assinatura/HMAC nos webhooks
- Lista de IPs/allowlist quando possível
- Rate limiting por canal

---

## Idempotência e Resiliência

- Idempotency-Key nos requests para evitar duplicidade em retries
- Timeouts e backoff exponencial nas chamadas externas
- Dead-letter (futuro) para eventos não processados
