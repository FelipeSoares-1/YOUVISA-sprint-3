import logging
import re

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# ResponseGeneratorAgent
# Builds a rich prompt from KnowledgeContext + intent + chat history and
# calls Gemini. Applies guardrails before returning. Falls back to mock.
# ---------------------------------------------------------------------------

BLOCKED_PHRASES = [
    "em breve será aprovado", "com certeza será aprovado", "garanto a aprovação",
    "em x dias", "ficará pronto em", "prometo que", "prometo o prazo",
    "tenho certeza que será aprovado", "100% aprovado",
    "não se preocupe, será aprovado",
]

SAFE_FALLBACK = (
    "Entendo sua preocupação. Para obter informações precisas sobre seu processo, "
    "recomendo acompanhar as atualizações de status no painel ou contatar nossa equipe diretamente. "
    "Posso ajudar com mais alguma dúvida sobre a documentação?"
)

SYSTEM_INSTRUCTION = """Você é Valéria, consultora especialista da YOUVISA — plataforma de processos consulares.

REGRAS ABSOLUTAS:
• Nunca invente prazos, datas ou garantias de aprovação
• Nunca afirme que um processo "será aprovado"
• Nunca forneça conselhos jurídicos
• Nunca responda perguntas fora do escopo consular
• Se não souber, diga que vai verificar com a equipe
• Seja empática, precisa e objetiva

FORMATAÇÃO — OBRIGATÓRIO:
• Responda SOMENTE em texto simples, sem markdown
• Não use asteriscos, underlines, hashtags ou qualquer símbolo de formatação
• Para listas use hífen simples: "- item"
• Máximo 4 frases ou 4 itens de lista por resposta
• Não comece a resposta com "Valéria:"

ESCOPO: Dúvidas sobre documentação, status de processo, próximos passos e orientações gerais de visto/passaporte.
"""

_MOCK_RESPONSES: dict[str, str] = {
    "STATUS_QUERY": (
        "Seu processo está em acompanhamento pela nossa equipe. "
        "Você pode ver o status atualizado em tempo real no Painel de Controle — "
        "ele mostra cada etapa e o histórico completo. "
        "Assim que houver uma mudança, você receberá notificação automática. 😊"
    ),
    "MISSING_DOCS": (
        "Para saber exatamente o que enviar, verifique seu processo no Painel de Controle. "
        "Se o status estiver como 'Pendência de Docs', aparecerá o que está faltando. "
        "Em geral, precisamos de: passaporte válido, comprovante de residência e foto recente. "
        "Posso detalhar algum documento específico?"
    ),
    "NEXT_STEP": (
        "O próximo passo depende do seu status atual. Se estiver 'Em Análise', aguarde a revisão da equipe. "
        "Se estiver 'Pendente', envie os documentos solicitados pelo painel. "
        "Após aprovação, receberá instruções para emissão do visto. "
        "Quer que eu explique alguma etapa específica?"
    ),
    "DEADLINE": (
        "Prazos consulares variam bastante — dependem do país, do tipo de visto e da demanda atual do consulado. "
        "A YOUVISA não fornece estimativas para não criar expectativas incorretas. "
        "Recomendo acompanhar o status pelo painel e aguardar a comunicação oficial."
    ),
    "APPROVAL_STATUS": (
        "O resultado do seu processo será comunicado via e-mail e SMS assim que sair. "
        "Você também pode acompanhar no painel — quando o status mudar para 'Aprovado' ou 'Reprovado', "
        "aparecerá automaticamente. Precisa de mais alguma informação?"
    ),
    "DOCUMENT_INFO": (
        "Claro! Posso ajudar com informações sobre documentos. "
        "Os mais comuns são: passaporte (validade mínima de 6 meses), "
        "comprovante de residência recente, fotos 3x4 e comprovante de renda. "
        "Qual documento específico você quer saber mais?"
    ),
    "GREETING": (
        "Olá! Seja bem-vindo(a) à YOUVISA! 😊 "
        "Sou a Valéria, sua consultora virtual. "
        "Estou aqui para ajudar com dúvidas sobre seu processo consular, "
        "documentos necessários e próximos passos. Como posso te ajudar hoje?"
    ),
    "HELP": (
        "Claro, estou aqui! Posso te ajudar com:\n"
        "• Status e andamento do seu processo\n"
        "• Quais documentos enviar\n"
        "• Próximos passos após cada etapa\n"
        "• Informações sobre prazos e aprovação\n\n"
        "O que você gostaria de saber?"
    ),
    "GENERAL": (
        "Entendi! Sou especializada em processos consulares e posso ajudar com "
        "status, documentação e orientações sobre seu visto. "
        "Se ainda não tem um processo ativo, comece enviando um documento no Painel de Controle. "
        "O que posso fazer por você?"
    ),
}


