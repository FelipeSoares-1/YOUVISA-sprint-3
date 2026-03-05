from google import genai
from google.genai import types
from pydantic import BaseModel, Field
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

class ExtractedFields(BaseModel):
    tipo_documento: str = Field(description="O tipo do documento")
    nome: str = Field(description="Nome completo do titular")
    numero_documento: str = Field(description="Número de identificação do documento")
    data_validade: str = Field(description="Data de validade do documento")
    pais_emissao: str = Field(description="País emissor do documento")

class DocumentAnalysis(BaseModel):
    classification: str = Field(description="A classificação do documento")
    confidence: float = Field(description="O nível de confiança da extração (0 a 1)")
    extracted_fields: ExtractedFields
    summary: str = Field(description="Um breve sumário sobre o documento")
    action_required: str = Field(description="Opcional. Ação requerida caso o documento exija atenção especial")

class AIService:
    def __init__(self):
        # O SDK google-genai procura automaticamente pela variável GEMINI_API_KEY
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client() if self.api_key else None
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
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=f"Analyze this document text: {text[:1000]}",
                config=types.GenerateContentConfig(
                    system_instruction=(
                        "You are a document analysis assistant. "
                        "Extract: document type, holder name, document number, "
                        "expiry date, issuing country. Return JSON."
                    ),
                    response_mime_type="application/json",
                    response_schema=DocumentAnalysis,
                    temperature=0.1,
                ),
            )
            return json.loads(response.text)
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
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=(
                    f"O status do processo é '{status}'. "
                    f"O histórico é: {json.dumps(context, default=str)}. "
                    "Explique para o cliente em português o que isso significa e qual o próximo passo."
                ),
                config=types.GenerateContentConfig(
                    system_instruction=guardrails_prompt,
                    temperature=0.7,
                )
            )
            raw_response = response.text
            # Apply deterministic guardrails filter
            return apply_guardrails(raw_response, status)
        except Exception:
            return SAFE_FALLBACK.get(status, "Não foi possível gerar a explicação no momento.")


ai_service = AIService()
