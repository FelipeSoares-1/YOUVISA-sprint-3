# Validação de Documentos (Visão Computacional)

## Objetivo
Auxiliar na verificação básica de documentos (ex.: passaporte) para reduzir erros de digitação e fraudes óbvias.

---

## Pipeline (MRP)

1) Pré-processamento (OpenCV): rotação, contraste, corte
2) Qualidade mínima (resolução, foco)
3) OCR (Tesseract) para extrair campos
4) Regras de consistência (formato, MRZ quando aplicável)
5) Sinalização de confiabilidade e orientação ao usuário

Observação: decisões críticas devem manter validação humana.

