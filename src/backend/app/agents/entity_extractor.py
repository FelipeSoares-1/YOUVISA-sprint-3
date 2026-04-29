from __future__ import annotations
import re
import json
import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# EntityExtractorAgent
# Two-pass extraction: regex (fast, deterministic) then Gemini structured
# output for anything not caught by patterns. Falls back gracefully.
# ---------------------------------------------------------------------------

@dataclass
class ExtractedEntities:
    doc_id: str | None = None
    document_type: str | None = None
    date_mentioned: str | None = None
    person_name: str | None = None
    raw: dict = field(default_factory=dict)


_UUID_RE = re.compile(
    r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", re.I
)
_DOC_TYPES = {
    "passaporte": "Passaporte",
    "passport": "Passaporte",
    "rg": "RG",
    "cnh": "CNH",
    "cpf": "CPF",
    "visto": "Visto",
    "visa": "Visto",
    "certid": "Certidão",
    "comprovante": "Comprovante",
}
_DATE_RE = re.compile(r"\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4}")


class EntityExtractorAgent:
    """
    Extracts structured entities from user messages.
    Regex pass is always applied; Gemini pass is optional and used when
    the regex pass leaves entities empty and a Gemini client is available.
    """

    def __init__(self, gemini_client=None, model: str = "gemini-2.5-flash"):
        self._client = gemini_client
        self._model = model

    def extract(self, message: str, intent: str) -> ExtractedEntities:
        entities = self._regex_pass(message)

        # Only invoke Gemini if regex came up empty and client is available
        if self._client and not any([entities.doc_id, entities.document_type, entities.date_mentioned]):
            entities = self._gemini_pass(message, intent, entities)

        return entities

    # ------------------------------------------------------------------
    def _regex_pass(self, message: str) -> ExtractedEntities:
        text = message.lower()
        entities = ExtractedEntities()

        uuid_match = _UUID_RE.search(message)
        if uuid_match:
            entities.doc_id = uuid_match.group(0)

        for keyword, doc_type in _DOC_TYPES.items():
            if keyword in text:
                entities.document_type = doc_type
                break

        date_match = _DATE_RE.search(message)
        if date_match:
            entities.date_mentioned = date_match.group(0)

        return entities

    def _gemini_pass(self, message: str, intent: str, base: ExtractedEntities) -> ExtractedEntities:
        try:
            from google.genai import types

            prompt = (
                f"Extract entities from this user message (intent={intent}).\n"
                f"Message: \"{message}\"\n"
                "Return JSON with keys: doc_id (string|null), document_type (string|null), "
                "date_mentioned (string|null), person_name (string|null). "
                "Use null for missing fields. No markdown."
            )
            response = self._client.models.generate_content(
                model=self._model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.0,
                )
            )
            data = json.loads(response.text)
            base.doc_id = data.get("doc_id") or base.doc_id
            base.document_type = data.get("document_type") or base.document_type
            base.date_mentioned = data.get("date_mentioned") or base.date_mentioned
            base.person_name = data.get("person_name")
            base.raw = data
        except Exception as exc:
            logger.warning("EntityExtractor Gemini pass failed: %s", exc)
        return base
