import requests
import time
import os
import json

BASE_URL = "http://localhost:8000/api"
FILE_PATH = "test_passport.txt"

def log(step, msg):
    print(f"\n[STEP {step}] {msg}")

def test_flow():
    # Create dummy file
    with open(FILE_PATH, "w") as f:
        f.write("DUMMY PASSPORT CONTENT")

    try:
        # 1. Upload
        log(1, "Enviando Documento...")
        with open(FILE_PATH, "rb") as f:
            files = {"file": (FILE_PATH, f)}
            res = requests.post(f"{BASE_URL}/documents/upload", files=files)
            if res.status_code != 200:
                print(f"❌ Upload falhou: {res.text}")
                return
            data = res.json()
            doc_id = data["id"]
            print(f"✅ Upload OK. ID: {doc_id}")

        # debug: check list
        res_list = requests.get(f"{BASE_URL}/documents/")
        print(f"   [DEBUG] Documentos no Backend: {len(res_list.json())}")

        # 2. Chat: Check Initial Status
        log(2, "Testando Chat (Esperado: RECEBIDO/Análise)...")
        chat_payload = {"message": "Qual o status do meu processo?"}
        chat_res = requests.post(f"{BASE_URL}/chat/", json=chat_payload)
        resp_text = chat_res.json()['response']
        print(f"🤖 Bot: {resp_text}")
        
        if "processo" not in resp_text and "status" not in resp_text and "Recebemos" not in resp_text:
             print("⚠️  Aviso: Resposta do bot pode estar genérica. Verifique se o singleton está funcionando.")

        # 3. Transition to Analysis
        log(3, "Admin: Avançando para EM_ANALISE...")
        res_trans = requests.post(f"{BASE_URL}/documents/{doc_id}/transition?event=START_ANALYSIS")
        print(f"   Status Novo: {res_trans.json().get('status')}")
        
        # 4. Chat: Check Analysis Status
        log(4, "Testando Chat (Esperado: EM_ANALISE)...")
        chat_res = requests.post(f"{BASE_URL}/chat/", json={"message": "Como ta o status?"})
        print(f"🤖 Bot: {chat_res.json()['response']}")
        
        # 5. Transition to Approved
        log(5, "Admin: Aprovando Documentação...")
        res_trans = requests.post(f"{BASE_URL}/documents/{doc_id}/transition?event=APPROVE")
        print(f"   Status Novo: {res_trans.json().get('status')}")

        # 6. Chat: Check Final Status
        log(6, "Testando Chat (Esperado: APROVADO)...")
        chat_res = requests.post(f"{BASE_URL}/chat/", json={"message": "Fui aprovado?"})
        print(f"🤖 Bot: {chat_res.json()['response']}")
        
        print("\n✅ Fluxo verificado. (Confira as respostas do bot acima)")
        
    finally:
        if os.path.exists(FILE_PATH):
            os.remove(FILE_PATH)

if __name__ == "__main__":
    test_flow()
