import requests
import json
import time

BASE_URL = "http://localhost:8000/api"

def run_verification():
    print("--- 1. Upload Document ---")
    files = {'file': ('test_doc.txt', 'Conteudo teste para sprint 3')}
    try:
        res = requests.post(f"{BASE_URL}/documents/upload", files=files)
        if res.status_code != 200:
            print(f"FAILED UPLOAD: {res.text}")
            return
        data = res.json()
        doc_id = data['id']
        print(f"SUCCESS: Uploaded doc_id={doc_id}")
        
        print("\n--- 2. Check Initial Status ---")
        res = requests.get(f"{BASE_URL}/documents/")
        procs = res.json()
        print(f"Processes found: {len(procs)}")
        print(f"Current Status: {procs[-1]['status']}") # Should be RECEBIDO or EM_ANALISE (if auto transitioned)

        print("\n--- 3. Simulate Analysis Transition ---")
        # In the code, upload triggers START_ANALYSIS automatically.
        # Let's transition to APPROVE manually.
        res = requests.post(f"{BASE_URL}/documents/{doc_id}/transition?event=APPROVE")
        if res.status_code == 200:
             print(f"SUCCESS: Transitioned to {res.json()['status']}")
        else:
             print(f"FAILED TRANSITION: {res.text}")

        print("\n--- 4. Chat Status Query ---")
        chat_payload = {"message": "Qual o status do meu processo?", "user_id": "test_user"}
        res = requests.post(f"{BASE_URL}/chat/", json=chat_payload)
        print(f"Chat Response: {res.json()['response']}")
        
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    run_verification()
