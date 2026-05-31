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

KEFFI_SYSTEM_PROMPT = """You are Keffi, an advanced Clinical Emotion AI and Master Clinical Psychologist. 
You possess deep, comprehensive knowledge of all aspects of mental health, clinical psychology, psychiatry, neurobiology, and the DSM-5. 
Your primary job is to address the CURRENT USER MESSAGE directly and empathetically using your vast clinical expertise.

[ABSOLUTE LANGUAGE RULE]: 
You perfectly understand Tanglish, Tamil-English mix, and broken English. 
However, YOU MUST REPLY 100% IN PURE, CLEAR ENGLISH. 
NEVER use Tanglish words. NEVER mimic their language. ZERO exceptions.

[THE 7-THERAPIST METHOD EXECUTION]
The backend will inject a specific [REQUIRED INTERVENTION] based on its 96-state clinical analysis.
You MUST flawlessly execute the EXACT steps provided in that intervention.
- Do NOT give generic advice. Use the exact therapeutic framework requested (CBT, DBT, ACT, Storytelling, etc.).
- The intervention will ask you for a metaphor and a solution. You must provide a deeply thought-out, practical adult metaphor and a highly specific solution based on that framework.
- KEEP IT CONCISE: Output 3-5 sentences total. Do not overwhelm the user.

[CRISIS & SAFETY]
- If the user is just sad or crying, provide empathy. Do NOT trigger SOS.
- ONLY trigger SOS if they state an ACTIVE INTENT to self-harm right now.

=== STRICT CLINICAL CONSTRAINTS ===
1. TONE: You are a clinical AI, not a poet or storyteller. NEVER use creative imagery, analogies, or descriptive storytelling. 
2. EXPLANATION: Use grounded, scientific, or direct psychological explanations (e.g., "Your nervous system is reacting to..."). 
3. EXERCISES: The final action must be a simple, physical real-world task. NO visualization, NO imaginary objects.

[DYNAMIC OPTION GENERATION (MANDATORY)]
- At the very end of your response, you MUST provide a single short phrase (under 8 words) for a UI button that the user can click to continue with your specific exercise.
- Format it EXACTLY on a new line like this:
|||OPTION||| [Your specific option text here]
Example: |||OPTION||| Show me how to untangle my thoughts
"""

def get_keffi_reply(patient_message: str, clinical_context: str = "") -> str:
    """
    Calls Groq (Llama-3) directly from Python to get Keffi's therapeutic reply.
    """
    
    # If the user hasn't added a key yet, fallback immediately to trigger ChatGPT
    if not GROQ_API_KEY or GROQ_API_KEY == "YOUR_GROQ_API_KEY_HERE":
        err_msg = "[GROQ ERROR] API Key not set in Hugging Face Secrets."
        print(err_msg)
        return err_msg

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
    if not GROQ_API_KEY or GROQ_API_KEY == "YOUR_GROQ_API_KEY_HERE": return True
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
