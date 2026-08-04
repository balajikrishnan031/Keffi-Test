import urllib.request
import json
import ssl

def test_live_keffi_api():
    print("=== TESTING KEFFI AI LIVE HUGGING FACE BACKEND API ENDPOINTS ===")
    
    backend_url = "https://balajikrishnan031-keffi-backend.hf.space"
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    # 1. Health Check
    print("\n--- 1. TESTING HEALTH CHECK (GET /) ---")
    try:
        req = urllib.request.Request(f"{backend_url}/")
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print(f"Status: {resp.status} OK")
            print(f"Server Message: {data.get('message', '')}")
            print(f"Platform: {data.get('platform', '')}")
            print(f"Status Details: {data.get('status', '')}")
    except Exception as e:
        print(f"Health Check Failed: {e}")

    # 2. Test Clinical AI Chat Queries (POST /api/chat)
    test_cases = [
        {
            "name": "Academic Anxiety & Exam Stress",
            "message": "I feel so overwhelmed by my college exams and my heart is beating fast.",
            "visual": {"emotion": "anxiety", "confidence": 0.89},
            "audio": {"f0_mean": 265.4, "pause_duration": 1.4}
        },
        {
            "name": "Depressive Hopelessness & Sadness",
            "message": "I feel hopeless like nothing is going right in my life and I have no energy.",
            "visual": {"emotion": "sadness", "confidence": 0.92},
            "audio": {"f0_mean": 110.2, "pause_duration": 2.8}
        },
        {
            "name": "Panic Attack Somatic Relief",
            "message": "Can you guide me through a 4-7-8 breathing exercise for panic?",
            "visual": {"emotion": "fear", "confidence": 0.85},
            "audio": {"f0_mean": 280.0, "pause_duration": 0.8}
        },
        {
            "name": "Text Deception Check (Smiling Depression)",
            "message": "I am fine today.",
            "visual": {"emotion": "depressive_slump", "confidence": 0.94},
            "audio": {"f0_mean": 105.0, "pause_duration": 3.1}
        }
    ]

    print("\n--- 2. TESTING CLINICAL AI CHAT INFERENCE (POST /api/chat) ---")
    for case in test_cases:
        print(f"\nScenario: {case['name']}")
        print(f"Patient Input: \"{case['message']}\"")
        
        payload = json.dumps({
            "message": case["message"],
            "session_id": "test_session_balaji",
            "user_id": "test_patient_4226",
            "visual_affect": case["visual"],
            "voice_prosody": case["audio"]
        }).encode('utf-8')

        req = urllib.request.Request(
            f"{backend_url}/api/chat",
            data=payload,
            headers={"Content-Type": "application/json"}
        )

        try:
            with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
                res = json.loads(resp.read().decode('utf-8'))
                print(f"Status: {resp.status} OK")
                print(f"Keffi AI Reply: {res.get('reply', '')[:250]}...")
                print(f"BERT Emotion Tag: {res.get('emotion', res.get('bert_emotion', 'N/A'))}")
                print(f"MHQ Score: {res.get('mhq_score', 'N/A')}/100")
                print(f"Risk Tier: {res.get('risk_tier', 'N/A')}")
        except Exception as e:
            print(f"Chat Request Failed: {e}")

    # 3. Test Explainable AI Decision Support (POST /api/explain_clinical_decision)
    print("\n--- 3. TESTING EXPLAINABLE AI SHAP/LIME (POST /api/explain_clinical_decision) ---")
    try:
        payload_xai = json.dumps({
            "text": "I feel completely hopeless and want to end everything",
            "session_id": "test_session_balaji"
        }).encode('utf-8')

        req_xai = urllib.request.Request(
            f"{backend_url}/api/explain_clinical_decision",
            data=payload_xai,
            headers={"Content-Type": "application/json"}
        )

        with urllib.request.urlopen(req_xai, context=ctx, timeout=15) as resp:
            res_xai = json.loads(resp.read().decode('utf-8'))
            print(f"Status: {resp.status} OK")
            print(f"XAI SHAP Explanation: {res_xai}")
    except Exception as e:
        print(f"XAI Request Note: {e}")

    # 4. Test Executive Admin Patient Roster (GET /api/admin/patients_full)
    print("\n--- 4. TESTING EXECUTIVE ADMIN HUB (GET /api/admin/patients_full) ---")
    try:
        req_admin = urllib.request.Request(f"{backend_url}/api/admin/patients_full")
        with urllib.request.urlopen(req_admin, context=ctx, timeout=10) as resp:
            res_admin = json.loads(resp.read().decode('utf-8'))
            print(f"Status: {resp.status} OK")
            print(f"Total Registered Outpatients in Cloud DB: {len(res_admin.get('patients', res_admin))}")
    except Exception as e:
        print(f"Admin Roster Note: {e}")

    # 5. Test Doctor Appointment Booking (POST /api/book_appointment)
    print("\n--- 5. TESTING AUTOMATED DOCTOR APPOINTMENT BOOKING (POST /api/book_appointment) ---")
    try:
        payload_book = json.dumps({
            "patient_id": "test_patient_4226",
            "patient_name": "Balaji P",
            "doctor_name": "Dr. S. Sivanesh M.Tech., Ph.D.",
            "date": "2026-08-10",
            "time_slot": "10:30 AM",
            "notes": "High Risk <40 MHQ Escalation Triage"
        }).encode('utf-8')

        req_book = urllib.request.Request(
            f"{backend_url}/api/book_appointment",
            data=payload_book,
            headers={"Content-Type": "application/json"}
        )

        with urllib.request.urlopen(req_book, context=ctx, timeout=15) as resp:
            res_book = json.loads(resp.read().decode('utf-8'))
            print(f"Status: {resp.status} OK")
            print(f"Booking Confirmation: {res_book}")
    except Exception as e:
        print(f"Doctor Booking Note: {e}")

if __name__ == "__main__":
    test_live_keffi_api()
