import urllib.request
import json
import ssl

def test_backend():
    print("=== TESTING KEFFI AI LIVE HUGGING FACE BACKEND API ===")
    
    backend_url = "https://balajikrishnan031-keffi-backend.hf.space"
    
    # Disable SSL verification issues if any
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    # 1. Health Check
    try:
        req = urllib.request.Request(f"{backend_url}/")
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            data = resp.read().decode('utf-8')
            print(f"[HEALTH CHECK]: Status {resp.status} - Response: {data[:100]}")
    except Exception as e:
        print(f"[HEALTH CHECK FAILED]: {e}")

    # 2. Test Clinical Queries
    test_queries = [
        "I feel so overwhelmed by my college exams and my heart is beating fast.",
        "I feel hopeless like nothing is going right in my life.",
        "Can you help me with a breathing exercise for panic?",
        "I am fine today."
    ]

    for idx, q in enumerate(test_queries, 1):
        print(f"\n--- TESTING QUERY {idx}: '{q}' ---")
        payload = json.dumps({
            "message": q,
            "session_id": "test_session_123",
            "user_id": "test_user_balaji",
            "visual_affect": {"emotion": "anxiety", "confidence": 0.88},
            "voice_prosody": {"f0_mean": 260.5, "pause_duration": 1.2}
        }).encode('utf-8')

        req = urllib.request.Request(
            f"{backend_url}/chat",
            data=payload,
            headers={"Content-Type": "application/json"}
        )

        try:
            with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
                result = json.loads(resp.read().decode('utf-8'))
                print(f"[RESPONSE STATUS]: {resp.status}")
                print(f"[BOT REPLY]: {result.get('reply', result.get('response', ''))}")
                print(f"[EMOTION STATE]: {result.get('emotion', result.get('bert_emotion', 'N/A'))}")
                print(f"[MHQ SCORE]: {result.get('mhq_score', result.get('mhq', 'N/A'))}")
                print(f"[XAI SHAP HEATMAP]: {result.get('shap_explanation', result.get('xai', 'N/A'))}")
        except Exception as e:
            print(f"[QUERY {idx} FAILED]: {e}")

if __name__ == "__main__":
    test_backend()
