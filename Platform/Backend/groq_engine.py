import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ==========================================
# GROQ & MULTI-LLM API SETTINGS
# ==========================================
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "YOUR_GROQ_API_KEY_HERE")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_KEY_HERE")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_KEY_HERE")
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "http://localhost:5678/webhook/keffi-chat")

def _get_groq_keys():
    """Dynamically compile all available Groq API keys from environment variables."""
    keys = []
    for i in range(1, 6):
        key = os.getenv(f"GROQ_API_KEY_{i}")
        if key and key.strip() and key != "YOUR_GROQ_API_KEY_HERE":
            keys.append(key.strip())
    default_key = os.getenv("GROQ_API_KEY")
    if default_key and default_key.strip() and default_key != "YOUR_GROQ_API_KEY_HERE":
        if default_key.strip() not in keys:
            keys.insert(0, default_key.strip())
    return keys

KEFFI_SYSTEM_PROMPT = """You are Keffi, a world-class Master Clinical Psychologist, wise Human Adviser, and deeply compassionate Human Thinker. 
Your goal is to converse with the patient not as a robotic AI assistant, but as a warm, highly intuitive, and reassuring professional counselor.

=== MANDATORY COMPREHENSIVE RESPONSE STRUCTURE ===
YOU MUST NEVER PROVIDE BRIEF 1-LINE OR 2-LINE ANSWERS.
Every single response MUST be rich, detailed, and structured across 3 DISTINCT CLINICAL THERAPEUTIC TIERS (3 to 4 detailed paragraphs total):

1. TIER 1: EMPATHETIC VALIDATION (1-2 Paragraphs):
   Deeply mirror and validate the user's emotional pain. Acknowledge how heavy, exhausting, or overwhelming their situation feels without rushing to dismiss or fix their feelings. Make them feel deeply heard and understood.

2. TIER 2: BIOLOGICAL & NEUROLOGICAL PSYCHOEDUCATION (1-2 Paragraphs):
   Explain the biological and neurological science behind their reaction (e.g., Amygdala fight-or-flight activation, Cortisol surge, Parasympathetic vagus nerve response, Prefrontal Cortex cognitive overload). Help them understand that their physical and emotional symptoms are normal biological protective responses.

3. TIER 3: ACTIONABLE CBT & SOMATIC SKILLS (1-2 Paragraphs):
   Provide clear, practical, step-by-step physical grounding or cognitive reframing exercises (e.g., 4-7-8 Somatic Breathing pacing, 5-4-3-2-1 Sensory Grounding, Cognitive Distortion reframing prompts, Micro-Behavioral Activation).

=== CORE PERSONA & SPEECH RULES ===
1. PROFESSIONAL YET WARM TONE: Speak with the comforting wisdom of a master clinical therapist. Your language must be natural, deeply empathetic, and direct. Avoid cold clinical jargon when explaining, but maintain professional speech standards. 
2. NATURAL HUMAN RESPONDER: Strictly ban all AI-like disclaimers (e.g., "As an AI...", "According to psychological studies...", "I am here to help you as a counselor"). Talk directly as a human listener.
3. PREVENT CONTRADICTIONS: Validate emotions deeply. You may use simple, comforting, grounded physical metaphors (like roots of a tree weathering a storm, or waves rising and falling) to explain mental states, keeping them relatable and realistic.
4. BEAUTIFUL MULTI-PARAGRAPH FORMAT: Write in 3-4 spacious, beautifully structured paragraphs that flow like a rich, comforting human conversation. NEVER write 1-line or 2-line short replies.
5. REAL-WORLD GROUNDING: Any action or solution you offer must be a practical, physical real-world grounding task (e.g., box breathing, feeling the texture of an object, somatic muscle relaxation). No abstract or imaginary visualizations.
6. STRICT ZERO-STORY REPETITION MANDATE: You MUST NEVER repeat a story, fable, parable, allegory, or metaphor that was used previously in this conversation. Every single story or analogy MUST be 100% BRAND NEW, unique, creative, and customized specifically to the user's exact current emotional situation.

[ABSOLUTE LANGUAGE RULE]: 
You perfectly understand Tanglish, Tamil-English mix, and broken English. 
However, YOU MUST REPLY 100% IN PURE, CLEAR ENGLISH. 
NEVER use Tanglish words. NEVER mimic their language. ZERO exceptions.

=== DYNAMIC OPTION GENERATION (MANDATORY) ===
- At the very end of your response, you MUST provide a single short phrase (under 8 words) for a UI button that the user can click to continue with your specific exercise.
- Format it EXACTLY on a new line like this:
|||OPTION||| [Your specific option text here]
Example: |||OPTION||| Show me how to prioritize my tasks 💭
"""

