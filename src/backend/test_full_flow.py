import requests
import time
import json

BASE_URL = "http://localhost:8000/api"

def log(section, msg):
    print(f"\n{'='*60}")
    print(f"  [{section}] {msg}")
    print(f"{'='*60}")

def pretty(data):
    print(json.dumps(data, indent=2, default=str, ensure_ascii=False))


def test_full_flow():
    # ========== STEP 1: Upload ==========
    log("STEP 1", "Enviando Documento via Upload...")
    with open("test_passport.txt", "w") as f:
        f.write("PASSPORT CONTENT - João Carlos da Silva - BR123456789")

    with open("test_passport.txt", "rb") as f:
        res = requests.post(f"{BASE_URL}/documents/upload", files={"file": ("test_passport.txt", f)})

    assert res.status_code == 200, f"Upload falhou: {res.text}"
    data = res.json()
    doc_id = data["id"]
    print(f"✅ Upload OK. doc_id = {doc_id}")
    print(f"   Status: {data['process']['status']}")
    print(f"   CV Fields: {data.get('cv_validation', {}).get('extracted_fields', {})}")
    print(f"   AI Class: {data.get('ai_classification', {})}")

    # ========== STEP 2: Verify list_documents returns doc_id ==========
    log("STEP 2", "Listando Documentos (deve ter 'id')...")
    res = requests.get(f"{BASE_URL}/documents/")
    docs = res.json()
    assert len(docs) > 0, "Lista vazia!"
    assert "id" in docs[-1], "'id' AUSENTE no GET /documents/ — BUG!"
    print(f"✅ list_documents OK. {len(docs)} processo(s). ID presente: {docs[-1]['id']}")

    # ========== STEP 3: Chat — Multiple Intents ==========
    log("STEP 3", "Testando Chatbot com múltiplas intenções...")

    intents_to_test = [
        ("Qual o status do meu processo?", "STATUS_QUERY"),
        ("Está faltando algum documento?", "MISSING_DOCS"),
        ("Qual o próximo passo?", "NEXT_STEP"),
        ("Quanto tempo demora?", "DEADLINE"),
        ("Olá, bom dia!", "GREETING"),
        ("Quero saber sobre vistos", "GENERAL"),
    ]

    for msg, expected_intent in intents_to_test:
        res = requests.post(f"{BASE_URL}/chat/", json={"message": msg, "user_id": "test_user"})
        assert res.status_code == 200, f"Chat falhou para '{msg}': {res.text}"
        chat_data = res.json()
        detected = chat_data.get("intent_detected", "???")
        print(f"  📨 \"{msg}\"")
        print(f"     Intent: {detected} (esperado: {expected_intent}) {'✅' if detected == expected_intent else '⚠️'}")
        print(f"     Resposta: {chat_data['response'][:100]}...")
        print()

    # ========== STEP 4: Admin Transitions ==========
    log("STEP 4", "Transição: EM_ANALISE → APROVADO...")
    res = requests.post(f"{BASE_URL}/documents/{doc_id}/transition?event=APPROVE&reason=Documentos+válidos")
    assert res.status_code == 200, f"Transição falhou: {res.text}"
    print(f"✅ Aprovado! Status: {res.json()['status']}")

    log("STEP 4b", "Transição: APROVADO → FINALIZADO...")
    res = requests.post(f"{BASE_URL}/documents/{doc_id}/transition?event=FINALIZE&reason=Processo+concluído")
    assert res.status_code == 200, f"Transição falhou: {res.text}"
    print(f"✅ Finalizado! Status: {res.json()['status']}")

    # ========== STEP 5: Invalid Transition (must fail) ==========
    log("STEP 5", "Testando transição INVÁLIDA (FINALIZADO → APPROVE)...")
    res = requests.post(f"{BASE_URL}/documents/{doc_id}/transition?event=APPROVE")
    assert res.status_code == 400, f"Deveria ter falhado! Status: {res.status_code}"
    print(f"✅ Transição inválida rejeitada corretamente: {res.json()['detail']}")

    # ========== STEP 6: History & Audit ==========
    log("STEP 6", "Verificando Histórico Auditável...")
    res = requests.get(f"{BASE_URL}/documents/{doc_id}/history")
    assert res.status_code == 200
    history = res.json()
    print(f"✅ Histórico com {len(history)} entradas:")
    for entry in history:
        print(f"   {entry['timestamp']} | {entry.get('from_status', '—')} → {entry['to_status']} | {entry['description']}")

    # ========== STEP 7: Notifications ==========
    log("STEP 7", "Verificando Notificações...")
    res = requests.get(f"{BASE_URL}/notifications/")
    assert res.status_code == 200
    notifs = res.json()
    print(f"✅ {len(notifs)} notificações registradas:")
    for n in notifs:
        print(f"   [{n['sent_at']}] {n['event_type']}: {n['message']}")

    # ========== STEP 8: Chat History ==========
    log("STEP 8", "Verificando Contexto de Conversa...")
    res = requests.get(f"{BASE_URL}/chat/history/test_user")
    assert res.status_code == 200
    chat_history = res.json()
    print(f"✅ Contexto armazenado: {len(chat_history)} mensagens")

    # ========== FINAL ==========
    log("RESULTADO", "🎉 TODOS OS TESTES PASSARAM! Sistema pronto para apresentação.")


if __name__ == "__main__":
    test_full_flow()
