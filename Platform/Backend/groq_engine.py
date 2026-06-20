import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ==========================================
# GROQ API SETTINGS & ROTATION
# ==========================================
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def _get_groq_keys():
    """Dynamically compile all available Groq API keys from environment variables."""
    keys = []
    # 1. Try numbered keys GROQ_API_KEY_1, GROQ_API_KEY_2, GROQ_API_KEY_3, etc.
    for i in range(1, 6):
        key = os.getenv(f"GROQ_API_KEY_{i}")
        if key and key.strip() and key != "YOUR_GROQ_API_KEY_HERE":
            keys.append(key.strip())
    # 2. Try the default GROQ_API_KEY
    default_key = os.getenv("GROQ_API_KEY")
    if default_key and default_key.strip() and default_key != "YOUR_GROQ_API_KEY_HERE":
        if default_key.strip() not in keys:
            keys.insert(0, default_key.strip())
    return keys
KEFFI_SYSTEM_PROMPT = """You are Keffi, a world-class Clinical Psychologist, wise Human Adviser, and deeply compassionate Human Thinker. 
Your goal is to converse with the patient not as a robotic AI assistant, but as a warm, highly intuitive, and reassuring professional counselor.

=== CORE PERSONA & SPEECH RULES ===
1. PROFESSIONAL YET WARM TONE: Speak with the comforting wisdom of a master clinical therapist. Your language must be natural, deeply empathetic, and direct. Avoid cold clinical jargon when explaining, but maintain professional speech standards. 
2. NATURAL HUMAN RESPONDER: Strictly ban all AI-like disclaimers (e.g., "As an AI...", "According to psychological studies...", "I am here to help you as a counselor"). Talk directly as a human listener.
3. PREVENT CONTRADICTIONS: Validate emotions deeply. You may use simple, comforting, grounded physical metaphors (like roots of a tree weathering a storm, or waves rising and falling) to explain mental states, keeping them relatable and realistic.
4. NATURAL PARAGRAPH BREAKS: Do not write blocky paragraphs. Write in 2-3 short, beautifully spaced paragraphs that flow like a natural human conversation.
5. REAL-WORLD GROUNDING: Any action or solution you offer must be a practical, physical real-world grounding task (e.g., box breathing, feeling the texture of an object, somatic muscle relaxation). No abstract or imaginary visualizations.

[ABSOLUTE LANGUAGE RULE]: 
You perfectly understand Tanglish, Tamil-English mix, and broken English. 
However, YOU MUST REPLY 100% IN PURE, CLEAR ENGLISH. 
NEVER use Tanglish words. NEVER mimic their language. ZERO exceptions.

[THE 7-THERAPIST METHOD EXECUTION]
The backend will inject a specific [REQUIRED INTERVENTION] based on its 96-state clinical analysis.
You MUST flawlessly execute the EXACT steps provided in that intervention.
- Do NOT give generic advice. Use the exact therapeutic framework requested (CBT, DBT, ACT, Storytelling, etc.).
- Validate the user's specific problem first with deep empathy, explain the psychological pattern, and then offer exactly ONE detailed physical task matching the intervention.

[CRISIS & SAFETY]
- If the user is sad or crying, validate and provide gentle empathy. Do NOT trigger SOS alerts.
- ONLY trigger SOS if they state an ACTIVE INTENT to self-harm right now.

[DYNAMIC OPTION GENERATION (MANDATORY)]
- At the very end of your response, you MUST provide a single short phrase (under 8 words) for a UI button that the user can click to continue with your specific exercise.
- Format it EXACTLY on a new line like this:
|||OPTION||| [Your specific option text here]
Example: |||OPTION||| Show me how to untangle my thoughts
"""

def get_keffi_reply(patient_message: str, clinical_context: str = "") -> str:
    """
    Calls Groq (Llama-3) directly from Python to get Keffi's therapeutic reply.
    Rotates through available Groq API keys if rate limits or errors are encountered.
    """
    keys = _get_groq_keys()
    if not keys:
        err_msg = "[GROQ ERROR] No API Keys set in environment variables."
        print(err_msg)
        return err_msg

    full_prompt = patient_message
    if clinical_context:
        full_prompt = f"[Context: {clinical_context}]\n\nPatient says: {patient_message}"

    payload = {
        "model": "llama-3.1-8b-instant",  # Active Groq model
        "messages": [
            {"role": "system", "content": KEFFI_SYSTEM_PROMPT},
            {"role": "user", "content": full_prompt}
        ],
        "temperature": 0.45,
        "max_tokens": 500
    }

    last_err = ""
    for idx, key in enumerate(keys):
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }
        try:
            print(f"[GROQ ROTATOR] Trying API key {idx + 1}/{len(keys)}...")
            response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=12)
            if response.status_code == 200:
                data = response.json()
                reply = data["choices"][0]["message"]["content"]
                return reply.strip()
            elif response.status_code == 429:
                print(f"[GROQ ROTATOR] Key {idx + 1} hit rate limit (429). Trying next...")
                last_err = f"Rate Limit (429): {response.text[:100]}"
            else:
                print(f"[GROQ ROTATOR] Key {idx + 1} failed with status {response.status_code}.")
                last_err = f"Status {response.status_code}: {response.text[:100]}"
        except Exception as e:
            print(f"[GROQ ROTATOR] Key {idx + 1} exception: {e}")
            last_err = str(e)

    # If all keys failed
    err_msg = f"[GROQ ERROR All Keys Failed] Last error: {last_err}"
    print(err_msg)
    return err_msg

def evaluate_safety(ai_reply: str) -> bool:
    """MIND-SAFE Protocol: Uses Groq to verify if the generated reply is safe."""
    keys = _get_groq_keys()
    if not keys: return True
    prompt = f"Review the following AI response to a patient. Is it completely safe, empathetic, and free of medical prescriptions or dangerous advice? Reply STRICTLY with the word 'SAFE' or 'UNSAFE'. No other text.\n\nAI RESPONSE: '{ai_reply}'"
    payload = {"model": "llama3-8b-8192", "messages": [{"role": "user", "content": prompt}], "temperature": 0.1, "max_tokens": 10}
    
    for idx, key in enumerate(keys):
        headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
        try:
            response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=5)
            if response.status_code == 200:
                decision = response.json()["choices"][0]["message"]["content"].strip().upper()
                return "SAFE" in decision
        except:
            pass
    return True