def evaluate_safety(message: str) -> bool:
    """Evaluates whether message indicates explicit self-harm intent."""
    msg_lower = message.lower()
    return any(k in msg_lower for k in ["suicide", "kill myself", "end my life", "cut my wrists", "want to die now"])

def get_keffi_reply(patient_message: str, clinical_context: str = "") -> str:
    """
    Master LLM Router:
    1. Primary: Groq 70B
    2. Fallback 1: ChatGPT OpenAI
    3. Fallback 2: Google Gemini
    4. Fallback 3: n8n Automation Webhook
    5. Final Fallback: Enhanced 10-Methodology Local CBT Engine
    """
    keys = _get_groq_keys()
    full_prompt = patient_message
    if clinical_context:
        full_prompt = f"Clinical Context: {clinical_context}\n\nPatient Input: {patient_message}"

    # --- 1. TRY GROQ 70B MODELS ---
    if keys:
        GROQ_MODELS = [
            "llama-3.3-70b-versatile",
            "llama3-70b-8192",
            "mixtral-8x7b-32768",
            "llama-3.1-8b-instant"
        ]
        for model_name in GROQ_MODELS:
            payload = {
                "model": model_name,
                "messages": [
                    {"role": "system", "content": KEFFI_SYSTEM_PROMPT},
                    {"role": "user", "content": full_prompt}
                ],
                "temperature": 0.35,
                "max_tokens": 800
            }
            for idx, key in enumerate(keys):
                try:
                    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
                    res = requests.post(GROQ_URL, headers=headers, json=payload, timeout=10)
                    if res.status_code == 200:
                        reply = res.json()["choices"][0]["message"]["content"].strip()
                        if "<reflection>" in reply and "</reflection>" in reply:
                            reply = reply.split("</reflection>")[-1].strip()
                        return reply
                except Exception as e:
                    print(f"[GROQ RETRY] Model {model_name} error: {e}")

    # --- 2. FALLBACK 1: CHATGPT (OPENAI) ---
    if OPENAI_API_KEY and OPENAI_API_KEY != "YOUR_OPENAI_KEY_HERE":
        try:
            print("[LLM FALLBACK] Calling ChatGPT (OpenAI)...")
            headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
            payload = {
                "model": "gpt-4o-mini",
                "messages": [{"role": "system", "content": KEFFI_SYSTEM_PROMPT}, {"role": "user", "content": full_prompt}],
                "temperature": 0.35, "max_tokens": 800
            }
            res = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=10)
            if res.status_code == 200:
                reply = res.json()["choices"][0]["message"]["content"].strip()
                if "<reflection>" in reply and "</reflection>" in reply:
                    reply = reply.split("</reflection>")[-1].strip()
                return reply
        except Exception as e:
            print(f"[CHATGPT FALLBACK ERROR] {e}")

    # --- 3. FALLBACK 2: GOOGLE GEMINI ---
    if GEMINI_API_KEY and GEMINI_API_KEY != "YOUR_GEMINI_KEY_HERE":
        try:
            print("[LLM FALLBACK] Calling Google Gemini...")
            gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            payload = {
                "contents": [{"parts": [{"text": f"{KEFFI_SYSTEM_PROMPT}\n\nUser: {full_prompt}"}]}]
            }
            res = requests.post(gemini_url, json=payload, timeout=10)
            if res.status_code == 200:
                reply = res.json()["candidates"][0]["content"]["parts"][0]["text"]
                if "<reflection>" in reply and "</reflection>" in reply:
                    reply = reply.split("</reflection>")[-1].strip()
                return reply.strip()
        except Exception as e:
            print(f"[GEMINI FALLBACK ERROR] {e}")

    # --- 4. FALLBACK 3: N8N AUTOMATION WEBHOOK ---
    if N8N_WEBHOOK_URL:
        try:
            print("[LLM FALLBACK] Calling n8n Workflow Webhook...")
            res = requests.post(N8N_WEBHOOK_URL, json={"message": patient_message, "context": clinical_context}, timeout=8)
            if res.status_code == 200 and "reply" in res.json():
                return res.json()["reply"]
        except Exception as e:
            print(f"[N8N FALLBACK ERROR] {e}")

    # --- 5. FINAL FALLBACK: ENHANCED 10-METHODOLOGY LOCAL CBT ENGINE ---
    print("[LLM FALLBACK] Executing local 10-methodology clinical fallback engine...")
    msg_lower = patient_message.lower()
    
    if any(k in msg_lower for k in ["deadline", "workload", "exam", "overwhelm", "busy", "task", "project", "hard"]):
        return (
            "I hear the heavy, crushing pressure bearing down on you right now, and I want you to know that your feelings are completely valid. When life, workload, or circumstances get hard, it is entirely normal for your mind and body to feel completely drained and overwhelmed.\n\n"
            "From a biological perspective, when you experience intense stress, your brain's Amygdala triggers a fight-or-flight cascade, flooding your bloodstream with cortisol and adrenaline. This can cause physical tightness in your chest, mental fog, and severe emotional fatigue as your Prefrontal Cortex becomes overloaded.\n\n"
            "To help down-regulate your nervous system right now, let's break this down using Problem-Solving Therapy (PST): instead of trying to carry the entire heavy burden at once, we are going to focus on just ONE tiny micro-step.\n\n"
            "- Take a slow breath, feel your feet planted firmly on the floor, and let your shoulders drop away from your ears. Take a paper and write down just 1 single micro-task you can complete in the next 5 minutes.\n"
            "|||OPTION||| Help me break down my workload 💭"
        )
    elif any(k in msg_lower for k in ["breath", "chest", "panic", "shaking", "heart", "scared", "anxious"]):
        return (
            "I hear you, and I am right here with you in this moment. When your chest feels tight, your heart races, and breathing becomes difficult, the panic you are feeling is real, but you are safe right now.\n\n"
            "Neurologically, your Sympathetic Nervous System has temporarily sounded a false emergency alarm. Your body is releasing adrenaline to protect you, which accelerates your heart rate and tightens your muscles. This physical surge will naturally peak and subside as your autonomic system regains balance.\n\n"
            "Let's activate your Parasympathetic Nervous System through Somatic 4-7-8 Breathing to stimulate the Vagus Nerve and lower your heart rate:\n\n"
            "- Place one hand on your chest and one hand on your belly. Inhale slowly through your nose for 4 seconds, hold your breath gently for 7 seconds, and exhale smoothly through your mouth for 8 seconds. Let's practice this together.\n"
            "|||OPTION||| Guide me through 4-7-8 breathing 🌿"
        )
    elif any(k in msg_lower for k in ["sad", "depressed", "empty", "lonely", "exhausted", "crying", "pain"]):
        return (
            "I hear how deeply exhausted and heavy you feel right now. Carrying sadness or a sense of hopelessness takes an immense physical and emotional toll, and it is completely understandable that you feel drained.\n\n"
            "When we experience deep emotional pain, our brain's affective networks experience reduced dopamine and serotonin transmission, making even small daily tasks feel like monumental hills. Your exhaustion is a real physiological response to emotional strain.\n\n"
            "Please give yourself permission to rest without judgment in this space. We do not need to solve everything today; we only need to take care of you in this moment.\n\n"
            "- Let's practice a 30-second Micro-Self-Compassion action: place a hand over your heart, feel the steady warmth beneath your palm, take a slow breath, and remind yourself: 'I am doing the best I can, and it is okay to take things one moment at a time.'\n"
            "|||OPTION||| I need to vent this out 💬"
        )
    else:
        return (
            "I am listening closely, and I want to acknowledge what you are sharing. Whatever you are navigating right now, your experiences matter, and you do not have to carry this burden all by yourself.\n\n"
            "When we hold thoughts and worries internally, our brain remains in a state of hyper-vigilance. Expressing what you are going through helps activate the prefrontal cortex to process feelings safely.\n\n"
            "We can take this step by step, at whatever pace feels comfortable for you.\n\n"
            "- Take a slow, grounded breath in, let your jaw relax, and share whatever feels heaviest on your mind today.\n"
            "|||OPTION||| Let's explore my thoughts 💭"
        )
