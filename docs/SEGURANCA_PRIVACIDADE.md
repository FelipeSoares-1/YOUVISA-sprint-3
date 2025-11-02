# Segurança e Privacidade (LGPD)

## Princípios

- Minimização de dados; finalidade explícita
- Consentimento informado; transparência
- Segurança por padrão (defense in depth)

---

## Controles (MVP → MRP)

- Trânsito: HTTPS/TLS
- Segredos: variáveis de ambiente; sem secrets no git
- Acesso: princípio do menor privilégio (IAM no MRP)
- Criptografia em repouso: bancos e storage (MRP)
- Logs: sem PII; mascaramento de dados sensíveis
- Auditoria: registro de ações administrativas

---

## Direitos do Titular

- Exportar dados sob demanda
- Solicitar anonimização/eliminação quando aplicável

---

## Ameaças e Mitigações (resumo)

- Interceptação de tráfego → TLS obrigatório; HSTS
- Exposição de segredos → env/secret manager; zero secrets no git
- Acesso indevido → IAM/least privilege; MFA em painéis
- Vazamento em logs → mascaramento e revisão de campos
- Abusos de API → rate limiting; HMAC de webhooks; allowlist de IPs quando possível
