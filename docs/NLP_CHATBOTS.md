# NLP e Chatbots — Intents, Entidades e Políticas

## Objetivo
Definir o núcleo de entendimento (NLU) e a política de diálogo para o MVP (Telegram) e evolução no MRP.

---

## Intents (MVP)

- saudacao (ex.: oi, olá)
- ajuda (como funciona, ajuda)
- menu (mostrar opções)
- iniciar_solicitacao (novo visto, iniciar processo)
- status (consultar status)
- falar_humano (falar com atendente)
- fallback (não compreendido)

Respostas padrão e prompts guiados devem minimizar ambiguidades no MVP.

---

## Entidades (MRP)

- nome
- pais_destino
- tipo_documento (passaporte, RG, etc.)
- data (viagem, agendamento)

---

## Pipeline NLU

- MVP
  - Tokenização + embeddings (spaCy ou SentenceTransformers)
  - Classificação de intenções (sklearn/lightweight)
  - Regras para palavras-chave do menu

- MRP
  - Rasa NLU com entidades e desambiguação
  - Treinamento com conjunto maior de exemplos

---

## Estratégia de Dados para NLU

- Coleta inicial: exemplos a partir de scripts de demo e brainstorm da equipe
- Rotulagem: planilha simples com colunas [texto, intent, entidades]
- Validação: split treino/validação; cross-validation no MVP
- Evolução: coletar frases reais com consentimento e anonimização

---

## Prós e Contras

- Regras + embeddings (MVP):
  - Prós: rápido, interpretável, barato
  - Contras: cobertura limitada, fragilidade a variações
- Rasa (MRP):
  - Prós: robustez, entidades, histórias de diálogo
  - Contras: exige operação (treino/versão), mais tuning

---

## Política de Diálogo

- Priorizar fluxos guiados por menu
- Confirmar dados sensíveis antes de persistir
- Fallback → oferecer opções + handoff humano

---

## Handoff Humano

- Intenção explícita “falar_humano”
- Baixa confiança (<0.4) por 2 turnos consecutivos

---

## Avaliação NLU

- MVP: acurácia >70% (cross-validation)
- MRP: acurácia >85%; F1 por intenção >0.8
