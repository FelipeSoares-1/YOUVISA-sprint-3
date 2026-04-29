from __future__ import annotations
import uuid
import logging
from datetime import datetime, timezone
from dataclasses import dataclass, field

from app.database import interaction_repo
from .intent_classifier import IntentClassifierAgent
from .entity_extractor import EntityExtractorAgent
from .knowledge_agent import KnowledgeAgent
from .response_generator import ResponseGeneratorAgent

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# OrchestratorAgent
# Coordinates the multi-agent pipeline:
#   1. IntentClassifier  — what does the user want?
#   2. EntityExtractor   — what entities are mentioned?
#   3. KnowledgeAgent    — what data is relevant?
#   4. ResponseGenerator — build the final answer
#   5. InteractionLog    — persist the full trace to SQLite
# ---------------------------------------------------------------------------

@dataclass
class OrchestrationResult:
    response: str
    intent: str
    intent_confidence: float
    entities: dict
    agent_trace: list[dict]
    session_id: str
    doc_id: str | None


class OrchestratorAgent:
    def __init__(self, gemini_client=None):
        self._intent_classifier = IntentClassifierAgent()
        self._entity_extractor = EntityExtractorAgent(gemini_client=gemini_client)
        self._knowledge_agent = KnowledgeAgent()
        self._response_generator = ResponseGeneratorAgent(gemini_client=gemini_client)

    def process(
        self,
        user_message: str,
        session_id: str,
        chat_history: list[dict] | None = None,
        session_doc_id: str | None = None,
    ) -> OrchestrationResult:
        trace: list[dict] = []
        history = chat_history or []

        # --- Step 1: Classify intent ----------------------------------------
        intent_result = self._intent_classifier.classify(user_message)
        trace.append({
            "agent": "IntentClassifierAgent",
            "output": {
                "intent": intent_result.intent,
                "confidence": intent_result.confidence,
                "matched_keywords": intent_result.matched_keywords,
            }
        })
        logger.info(
            "Intent classified: %s (%.0f%%) session=%s",
            intent_result.intent, intent_result.confidence * 100, session_id
        )

        # --- Step 2: Extract entities ----------------------------------------
        entities = self._entity_extractor.extract(user_message, intent_result.intent)
        entities_dict = {
            "doc_id": entities.doc_id,
            "document_type": entities.document_type,
            "date_mentioned": entities.date_mentioned,
            "person_name": entities.person_name,
        }
        trace.append({
            "agent": "EntityExtractorAgent",
            "output": entities_dict,
        })

        # --- Step 3: Fetch knowledge -----------------------------------------
        knowledge = self._knowledge_agent.query(
            intent=intent_result.intent,
            entities=entities,
            session_doc_id=session_doc_id,
        )
        active_doc_id = knowledge.process["doc_id"] if knowledge.process else None
        trace.append({
            "agent": "KnowledgeAgent",
            "output": {
                "process_found": knowledge.process is not None,
                "doc_id": active_doc_id,
                "relevant_facts_count": len(knowledge.relevant_facts),
                "history_summary": knowledge.history_summary,
            }
        })

        # --- Step 4: Generate response ----------------------------------------
        response = self._response_generator.generate(
            user_message=user_message,
            intent=intent_result.intent,
            knowledge=knowledge,
            chat_history=history,
        )
        trace.append({
            "agent": "ResponseGeneratorAgent",
            "output": {"response_length": len(response), "guardrails_applied": True},
        })

        # --- Step 5: Persist interaction log ---------------------------------
        log_entry = {
            "id": str(uuid.uuid4()),
            "session_id": session_id,
            "doc_id": active_doc_id,
            "user_message": user_message,
            "detected_intent": intent_result.intent,
            "intent_confidence": intent_result.confidence,
            "entities": entities_dict,
            "agent_trace": trace,
            "response": response,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        try:
            interaction_repo.save(log_entry)
        except Exception as exc:
            logger.error("Failed to persist interaction log: %s", exc)

        return OrchestrationResult(
            response=response,
            intent=intent_result.intent,
            intent_confidence=intent_result.confidence,
            entities=entities_dict,
            agent_trace=trace,
            session_id=session_id,
            doc_id=active_doc_id,
        )
