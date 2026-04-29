from __future__ import annotations
import logging
from dataclasses import dataclass, field
from app.database import process_repo
from app.agents.knowledge_base import get_kb_facts

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# KnowledgeAgent
# Retrieves structured context from the database based on intent + entities.
# Isolates all DB access from the response generator.
# ---------------------------------------------------------------------------

@dataclass
class KnowledgeContext:
    process: dict | None = None
    history_summary: str = ""
    relevant_facts: list[str] = field(default_factory=list)


_STATUS_LABELS = {
    "RECEBIDO": "recebido e aguardando análise",
    "EM_ANALISE": "em análise pela equipe técnica",
    "PENDENTE_DOCS": "pendente — documentação adicional necessária",
    "APROVADO": "aprovado",
    "REPROVADO": "reprovado",
    "FINALIZADO": "finalizado com sucesso",
}

_NEXT_STEPS = {
    "RECEBIDO": "Aguardar o início da análise. Nenhuma ação necessária por ora.",
    "EM_ANALISE": "Acompanhar o status. A equipe está revisando seus documentos.",
    "PENDENTE_DOCS": "Enviar os documentos solicitados o quanto antes para retomar o processo.",
    "APROVADO": "O processo está aprovado e será finalizado em breve.",
    "REPROVADO": "Entrar em contato com a equipe para verificar os motivos e possibilidade de recurso.",
    "FINALIZADO": "O processo está concluído. Guarde os comprovantes.",
}

_MISSING_DOCS_BY_STATUS = {
    "PENDENTE_DOCS": [
        "Documento de identidade (frente e verso)",
        "Comprovante de residência atualizado (últimos 3 meses)",
        "Foto 3x4 recente com fundo branco",
    ],
}


class KnowledgeAgent:
    """
    Queries the database and builds a KnowledgeContext relevant to the
    detected intent. Decouples data retrieval from response generation.
    """

    def query(self, intent: str, entities, session_doc_id: str | None = None) -> KnowledgeContext:
        ctx = KnowledgeContext()

        doc_id = (entities.doc_id if entities else None) or session_doc_id
        process = None

        if doc_id:
            process = process_repo.get(doc_id)

        if not process:
            process = process_repo.get_latest()

        facts: list[str] = []

        if process:
            ctx.process = process
            status = process.get("status", "RECEBIDO")
            label = _STATUS_LABELS.get(status, status)

            ctx.history_summary = (
                f"Processo {process['doc_id'][:8]}… — arquivo: {process['filename']} — "
                f"status atual: {label} — "
                f"{len(process.get('history', []))} evento(s) registrado(s)."
            )

            if intent in ("STATUS_QUERY", "APPROVAL_STATUS"):
                facts.append(f"Status atual: {label}.")
                history = process.get("history", [])
                if len(history) > 1:
                    last = history[-1]
                    facts.append(
                        f"Última atualização: {last.get('description', '')} "
                        f"em {last['timestamp'][:10]}."
                    )

            if intent == "NEXT_STEP":
                facts.append(f"Próximo passo recomendado: {_NEXT_STEPS.get(status, 'Aguardar atualização.')}")

            if intent == "MISSING_DOCS":
                missing = _MISSING_DOCS_BY_STATUS.get(status, [])
                if missing:
                    facts.append("Documentos pendentes: " + "; ".join(missing))
                else:
                    facts.append("Nenhuma pendência documental identificada no status atual.")

            if intent == "DEADLINE":
                facts.append(
                    "Prazos variam conforme o consulado e o tipo de visto. "
                    "O sistema não fornece estimativas automáticas de prazo."
                )

        # Always append KB facts — available even without an active process
        facts.extend(get_kb_facts(intent))

        ctx.relevant_facts = facts
        return ctx
