# Roteiro de Demo (MVP)

Objetivo: demonstrar fluxos principais no Telegram com mensagens exemplificadas.

---

## Cenário 1 — Iniciar Solicitação

Usuário: Olá
Bot: Olá! Posso ajudar. Escolha uma opção:
- Iniciar Solicitação
- Consultar Status
- Falar com Humano

Usuário: Iniciar Solicitação
Bot: Ótimo! Para começarmos, informe seu país de destino.
Usuário: Canadá
Bot: Perfeito. Tipo de documento? (Passaporte, RG...)
Usuário: Passaporte
Bot: Confirmando: destino Canadá, documento Passaporte. Posso prosseguir?
Usuário: Sim
Bot: Protocolo criado: YV-2025-00123. Você pode acompanhar em “Consultar Status”.

---

## Cenário 2 — Consultar Status

Usuário: Consultar Status
Bot: Informe seu protocolo (ex.: YV-2025-00123)
Usuário: YV-2025-00123
Bot: Status: Em análise. Previsão: 3 dias úteis.

---

## Cenário 3 — Handoff Humano

Usuário: Falar com Humano
Bot: Certo, estou encaminhando seu atendimento. Você receberá retorno em breve.
(ticket criado com resumo das últimas mensagens)

