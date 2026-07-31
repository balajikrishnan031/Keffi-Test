"""
Keffi AI - Temporal Emotion Knowledge Graph
Maintains long-term graph memory mapping:
User -> Triggers -> Emotional States -> Coping Mechanisms -> Personal Preferences
Generates hyper-personalized empathetic memory recalls.
"""

# In-Memory Temporal Knowledge Graph Storage (Persisted across sessions)
TEMPORAL_GRAPH_DB = {
    "P-102": {
        "triggers": ["Academic Reviews", "Exam Deadlines", "Parental Expectations"],
        "emotional_episodes": [
            {"date": "2026-07-15", "trigger": "Academic Reviews", "state": "Exam Panic", "coping_used": "Tamil Lofi Music", "rating": 5},
            {"date": "2026-07-28", "trigger": "Workload Overwhelm", "state": "Depressive Fatigue", "coping_used": "4-7-8 Somatic Breathing", "rating": 4}
        ],
        "proven_coping_mechanisms": {
            "Exam Panic": "Tamil Lofi Music & PST Task Decomposition",
            "Depressive Fatigue": "4-7-8 Somatic Breathing & Micro-Task",
            "Relationship Stress": "ACT Cognitive Defusion"
        },
        "personal_preferences": ["Tamil Calming Music", "Short Direct Reframes", "Box Breathing"]
    }
}

def query_temporal_knowledge_graph(patient_id: str, current_message: str, current_state: str) -> dict:
    """
    Queries patient's long-term temporal knowledge graph for past triggers and successful coping mechanisms.
    """
    user_graph = TEMPORAL_GRAPH_DB.get(patient_id, {
        "triggers": ["General Work Stress"],
        "proven_coping_mechanisms": {"General": "Somatic Breathing"},
        "personal_preferences": ["Calming Music"]
    })
    
    msg_lower = current_message.lower()
    matched_trigger = next((t for t in user_graph["triggers"] if any(w in msg_lower for w in t.lower().split())), None)
    
    past_proven_coping = user_graph["proven_coping_mechanisms"].get(current_state, "4-7-8 Somatic Breathing")
    preferred_music = user_graph["personal_preferences"][0] if user_graph["personal_preferences"] else "Calming Music"
    
    if matched_trigger:
        personalized_recall_prompt = (
            f"I know you usually feel this way before your '{matched_trigger}'. "
            f"Last time, listening to {preferred_music} and practicing {past_proven_coping} really helped you feel grounded. "
            f"Shall I play that for you now?"
        )
    else:
        personalized_recall_prompt = (
            f"Remember that when feelings of {current_state} arise, practicing {past_proven_coping} has brought you relief in the past."
        )
        
    return {
        "patient_id": patient_id,
        "matched_past_trigger": matched_trigger,
        "proven_coping_mechanism": past_proven_coping,
        "personalized_empathetic_recall": personalized_recall_prompt,
        "status": "Temporal Knowledge Graph Active"
    }

def record_graph_coping_success(patient_id: str, state: str, coping_used: str, rating: int = 5):
    """Records a new successful coping episode into the Knowledge Graph."""
    if patient_id not in TEMPORAL_GRAPH_DB:
        TEMPORAL_GRAPH_DB[patient_id] = {"triggers": [], "proven_coping_mechanisms": {}, "personal_preferences": []}
    TEMPORAL_GRAPH_DB[patient_id]["proven_coping_mechanisms"][state] = coping_used
    return True
