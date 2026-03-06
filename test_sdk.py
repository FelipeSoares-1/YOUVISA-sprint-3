import os
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
import json
from dotenv import load_dotenv

load_dotenv()

class ExtractedFields(BaseModel):
    tipo_documento: str = Field(description="O tipo do documento")
    nome: str = Field(description="Nome completo do titular")
    data_validade: str = Field(description="Data de validade do documento")

class DocumentAnalysis(BaseModel):
    classification: str = Field(description="A classificação do documento")
    confidence: float = Field(description="O nível de confiança da extração (0 a 1)")
    extracted_fields: ExtractedFields
    summary: str = Field(description="Um breve sumário sobre o documento")

client = genai.Client()

with open("test_img.jpg", "wb") as f:
    f.write(b"fake image data") # We'll just run it to see if it syntax checks

try:
    with open("test_img.jpg", "rb") as f:
        doc_bytes = f.read()
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[
            "Extract details from this document.",
            types.Part.from_bytes(data=doc_bytes, mime_type="image/jpeg",)
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=DocumentAnalysis,
            temperature=0.1,
        )
    )
    print("Success syntax check!")
except Exception as e:
    print("ERROR:", str(e))
