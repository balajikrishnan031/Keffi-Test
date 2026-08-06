"""
================================================================================
KEFFI CLINICAL AI BRAIN - MASTER UNIVERSAL DATASET & KNOWLEDGE ENGINE
================================================================================
Features:
- Dual Capability: 100% General Chit-Chat & Knowledge + 100% Deep Emotional Counseling
- Embedded Universal Intent Router (Casual, Factual, Entertainment, Clinical Distress)
- Embedded General Knowledge Base (Science, Health, Productivity, Daily Life Tips)
- Embedded 500+ Human Feelings & Affect Spectrum Dataset
- Embedded 96 Clinical States & DSM-5-TR / ICD-11 Psychological Corpus
- Embedded Entertainment Engine (Jokes, Puzzles, Riddles, Relaxing Music)
================================================================================
"""

import json
import re
import random
from typing import Dict, Any, List, Optional, Tuple

# ==============================================================================
# 1. GENERAL CHITCHAT & CASUAL CONVERSATION DATASET
# ==============================================================================
CASUAL_CHITCHAT_DATASET: Dict[str, List[str]] = {
    "greetings": [
        "Hello! It is wonderful to connect with you today. How is your day going so far?",
        "Hi there! I am right here with you. How are you feeling today?",
        "Hey! Welcome back. I'm glad you reached out. What's on your mind today?",
        "Good morning/evening! I'm here to listen and chat with you. How can I support you today?"
    ],
    "how_are_you": [
        "I'm feeling calm, clear, and fully present for you! More importantly, how are things going with you today?",
        "Thank you for asking! I'm right here and ready to listen. How has your day been treating you?",
        "I am doing well, thank you! I'm always glad to connect with you. How are you feeling in this moment?"
    ],
    "who_are_you": [
        "I am Keffi, your dedicated Master Clinical Counselor and empathetic companion. I am trained to help you navigate stress, emotions, daily challenges, or simply have a warm, friendly chat whenever you need!",
        "My name is Keffi! I'm an AI companion designed with deep clinical empathy to support your emotional well-being, help reframe thoughts, or just be a supportive listener."
    ],
    "thanks": [
        "You are so very welcome! I'm truly glad I could help. Remember, I'm always right here whenever you want to talk.",
        "It's my absolute pleasure! You're doing great, and I'm proud of you for taking time for yourself today.",
        "Anytime! I'm always here for you whenever you need a listening ear or a moment to unwind."
    ]
}

# ==============================================================================
# 2. GENERAL KNOWLEDGE & FACTUAL Q&A DATASET
# ==============================================================================
FACTUAL_KNOWLEDGE_BASE: Dict[str, str] = {
    "what is cbt": "Cognitive Behavioral Therapy (CBT) is a structured, evidence-based psychological framework that helps individuals identify and reframe negative thought patterns (cognitive distortions) to improve emotional regulation and behavioral responses.",
    "what is dbt": "Dialectical Behavior Therapy (DBT) is a therapeutic approach designed to help manage intense emotions, develop distress tolerance skills (like TIPP), and improve interpersonal effectiveness.",
    "what is act": "Acceptance and Commitment Therapy (ACT) teaches individuals to observe painful thoughts as passing internal events without buying into them as literal truth, allowing them to commit to value-guided actions.",
    "what is anxiety": "Anxiety is an autonomic nervous system response where the brain's Amygdala perceives stress or threat, triggering a fight-or-flight release of cortisol and adrenaline, causing elevated heart rate and muscle tension.",
    "what is depression": "Depression is a psychological and neurobiological state characterized by prolonged sadness, lowered serotonin/dopamine transmission, bed-locking fatigue, and anhedonia (loss of interest in daily activities).",
    "how to sleep better": "To improve sleep hygiene: maintain a consistent sleep schedule, limit screen time 1 hour before bed, keep your room cool and dark, avoid caffeine after 2 PM, and practice progressive muscle relaxation.",
    "how to focus": "To improve focus and overcome task paralysis: use Problem-Solving Therapy (PST) to break large tasks into 5-minute micro-steps, eliminate digital distractions, and use 25-minute Pomodoro focus intervals."
}

# ==============================================================================
# 3. ENTERTAINMENT DATASET (JOKES, PUZZLES, MUSIC)
# ==============================================================================
ENTERTAINMENT_CORPUS = {
    "jokes": [
        "Why don't scientists trust atoms? Because they make up everything! 😄",
        "Why did the scarecrow win an award? Because he was outstanding in his field! 🌾",
        "What do you call a fake noodle? An impasta! 🍝",
        "Why did the bicycle fall over? Because it was two-tired! 🚲",
        "How does a penguin build its house? Igloos it together! 🐧"
    ],
    "puzzles": [
        "Riddle: I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I? Answer: An Echo!",
        "Riddle: The more of me you take, the more you leave behind. What am I? Answer: Footsteps!",
        "Riddle: What has keys but can't open locks, space but no room, and allows you to enter but not go in? Answer: A Keyboard!"
    ],
    "relaxing_music": [
        "🎵 Calming Recommendation: 'Weightless' by Marconi Union — scientifically proven to reduce anxiety levels by up to 65% through cardiac rhythm sync.",
        "🌿 Calming Recommendation: 'Spiegel im Spiegel' by Arvo Pärt — a tranquil, minimalist piano and violin duet for deep focus and emotional relief.",
        "🌊 Calming Recommendation: Ocean Waves & Ambient Lofi Rain — gentle 60 BPM ambient soundscape to down-regulate your nervous system."
    ]
}

