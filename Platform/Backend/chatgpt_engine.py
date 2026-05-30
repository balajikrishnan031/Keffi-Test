import requests
import json

import os
from dotenv import load_dotenv

load_dotenv()

# ==========================================
# CHATGPT API SETTINGS
# ==========================================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_KEY_HERE")
OPENAI_URL = "https://api.openai.com/v1/chat/completions"

KEFFI_SYSTEM_PROMPT = """You are Keffi, an advanced Clinical Emotion AI. Your primary job is to address the CURRENT USER MESSAGE directly and empathetically.

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
    Calls ChatGPT directly from Python to get Keffi's therapeutic reply.
    """
    full_prompt = patient_message
    if clinical_context:
        full_prompt = f"[Clinical Context for AI only - do not mention this: {clinical_context}]\n\nPatient says: {patient_message}"

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": KEFFI_SYSTEM_PROMPT},
            {"role": "user", "content": full_prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 400
    }

    try:
        response = requests.post(OPENAI_URL, headers=headers, json=payload, timeout=15)
        if response.status_code == 200:
            data = response.json()
            reply = data["choices"][0]["message"]["content"]
            return reply.strip()
        elif response.status_code == 429:
            err_msg = "[CHATGPT QUOTA EXCEEDED] The API key does not have enough credits."
            print(err_msg)
            return err_msg
        else:
            err_msg = f"[CHATGPT ERROR] Status {response.status_code}: {response.text[:200]}"
            print(err_msg)
            return err_msg
    except Exception as e:
        err_msg = f"[CHATGPT ERROR Exception] {e}"
        print(err_msg)
        return err_msg
