from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()

class AIService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None
        self.mock_mode = not bool(self.api_key)

    def analyze_document(self, text: str):
        """
        Analyzes the document text to classify it and extract key info.
        """
        if self.mock_mode:
            return {
                "classification": "Passaporte (Simulado)",
                "confidence": 0.98,
                "summary": "Documento de identificação internacional. (IA Mock)",
                "action_required": "Validar data de validade"
            }
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a document analysis assistant. Classify the document and extract key info in JSON format."},
                    {"role": "user", "content": f"Analyze this text: {text[:1000]}"}
                ]
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {"error": str(e), "classification": "Unknown", "confidence": 0.0}

    def explain_status(self, status: str, context: dict):
        """
        Generates a user-friendly explanation of the current status using Guardrails.
        """
        if self.mock_mode:
            explanations = {
                "RECEBIDO": "Recebemos seu documento e ele está na fila para análise inicial.",
                "EM_ANALISE": "Nossa equipe e sistemas inteligentes estão validando seus dados neste momento.",
                "PENDENTE_DOCS": "Identificamos que falta uma página ou o documento está ilegível. Por favor, reenvie.",
                "APROVADO": "Parabéns! Sua documentação foi aprovada. O próximo passo é a emissão do visto.",
                "REPROVADO": "Infelizmente, identificamos inconsistências graves. Entre em contato com o suporte."
            }
            return explanations.get(status, "Status desconhecido.")

        guardrails = """
        IMPORTANTE:
        1. Você é um assistente virtual da YOUVISA.
        2. NUNCA invente prazos exatos (ex: "ficará pronto amanhã") a menos que esteja no contexto.
        3. NUNCA garanta aprovação se o status não for "APROVADO".
        4. Use linguagem clara, empática e profissional.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": guardrails},
                    {"role": "user", "content": f"O status do processo é '{status}'. O histórico é: {context}. Explique para o cliente o que isso significa e qual o próximo passo."}
                ]
            )
            return response.choices[0].message.content
        except Exception:
            return "Não foi possível gerar a explicação no momento."

ai_service = AIService()
