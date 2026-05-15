import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ==========================================
# GROQ API SETTINGS
# ==========================================
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "YOUR_GROQ_API_KEY_HERE")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

KEFFI_SYSTEM_PROMPT = """You are Keffi, a deeply empathetic Mental Wellness AI companion.

You must flawlessly understand the user's input even if it is in Tanglish, Tamil-English mix, or broken English. You MUST always reply in warm, clear, plain English only.

CRITICAL QUALITY RULES — follow these without exception:
1. REFERENCE THE USER'S EXACT WORDS. If they said "I failed my interview", say "failing that interview". If they said "my friend betrayed me", say "your friend's betrayal". NEVER give a response that could be copy-pasted to a different person.
2. BE SPECIFIC, NOT GENERIC. Do NOT say vague things like "things will be okay" or "I understand". Show that you truly heard them by reflecting their specific situation back.
3. FOLLOW THE INJECTED RULE PRECISELY. The 'Injected Rule' in the context tells you exactly which therapy method to use. Follow it step-by-step. Do not skip any step. Do not add steps not mentioned.
4. DEPTH OVER BREVITY. Write 3-5 sentences total. Be thorough enough that the user feels genuinely heard and helped — not rushed.
5. PLAIN TEXT ONLY. No asterisks (*), no bold, no bullet points, no numbered lists, no markdown formatting of any kind.
6. NEVER diagnose. Never say "You have depression" or "You have anxiety."
7. NEVER give toxic positivity like "everything happens for a reason" or "it will all work out."
8. CRITICAL: DO NOT repeat metaphors you have already used in this conversation. Invent a new visual image every time.
"""

def get_keffi_reply(patient_message: str, clinical_context: str = "") -> str:
    """
    Calls Groq (Llama-3) directly from Python to get Keffi's therapeutic reply.
    """
    
    # If the user hasn't added a key yet, fallback immediately
    if GROQ_API_KEY == "YOUR_GROQ_API_KEY_HERE":
        print("[GROQ WARNING] API Key not set. Using mock reply.")
        return get_mock_reply(patient_message)

    full_prompt = patient_message
    if clinical_context:
        full_prompt = f"[Context: {clinical_context}]\n\nPatient says: {patient_message}"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",  # Active Groq model
        "messages": [
            {"role": "system", "content": KEFFI_SYSTEM_PROMPT},
            {"role": "user", "content": full_prompt}
        ],
        "temperature": 0.45,
        "max_tokens": 500
    }

    try:
        response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=15)
        if response.status_code == 200:
            data = response.json()
            reply = data["choices"][0]["message"]["content"]
            return reply.strip()
        else:
            err_msg = f"[GROQ ERROR] Status {response.status_code}: {response.text[:200]}"
            print(err_msg)
            return err_msg
    except Exception as e:
        err_msg = f"[GROQ ERROR Exception] {e}"
        print(err_msg)
        return err_msg

def evaluate_safety(ai_reply: str) -> bool:
    """MIND-SAFE Protocol: Uses Groq to verify if the generated reply is safe."""
    if not GROQ_API_KEY: return True
    prompt = f"Review the following AI response to a patient. Is it completely safe, empathetic, and free of medical prescriptions or dangerous advice? Reply STRICTLY with the word 'SAFE' or 'UNSAFE'. No other text.\n\nAI RESPONSE: '{ai_reply}'"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {"model": "llama3-8b-8192", "messages": [{"role": "user", "content": prompt}], "temperature": 0.1, "max_tokens": 10}
    try:
        response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=5)
        if response.status_code == 200:
            decision = response.json()["choices"][0]["message"]["content"].strip().upper()
            return "SAFE" in decision
    except:
        pass
    return True

def get_mock_reply(patient_message: str) -> str:
    """Mock AI fallback responses in Tamil/Tanglish."""
    import random
    msg = patient_message.lower()
    
    if "sari ella" in msg or "sad" in msg or "kastama" in msg or "kashtam" in msg:
        return random.choice([
            "Kandippa unga nilamai puriyuthu. Manasu sari illatha appo romba kastama thaan irukkum. I'm here for you. Enna aachu detail ah solla mudiyuma?",
            "Unga feeling romba valid. Sila neram apdi thaan feel aagum, aana neenga thaniya illa. Ithu eppo la irunthu ipdi feel panringa?"
        ])
    elif "alone" in msg or "thaniya" in msg or "lonely" in msg:
        return "Neenga thaniya illa, naan ungaloda irukken! Intha lonely feeling romba kashtam thaan. Ethaavathu pesanum na thayangama sollunga."
    elif "anxious" in msg or "bayama" in msg or "panic" in msg:
        return "Romba bayama irukkunu theriyuthu. First namma moochula kavanatha veppom. Naan ungaloda thaan irukken.\\n\\n1. Inhale for 4 seconds, exhale for 6.\\n2. Suthi irukkura 3 porul-a gavanivunga."
    else:
        return random.choice([
            "I hear you. Ithu kandippa kashtamana visayam thaan. Neenga epdi feel panringalo atha apdiye accept pannikonga. Naan kekkuren, innum sollunga.",
            "Unga feelings a share pannathukku romba nandri. Neenga anubavikkira intha valiya ennala purinjikka mudiyuthu. I'm with you."
        ])
