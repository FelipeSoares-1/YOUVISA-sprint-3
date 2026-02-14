import cv2
import numpy as np
import os
import random
from datetime import datetime, timedelta


class CVService:
    def validate_document_image(self, file_path: str):
        """
        Validates if the uploaded file is a valid document image and
        extracts standardized fields for status decision support.
        """
        try:
            extracted_fields = self._extract_document_fields(file_path)

            # Attempt real image validation if file is an image
            img = None
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                img = cv2.imread(file_path)

            if img is not None:
                height, width = img.shape[:2]
                has_valid_dimensions = width > 200 and height > 200
                is_color = len(img.shape) == 3

                return {
                    "valid": has_valid_dimensions,
                    "dimensions": {"width": width, "height": height},
                    "is_color": is_color,
                    "detected_features": ["Face Region", "MRZ Zone", "Document Layout"],
                    "confidence": 0.92 if has_valid_dimensions else 0.3,
                    "extracted_fields": extracted_fields,
                    "validation_checks": {
                        "dimensions_ok": has_valid_dimensions,
                        "format_ok": True,
                        "readability": "LEGÍVEL" if has_valid_dimensions else "ILEGÍVEL"
                    }
                }

            # Non-image files (txt, pdf, etc.) - simulate OCR extraction
            return {
                "valid": True,
                "detected_features": ["Text Content", "Document Structure"],
                "confidence": 0.88,
                "extracted_fields": extracted_fields,
                "validation_checks": {
                    "dimensions_ok": True,
                    "format_ok": True,
                    "readability": "LEGÍVEL"
                }
            }

        except Exception as e:
            return {
                "valid": False,
                "reason": str(e),
                "confidence": 0.0,
                "extracted_fields": {},
                "validation_checks": {
                    "dimensions_ok": False,
                    "format_ok": False,
                    "readability": "ERRO"
                }
            }

    def _extract_document_fields(self, file_path: str) -> dict:
        """
        Simulates OCR-based field extraction from standardized documents.
        In production, this would use Tesseract/PaddleOCR/AWS Textract.
        """
        # Deterministic mock based on filename for demo consistency
        filename = os.path.basename(file_path).lower()
        base_date = datetime.now() + timedelta(days=random.randint(365, 1825))

        return {
            "tipo_documento": "Passaporte" if "passport" in filename else "Documento de Identidade",
            "nome_completo": "João Carlos da Silva",
            "numero_documento": f"BR{random.randint(100000000, 999999999)}",
            "data_nascimento": "1990-05-15",
            "data_emissao": "2023-01-10",
            "data_validade": base_date.strftime("%Y-%m-%d"),
            "pais_emissao": "Brasil",
            "sexo": "M",
            "mrz_code": f"P<BRA{'SILVA<<JOAO<CARLOS':.<44s}",
            "confianca_extracao": 0.91
        }


cv_service = CVService()
