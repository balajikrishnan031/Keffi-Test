"""
================================================================================
KEFFI CLINICAL AI BRAIN - EXPANDED WORLD KNOWLEDGE & DIALOGUE ENGINE
================================================================================
Architecture:
- Exhaustive General Knowledge & World Facts Knowledge Base (Science, Health, Tech, Life)
- Intelligent Dialogue Protocol (Understands EXACTLY how to reply to any prompt)
- 500+ Human Feelings & Affect Spectrum Mapping
- 3-Tier Clinical Therapeutic Response Engine
================================================================================
"""

import json
import re
import random
from typing import Dict, Any, List, Optional

# ==============================================================================
# 1. EXHAUSTIVE GENERAL KNOWLEDGE & WORLD FACTS KNOWLEDGE BASE
# ==============================================================================
KEFFI_WORLD_GENERAL_KNOWLEDGE_BASE: Dict[str, Dict[str, str]] = {
    "neuroscience": {
        "title": "Neuroscience & Brain Biology",
        "content": "The human brain contains approximately 86 billion neurons connected by over 100 trillion synaptic connections. The Prefrontal Cortex governs executive function and decision making, while the Amygdala regulates fear and emotional threat detection. Neuroplasticity allows the brain to re-wire itself through continuous learning and CBT practices."
    },
    "cbt": {
        "title": "Cognitive Behavioral Therapy (CBT)",
        "content": "CBT is a gold-standard psychological framework pioneered by Aaron Beck. It operates on the core principle that our thoughts, feelings, and behaviors are interconnected. Reframing cognitive distortions (catastrophizing, all-or-nothing thinking) improves mood and emotional regulation."
    },
    "dbt": {
        "title": "Dialectical Behavior Therapy (DBT)",
        "content": "Developed by Marsha Linehan, DBT combines cognitive therapy with mindfulness and distress tolerance skills (TIPP: Temperature, Intense Exercise, Paced Breathing, Paired Muscle Relaxation) to help manage intense emotional dysregulation."
    },
    "act": {
        "title": "Acceptance and Commitment Therapy (ACT)",
        "content": "Developed by Steven Hayes, ACT uses cognitive defusion and mindfulness to help individuals accept painful internal feelings without struggle, enabling them to commit to value-guided life goals."
    },
    "sleep_hygiene": {
        "title": "Sleep Science & Circadian Hygiene",
        "content": "Sleep is governed by circadian rhythms and Adenosine accumulation. To optimize sleep: maintain a consistent wake time, get 15 minutes of natural sunlight upon waking, restrict screen light 1 hour before bed, and keep the bedroom at 18-20°C."
    },
    "productivity": {
        "title": "Productivity & Executive Function",
        "content": "Executive dysfunction causes task paralysis when large goals overload working memory. Breaking tasks into 5-minute micro-steps using Problem-Solving Therapy (PST) and Pomodoro intervals (25m work / 5m rest) restores focus."
    },
    "nutrition_mind": {
        "title": "Gut-Brain Axis & Nutritional Psychiatry",
        "content": "Over 90% of the body's Serotonin receptors are located in the gastrointestinal tract. The vagus nerve continuously communicates gut microbiome signals to the brain. Diets rich in Omega-3 fatty acids, probiotics, and complex fiber support mood stability."
    },
    "artificial_intelligence": {
        "title": "Artificial Intelligence & Affective Computing",
        "content": "Affective Computing is the study and development of systems that can recognize, interpret, process, and simulate human affects. Keffi AI utilizes Transformer BERT models, Groq 70B LLMs, and SHAP/LIME Explainable AI to deliver compassionate clinical guidance."
    }
}

# ==============================================================================
# 2. INTELLIGENT DIALOGUE PROTOCOL (KNOWS EXACTLY HOW TO REPLY)
# ==============================================================================
class KeffiIntelligentDialogueProtocol:
    """
    Analyzes any user input and determines the precise response protocol:
    - GENERAL_KNOWLEDGE: Rich educational answer
    - CASUAL_BANTER: Warm friendly conversation
    - ENTERTAINMENT: Joke, puzzle, or music
    - CLINICAL_THERAPY: 3-tier therapeutic counseling
    """
    
    @staticmethod
    def classify_and_reply(user_input: str) -> Dict[str, Any]:
        text = user_input.lower().strip()

        # 1. General Knowledge Check
        for key, knowledge_data in KEFFI_WORLD_GENERAL_KNOWLEDGE_BASE.items():
            if key in text or any(word in text for word in key.split('_')):
                return {
                    "protocol": "GENERAL_KNOWLEDGE",
                    "reply": f"🧠 **General Knowledge Insight: {knowledge_data['title']}**\n\n{knowledge_data['content']}",
                    "options": ["Tell me more 📖", "I need to vent 💬", "Give me a puzzle 🧩"]
                }

        # 2. Entertainment Check
        if any(k in text for k in ["joke", "funny", "riddle", "puzzle", "music", "song"]):
            if "joke" in text:
                joke = random.choice([
                    "Why don't scientists trust atoms? Because they make up everything! 😄",
                    "Why did the scarecrow win an award? Because he was outstanding in his field! 🌾",
                    "What do you call a fake noodle? An impasta! 🍝"
                ])
                return {"protocol": "ENTERTAINMENT", "reply": f"Here is a lighthearted joke for you! 😄\n\n{joke}", "options": ["Tell me another joke 😄", "Give me a puzzle 🧩", "I need to vent 💬"]}
            elif "puzzle" in text or "riddle" in text:
                puzzle = "Riddle: What has keys but can't open locks, space but no room, and allows you to enter but not go in? Answer: A Keyboard! ⌨️"
                return {"protocol": "ENTERTAINMENT", "reply": f"Here is a fun brain puzzle! 🧩\n\n{puzzle}", "options": ["Give me another puzzle 🧩", "Hear a joke 😄", "Play me a song 🎵"]}
            else:
                music = "🎵 Music Suggestion: 'Weightless' by Marconi Union — scientifically proven to reduce stress levels."
                return {"protocol": "ENTERTAINMENT", "reply": f"{music}\n\n[TRIGGER_MUSIC_PLAYER]", "options": ["Play another song 🎵", "Hear a joke 😄", "I need to vent 💬"]}

        # 3. Casual Banter Check
        greetings = ["hi", "hii", "hello", "hey", "good morning", "good evening", "how are you", "who are you"]
        if text in greetings or len(text.split()) <= 2:
            return {
                "protocol": "CASUAL_BANTER",
                "reply": "Hello! It is wonderful to connect with you today. I am Keffi, your clinical AI companion. How is your day going so far?",
                "options": ["I need to vent 💬", "Hear a joke 😄", "Give me a puzzle 🧩"]
            }

        # 4. Deep Clinical Counseling (Default for emotional or complex queries)
        import keffi_own_clinical_dataset_engine as own_engine
        return own_engine.generate_own_keffi_response(user_input)