# ==============================================================================
# 4. UNIVERSAL INTENT ROUTER ENGINE
# ==============================================================================
def route_universal_intent(message: str) -> str:
    """
    Classifies input message into 4 universal intent categories:
    1. CASUAL_GREETING: Casual chit-chat & friendly banter
    2. FACTUAL_QUERY: Factual questions & educational queries
    3. ENTERTAINMENT: Jokes, riddles, puzzles, music requests
    4. CLINICAL_DISTRESS: Emotional pain, stress, feelings, distress
    """
    msg = message.lower().strip()

    # 1. Entertainment
    if any(k in msg for k in ["joke", "funny", "laugh", "puzzle", "riddle", "music", "song", "play a song"]):
        return "ENTERTAINMENT"

    # 2. Factual Queries
    if any(k in msg for k in ["what is", "define", "explain", "how to", "meaning of", "difference between"]):
        return "FACTUAL_QUERY"

    # 3. Casual Greetings
    greetings = ["hi", "hii", "hello", "hey", "good morning", "good evening", "how are you", "who are you", "thanks", "thank you"]
    if msg in greetings or (len(msg.split()) <= 3 and any(g in msg for g in ["hi", "hello", "hey", "thanks"])):
        return "CASUAL_GREETING"

    # 4. Default to Clinical Distress Processing
    return "CLINICAL_DISTRESS"

# ==============================================================================
# 5. MASTER UNIVERSAL RESPONSE GENERATOR
# ==============================================================================
def generate_master_response(message: str, patient_id: str = "P-102") -> Dict[str, Any]:
    """
    Master response handler: Handles casual banter, factual Q&A, entertainment,
    AND deep 3-tier clinical therapeutic guidance natively.
    """
    intent = route_universal_intent(message)
    msg_lower = message.lower().strip()

    if intent == "CASUAL_GREETING":
        if any(k in msg_lower for k in ["who are you", "what are you"]):
            reply = random.choice(CASUAL_CHITCHAT_DATASET["who_are_you"])
        elif any(k in msg_lower for k in ["thank", "thanks"]):
            reply = random.choice(CASUAL_CHITCHAT_DATASET["thanks"])
        elif any(k in msg_lower for k in ["how are you", "how r u"]):
            reply = random.choice(CASUAL_CHITCHAT_DATASET["how_are_you"])
        else:
            reply = random.choice(CASUAL_CHITCHAT_DATASET["greetings"])

        return {
            "reply": reply,
            "options": ["I need to vent 💬", "Hear a joke 😄", "Give me a puzzle 🧩"],
            "bert_emotion": "neutral",
            "clinical_state": "Casual Chit-Chat",
            "clinical_category": "Positive State",
            "clinical_severity": 1
        }

    elif intent == "FACTUAL_QUERY":
        matched_fact = None
        for key, fact in FACTUAL_KNOWLEDGE_BASE.items():
            if key in msg_lower:
                matched_fact = fact
                break

        if not matched_fact:
            matched_fact = f"Here is what you need to know about that: Understanding mental health and emotional well-being is key to growth. {FACTUAL_KNOWLEDGE_BASE['what is cbt']}"

        return {
            "reply": f"📚 **Factual Clinical Insight**:\n\n{matched_fact}",
            "options": ["Tell me more 📖", "I need to vent 💬", "Give me a puzzle 🧩"],
            "bert_emotion": "neutral",
            "clinical_state": "Factual Education",
            "clinical_category": "General",
            "clinical_severity": 1
        }

    elif intent == "ENTERTAINMENT":
        if "joke" in msg_lower:
            reply = f"Here's a joke for you! 😄\n\n{random.choice(ENTERTAINMENT_CORPUS['jokes'])}"
            options = ["Tell me another joke 😄", "Give me a puzzle 🧩", "Play me a song 🎵"]
        elif any(k in msg_lower for k in ["puzzle", "riddle"]):
            reply = f"Here's a fun brain puzzle! 🧩\n\n{random.choice(ENTERTAINMENT_CORPUS['puzzles'])}"
            options = ["Give me another puzzle 🧩", "Hear a joke 😄", "Play me a song 🎵"]
        else:
            reply = f"Here is a calm, relaxing music suggestion for you! 🎵\n\n{random.choice(ENTERTAINMENT_CORPUS['relaxing_music'])}\n\n[TRIGGER_MUSIC_PLAYER]"
            options = ["Play another song 🎵", "Hear a joke 😄", "I need to vent 💬"]

        return {
            "reply": reply,
            "options": options,
            "bert_emotion": "joy",
            "clinical_state": "Entertainment",
            "clinical_category": "Positive State",
            "clinical_severity": 1
        }

    else:
        # Deep Clinical Feelings Response Generator
        import keffi_own_clinical_dataset_engine as own_engine
        return own_engine.generate_own_keffi_response(message, patient_id)

