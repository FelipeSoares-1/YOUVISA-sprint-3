from openai import OpenAI
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

# Deterministic guardrail: words/phrases the AI must NEVER output
BLOCKED_PHRASES = [
    "amanhã", "em breve será aprovado", "com certeza",
    "garanto", "prazo de", "em X dias", "ficará pronto em",
    "não se preocupe, será aprovado", "100% aprovado",
    "dentro de 24 horas", "dentro de 48 horas",
    "prometo", "tenho certeza"
]

# Pre-approved fallback messages (safe, deterministic)
SAFE_FALLBACK = {
    "RECEBIDO": "Seu documento foi recebido e aguarda análise. Você será notificado assim que houver atualização.",
    "EM_ANALISE": "Seu documento está em análise pela equipe técnica. Acompanhe pelo painel para atualizações.",
    "PENDENTE_DOCS": "Existe uma pendência na sua documentação. Por favor, verifique e reenvie pelo painel.",
    "APROVADO": "Sua documentação foi aprovada. Aguarde os próximos passos sobre a emissão do visto.",
    "REPROVADO": "Sua documentação foi reprovada. Entre em contato com o suporte para mais informações.",
    "FINALIZADO": "Seu processo foi concluído com sucesso. Obrigado por usar a YOUVISA!"
}


def apply_guardrails(text: str, status: str) -> str:
    """
    Deterministic output filter.
    If the AI generates any blocked phrase, replace with a safe pre-approved message.
    """
    text_lower = text.lower()
    for phrase in BLOCKED_PHRASES:
        if phrase.lower() in text_lower:
            return SAFE_FALLBACK.get(status, "Não posso fornecer essa informação no momento.")
    return text


class AIService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None
        self.mock_mode = not bool(self.api_key)

    def analyze_document(self, text: str):
        if self.mock_mode:
            return {
                "classification": "Passaporte (Simulado)",
                "confidence": 0.95,
                "extracted_fields": {
                    "tipo_documento": "Passaporte",
                    "nome": "João da Silva",
                    "numero_documento": "BR123456789",
                    "data_validade": "2028-12-15",
                    "pais_emissao": "Brasil"
                },
                "summary": "Documento de identificação internacional válido.",
                "action_required": "Validar data de validade e conferir foto."
            }

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": (
                        "You are a document analysis assistant. "
                        "Extract: document type, holder name, document number, "
                        "expiry date, issuing country. Return JSON."
                    )},
                    {"role": "user", "content": f"Analyze this document text: {text[:1000]}"}
                ]
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {"error": str(e), "classification": "Unknown", "confidence": 0.0}

    def explain_status(self, status: str, context: list):
        if self.mock_mode:
            explanations = {
                "RECEBIDO": (
                    "📩 Recebemos seu documento e ele está na fila para análise inicial. "
                    "Nossa equipe verificará a integridade e legibilidade do arquivo."
                ),
                "EM_ANALISE": (
                    "🔍 Nossa equipe e sistemas inteligentes estão validando seus dados neste momento. "
                    "Estamos conferindo a autenticidade do documento e extraindo as informações necessárias."
                ),
                "PENDENTE_DOCS": (
                    "⚠️ Identificamos que falta uma página ou o documento está ilegível. "
                    "Por favor, reenvie a documentação completa pelo painel."
                ),
                "APROVADO": (
                    "✅ Parabéns! Sua documentação foi aprovada após análise técnica. "
                    "O próximo passo é aguardar a emissão do visto."
                ),
                "REPROVADO": (
                    "❌ Infelizmente, identificamos inconsistências graves na documentação. "
                    "Entre em contato com o suporte para entender os motivos e possíveis ações."
                ),
                "FINALIZADO": (
                    "🎉 Seu processo foi concluído com sucesso! "
                    "Agradecemos por utilizar a YOUVISA."
                ),
            }
            return explanations.get(status, "Status desconhecido. Contate o suporte.")

        guardrails_prompt = """
        REGRAS OBRIGATÓRIAS (VOCE DEVE SEGUIR SEM EXCEÇÃO):
        1. Você é o assistente virtual da YOUVISA.
        2. NUNCA invente prazos (ex: "ficará pronto amanhã").
        3. NUNCA garanta aprovação se o status NÃO for "APROVADO".
        4. NUNCA recomende ações legais ou jurídicas.
        5. Use linguagem clara, empática e profissional.
        6. Baseie-se SOMENTE nos dados fornecidos no contexto.
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": guardrails_prompt},
                    {"role": "user", "content": (
                        f"O status do processo é '{status}'. "
                        f"O histórico é: {json.dumps(context, default=str)}. "
                        "Explique para o cliente em português o que isso significa e qual o próximo passo."
                    )}
                ]
            )
            raw_response = response.choices[0].message.content
            # Apply deterministic guardrails filter
            return apply_guardrails(raw_response, status)
        except Exception:
            return SAFE_FALLBACK.get(status, "Não foi possível gerar a explicação no momento.")


ai_service = AIService()
