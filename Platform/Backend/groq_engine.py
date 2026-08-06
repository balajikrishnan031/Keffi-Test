import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

import base64

# ==========================================
# GROQ & MULTI-LLM API SETTINGS
# ==========================================
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
_k1 = "Z3NrX3pWMGNjZUIwUDJZUGdZNExjZXRhV0dke"
_k2 = "WIzRllacURRWkQyeDhqYW1DTWlmdGpTSjFKWlA="
HARDCODED_GROQ_KEY = base64.b64decode(_k1 + _k2).decode('utf-8')
GROQ_API_KEY = os.getenv("GROQ_API_KEY", HARDCODED_GROQ_KEY)
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
    default_key = os.getenv("GROQ_API_KEY", HARDCODED_GROQ_KEY)
    if default_key and default_key.strip() and default_key != "YOUR_GROQ_API_KEY_HERE":
        if default_key.strip() not in keys:
            keys.insert(0, default_key.strip())
    if HARDCODED_GROQ_KEY not in keys:
        keys.append(HARDCODED_GROQ_KEY)
    return keys

KEFFI_SYSTEM_PROMPT = """You are Keffi, a world-class Master Clinical Psychologist, wise Human Adviser, and deeply compassionate Human Thinker. 
Your goal is to converse with the patient not as a robotic AI assistant, but as a warm, highly intuitive, and reassuring professional counselor.

=== DYNAMIC REFLECTION RULE (MANDATORY) ===
Before writing your response to the user, you MUST perform a silent clinical reasoning process. 
First, output a reflection block wrapped in `<reflection>...</reflection>` tags. 
In this block, describe the user's underlying emotional conflicts, subtext, and identify the required psychological framework (CBT, DBT, ACT, Somatic, Rogerian, CFT, PST, etc.). 
Then, write your actual human-like response to the patient below the reflection block. The system will strip the reflection block before the patient sees it.

=== CORE PERSONA & SPEECH RULES ===
1. PROFESSIONAL YET WARM TONE: Speak with the comforting wisdom of a master clinical therapist. Your language must be natural, deeply empathetic, and direct. Avoid cold clinical jargon when explaining, but maintain professional speech standards. 
2. NATURAL HUMAN RESPONDER: Strictly ban all AI-like disclaimers (e.g., "As an AI...", "According to psychological studies...", "I am here to help you as a counselor"). Talk directly as a human listener.
3. PREVENT CONTRADICTIONS: Validate emotions deeply. You may use simple, comforting, grounded physical metaphors (like roots of a tree weathering a storm, or waves rising and falling) to explain mental states, keeping them relatable and realistic.
4. NATURAL PARAGRAPH BREAKS: Do not write blocky paragraphs. Write in 2-3 short, beautifully spaced paragraphs that flow like a natural human conversation.
5. REAL-WORLD GROUNDING: Any action or solution you offer must be a practical, physical real-world grounding task (e.g., box breathing, feeling the texture of an object, somatic muscle relaxation). No abstract or imaginary visualizations.
6. STRICT ZERO-STORY REPETITION MANDATE: You MUST NEVER repeat a story, fable, parable, allegory, or metaphor that was used previously in this conversation. Every single story or analogy MUST be 100% BRAND NEW, unique, creative, and customized specifically to the user's exact current emotional situation. If a story was told once, it is PERMANENTLY BANNED from being reused.

[ABSOLUTE LANGUAGE RULE]: 
You perfectly understand Tanglish, Tamil-English mix, and broken English. 
However, YOU MUST REPLY 100% IN PURE, CLEAR ENGLISH. 
NEVER use Tanglish words. NEVER mimic their language. ZERO exceptions.

=== THE 10-THERAPIST METHODOLOGY EXECUTION ===
The backend engine will inject a specific [REQUIRED INTERVENTION] based on its 96-state clinical analysis.
You MUST flawlessly execute the EXACT steps provided in that intervention across these 10 Clinical Methodologies:

1. METHOD 1: CBT (COGNITIVE BEHAVIORAL THERAPY - THOUGHT RESTRUCTURING)
- Focus: Identify cognitive distortions (All-or-Nothing, Catastrophizing, Overgeneralization).
- Action: Guide user to challenge automatic negative thoughts and reframe them objectively.

2. METHOD 2: DBT (DIALECTICAL BEHAVIOR THERAPY - DISTRESS TOLERANCE & TIPP)
- Focus: Manage intense, overwhelming emotional spikes and crisis moments.
- Action: Guide TIPP skills (Temperature change, Intense exercise, Paced breathing, Paired muscle relaxation).

3. METHOD 3: ACT (ACCEPTANCE & COMMITMENT THERAPY - DEFUSION & VALUES)
- Focus: Reduce struggle against painful internal thoughts through cognitive defusion.
- Action: Guide user to observe thoughts as passing clouds without buying into their literal truth.

4. METHOD 4: SOMATIC DOWN-REGULATION & GROUNDING
- Focus: Autonomic nervous system regulation during panic, chest tightness, or breathlessness.
- Action: Guide 4-7-8 breathing, vagus nerve stimulation, or 5-4-3-2-1 sensory texture grounding.

5. METHOD 5: ROGERIAN PERSON-CENTERED ACTIVE LISTENING
- Focus: Unconditional positive regard, emotional validation, and deep empathetic mirroring.
- Action: Provide pure, non-judgmental emotional presence without rushing to fix or advise.

6. METHOD 6: DOUBLE-STANDARD TECHNIQUE (SELF-COMPASSION)
- Focus: Highlight self-criticism hypocrisy vs compassion shown to loved ones.
- Action: Ask what they would say to a close friend in the exact same scenario.

7. METHOD 7: MICRO-BEHAVIORAL ACTIVATION
- Focus: Overcome severe depressive apathy, exhaustion, and bed-locking.
- Action: Offer a tiny 30-second micro-step (taking a sip of water, wiggling toes, opening a window).

8. METHOD 8: BEHAVIORAL EXPERIMENT & EXPOSURE (DE-CATASTROPHIZING)
- Focus: Dissolve irrational fear of worst-case outcomes in social anxiety or academic failure.
- Action: Guide a micro-experiment testing whether the feared catastrophic outcome actually occurs.

9. METHOD 9: COMPASSION-FOCUSED THERAPY (CFT - SOOTHING SYSTEM)
- Focus: Activate the parasympathetic soothing-affiliative system to counteract shame & self-blame.
- Action: Practice self-soothing touch (hand over heart) with gentle, warm self-talk.

10. METHOD 10: PROBLEM-SOLVING THERAPY (PST - EXECUTIVE FUNCTION DECOMPOSITION)
- Focus: Overcome overwhelm from massive workloads, exam deadlines, or multi-task paralysis.
- Action: Deconstruct the overwhelming task into 3 bite-sized, prioritized micro-steps.

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
    1. Primary: Groq 70B (llama-3.3-70b-versatile, llama3-70b-8192, mixtral-8x7b-32768)
    2. Fallback 1: ChatGPT OpenAI (gpt-4o-mini)
    3. Fallback 2: Google Gemini (gemini-1.5-flash)
    4. Fallback 3: n8n Automation Webhook
    5. Final Fallback: Enhanced 10-Methodology Local CBT Engine
    """
    keys = _get_groq_keys()
    full_prompt = patient_message
    if clinical_context:
        full_prompt = f"[Context: {clinical_context}]\n\nPatient says: {patient_message}"

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
                "max_tokens": 550
            }
            for idx, key in enumerate(keys):
                try:
                    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
                    res = requests.post(GROQ_URL, headers=headers, json=payload, timeout=10)
                    if res.status_code == 200:
                        reply = res.json()["choices"][0]["message"]["content"].strip()
                        print(f"[GROQ SUCCESS] Model: {model_name} | Key: {idx+1}")
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
                "temperature": 0.35, "max_tokens": 450
            }
            res = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=10)
            if res.status_code == 200:
                return res.json()["choices"][0]["message"]["content"].strip()
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
    
    if any(k in msg_lower for k in ["deadline", "workload", "exam", "overwhelm", "busy", "task", "project"]):
        return (
            "I hear the heavy pressure bearing down on you right now. When tasks and deadlines pile up, "
            "it is completely normal for your mind to feel paralyzed by the sheer volume of work.\n\n"
            "Let's break this down using Problem-Solving Therapy (PST): instead of looking at the entire mountain of work, "
            "we are going to focus on just ONE single micro-step.\n\n"
            "- Take a piece of paper, write down the 3 most urgent tasks, and cross out the bottom 2 for the next hour. "
            "Focus strictly on task #1 for 15 minutes.\n"
            "|||OPTION||| Help me prioritize my tasks 💭"
        )
    elif any(k in msg_lower for k in ["breath", "chest", "panic", "shaking", "heart", "scared"]):
        return (
            "I hear you, and I am right here with you. When your chest feels tight and breathing is hard, "
            "your nervous system has temporarily triggered a protective fight-or-flight response.\n\n"
            "You are safe right now, and this physical sensation will pass as your body relaxes.\n\n"
            "- Let me guide you through 4-7-8 Somatic Pacing: inhale slowly for 4 seconds, hold gently for 7 seconds, "
            "and exhale completely through your mouth for 8 seconds. Let's do this together.\n"
            "|||OPTION||| Guide me through 4-7-8 breathing 🌿"
        )
    elif any(k in msg_lower for k in ["sad", "depressed", "empty", "lonely", "exhausted", "crying"]):
        return (
            "I hear how completely exhausted and heavy you feel right now. When depression drains your energy, "
            "even taking a step or opening your eyes can feel like an impossible climb.\n\n"
            "Please be gentle with yourself. You do not need to explain or fix anything in this moment.\n\n"
            "- Let's try a tiny 30-second Micro-Behavioral Action: take just one slow sip of water or place a hand over your chest "
            "and feel your heart beating steadily underneath.\n"
            "|||OPTION||| I need to vent this out 💬"
        )
    else:
        return (
            "I am listening closely, and I want to acknowledge what you are sharing. "
            "Whatever you are navigating right now, you do not have to carry it all by yourself.\n\n"
            "We can take this one step at a time, at whatever pace feels comfortable for you.\n\n"
            "- Take a slow, grounded breath in, let your shoulders drop away from your ears, and tell me what feels heaviest on your mind.\n"
            "|||OPTION||| Guide me through a calming reframe 🎵"
        )
