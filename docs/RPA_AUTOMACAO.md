# RPA e Automação de Processos

## Objetivo
Reduzir tarefas repetitivas como consulta de status e pré-preenchimento de formulários.

---

## Candidatos a Automação

- Consulta de status em portais consulares
- Extração de campos de documentos (com OCR) e validação de consistência
- Pré-preenchimento de formulários com dados coletados no chat

---

## Ferramentas

- MVP: Playwright (headless) para navegação estável
- Alternativas: Selenium (amplo suporte, porém mais flakey), Robocorp/RPA Framework (ecossistema RPA voltado a negócios)

---

## Boas Práticas

- Idempotência: retentativas com backoff
- Observabilidade: logs por etapa e prints ao falhar
- Segurança: não registrar PII em logs; segredos via vault/env

---

## Prós/Contras por Abordagem

- Playwright
  - Prós: moderno, tracing embutido, controle de rede
  - Contras: menos material legado
- Selenium
  - Prós: comunidade enorme, compatibilidade
  - Contras: maior flakiness, API mais antiga
- Robocorp/RPA Framework
  - Prós: focado em automação de processos, ferramentas de orquestração
  - Contras: curva e tooling específico
