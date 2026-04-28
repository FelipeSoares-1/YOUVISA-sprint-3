import re
from dataclasses import dataclass

# ---------------------------------------------------------------------------
# IntentClassifierAgent
# Rule-based classifier using keyword patterns and confidence scoring.
# Deterministic, zero-latency, zero API cost — appropriate for production.
# ---------------------------------------------------------------------------

@dataclass
class IntentResult:
    intent: str
    confidence: float
    matched_keywords: list[str]


_INTENT_PATTERNS: list[tuple[str, list[str], float]] = [
    # (intent_name, keywords, base_confidence)
    ("STATUS_QUERY", [
        r"status", r"andamento", r"como est[aá]", r"em que p[eé]",
        r"o que aconteceu", r"atualiza[çc][aã]o", r"progresso",
        r"fase", r"situa[çc][aã]o", r"processando",
        r"meu processo", r"meus processos", r"ver processo",
        r"acompanhar", r"onde est[aá]", r"saber sobre",
    ], 0.90),

    ("MISSING_DOCS", [
        r"falta", r"pendente", r"pendência", r"preciso enviar",
        r"o que falta", r"documentos faltando", r"incompleto",
        r"documento obrigat[oó]rio", r"anexo", r"comprovante",
        r"tem que mandar", r"preciso mandar", r"o que mandar",
        r"o que enviar", r"quais documentos", r"que documentos",
        r"o que preciso", r"o que é necessário",
    ], 0.90),

    ("NEXT_STEP", [
        r"próximo passo", r"o que fazer", r"como prosseguir",
        r"agora o que", r"depois", r"seguinte", r"continuar",
        r"próxima etapa", r"próximo", r"devo fazer",
        r"como faço", r"o que devo", r"como proceder",
    ], 0.88),

    ("DEADLINE", [
        r"prazo", r"quanto tempo", r"demora", r"quando fica pronto",
        r"data prevista", r"tempo de espera", r"dias?",
        r"semanas?", r"quando ser[aá]", r"quanto demora",
        r"quando termina", r"quando sai", r"previs[aã]o",
    ], 0.88),

    ("APPROVAL_STATUS", [
        r"aprovad[ao]", r"reprovad[ao]", r"negad[ao]", r"deferid[ao]",
        r"indeferid[ao]", r"deferiment[ao]", r"aprova[çc][aã]o",
        r"resultado", r"decis[aã]o", r"foi aprovado", r"vou ser aprovado",
        r"chances", r"vai aprovar",
    ], 0.90),

    ("DOCUMENT_INFO", [
        r"passaporte", r"visto", r"\brg\b", r"\bcpf\b", r"\bcnh\b",
        r"certid[aã]o", r"comprovante de resid[eê]ncia",
        r"extrato", r"foto", r"documento de identidade",
        r"validade", r"valid[ao]", r"documento",
        r"\betias\b", r"\beta\b", r"autoriza[çc][aã]o eletr[oô]nica",
        r"reino unido", r"schengen", r"ds-?160", r"casv",
        r"b1", r"b2", r"b1/b2", r"taxa consular", r"mrv",
        r"visto americano", r"visto europeu", r"visto de turismo",
    ], 0.85),

    ("GREETING", [
        r"^ol[aá]", r"^oi\b", r"^bom dia", r"^boa tarde",
        r"^boa noite", r"tudo bem", r"tudo certo", r"^e a[ií]",
        r"^ei\b", r"^hey\b",
    ], 0.95),

    ("HELP", [
        r"ajuda", r"help", r"como funciona", r"n[aã]o entendo",
        r"o que [eé] isso", r"explica", r"pode me explicar",
        r"como usar", r"me ajuda", r"me ajude", r"me orienta",
        r"n[aã]o sei", r"perdid[ao]",
    ], 0.85),
]

_GENERAL_INTENT = "GENERAL"


class IntentClassifierAgent:
    """
    Classifies user messages into predefined intents using regex pattern matching.
    Returns confidence based on number of matched keywords relative to pattern count.
    """

    def classify(self, message: str) -> IntentResult:
        text = message.lower().strip()
        best_intent = _GENERAL_INTENT
        best_confidence = 0.30  # floor for GENERAL
        best_keywords: list[str] = []

        for intent, patterns, base_conf in _INTENT_PATTERNS:
            matched = [p for p in patterns if re.search(p, text)]
            if not matched:
                continue

            # Confidence scales with keyword density; caps at base_conf
            ratio = min(len(matched) / max(len(patterns) * 0.3, 1), 1.0)
            confidence = round(base_conf * (0.7 + 0.3 * ratio), 3)

            if confidence > best_confidence:
                best_intent = intent
                best_confidence = confidence
                best_keywords = matched

        return IntentResult(
            intent=best_intent,
            confidence=best_confidence,
            matched_keywords=best_keywords,
        )
