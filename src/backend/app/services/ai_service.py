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

ai_service = AIService()