class ResponseGeneratorAgent:
    """
    Generates contextual responses using Gemini with prompt engineering.
    Applies deterministic guardrails post-generation.
    Falls back to mock responses when Gemini is unavailable.
    """

    def __init__(self, gemini_client=None, model: str = "gemini-2.5-flash"):
        self._client = gemini_client
        self._model = model
        self._mock = gemini_client is None
        if self._mock:
            logger.info("ResponseGeneratorAgent running in mock mode")

    def generate(
        self,
        user_message: str,
        intent: str,
        knowledge,
        chat_history: list[dict],
    ) -> str:
        if self._mock:
            return _MOCK_RESPONSES.get(intent, _MOCK_RESPONSES["GENERAL"])

        try:
            return self._gemini_generate(user_message, intent, knowledge, chat_history)
        except Exception as exc:
            logger.warning("Gemini generation failed, using mock: %s", exc)
            return _MOCK_RESPONSES.get(intent, _MOCK_RESPONSES["GENERAL"])

    # ------------------------------------------------------------------
    def _gemini_generate(self, user_message, intent, knowledge, chat_history) -> str:
        from google.genai import types

        context_block = self._build_context(intent, knowledge)
        history_block = self._format_history(chat_history)

        prompt = (
            f"{context_block}\n\n"
            f"{history_block}\n\n"
            f"Intenção detectada: {intent}\n"
            f"Usuário: {user_message}\n"
            f"Valéria:"
        )

        response = self._client.models.generate_content(
            model=self._model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.4,
                max_output_tokens=400,
            )
        )
        text = response.text.strip()
        return self._apply_guardrails(text)

    def _build_context(self, intent: str, knowledge) -> str:
        if not knowledge or not knowledge.process:
            return (
                "Contexto: O usuário ainda não possui um processo ativo na plataforma.\n"
                "Instrução: Seja acolhedora e útil. Explique brevemente como funciona a YOUVISA "
                "e oriente o usuário a fazer o upload de um documento no Painel de Controle "
                "para iniciar seu processo. Responda de forma empática e direta à pergunta feita."
            )

        facts = "\n".join(f"• {f}" for f in knowledge.relevant_facts) if knowledge.relevant_facts else "• Nenhum fato específico para esta intenção."
        return (
            f"Contexto do processo:\n"
            f"{knowledge.history_summary}\n\n"
            f"Fatos relevantes para intenção '{intent}':\n{facts}"
        )

    def _format_history(self, history: list[dict]) -> str:
        if not history:
            return "Histórico de conversa: (início da sessão)"
        lines = []
        for msg in history[-8:]:
            role = "Usuário" if msg.get("role") == "user" else "Valéria"
            lines.append(f"{role}: {msg.get('content', '')}")
        return "Histórico recente:\n" + "\n".join(lines)

    def _strip_markdown(self, text: str) -> str:
        """Remove markdown symbols Gemini may produce despite instructions."""
        # Bold and italic: **text**, *text*, __text__, _text_
        text = re.sub(r'\*{1,3}([^*]+)\*{1,3}', r'\1', text)
        text = re.sub(r'_{1,2}([^_]+)_{1,2}', r'\1', text)
        # Headers: ## Title → Title
        text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
        # Bullet markers: "*   item" or "* item" → "- item"
        text = re.sub(r'^\*{1,2}\s+', '- ', text, flags=re.MULTILINE)
        # Inline code: `text` → text
        text = re.sub(r'`([^`]+)`', r'\1', text)
        # Trailing spaces and multiple blank lines
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()

    def _apply_guardrails(self, text: str) -> str:
        text = self._strip_markdown(text)
        lower = text.lower()
        for phrase in BLOCKED_PHRASES:
            if phrase in lower:
                logger.info("Guardrail triggered: blocked phrase '%s'", phrase)
                return SAFE_FALLBACK
        return text
