"""
Keffi AI - Cognitive Distortion Mapping Engine (Advanced CBT)
Identifies 10 core CBT psychological distortions in patient text and provides exact reframing prescriptions.
"""

import re

COGNITIVE_DISTORTION_RULES = [
    {
        "distortion": "Catastrophizing",
        "keywords": ["everything is ruined", "life is over", "disaster", "never recover", "worst case", "completely ruined", "inime enakku velaiye kedaikkathu"],
        "definition": "Jumping to the absolute worst possible catastrophic conclusion without considering realistic outcomes.",
        "cbt_prescription": "Examine the evidence: What is the most realistic outcome, and what is one small step to handle it?"
    },
    {
        "distortion": "Black-and-White Thinking (All-or-Nothing)",
        "keywords": ["total failure", "always", "never", "completely useless", "perfect or nothing", "everyone hates me", "nobody cares"],
        "definition": "Viewing situations in rigid binary extremes—either total success or complete failure.",
        "cbt_prescription": "Find the middle ground: What is a 50% truth in this situation rather than 0% or 100%?"
    },
    {
        "distortion": "Overgeneralization",
        "keywords": ["this always happens", "i never get anything right", "every time i try", "history repeats"],
        "definition": "Holding a single negative event as a permanent, endless pattern of defeat.",
        "cbt_prescription": "Challenge the word 'always': Can you recall one time when things went differently?"
    },
    {
        "distortion": "Mental Filter",
        "keywords": ["only one mistake", "ruined the whole thing", "ignored the good", "focusing on the bad"],
        "definition": "Dwelling exclusively on a single negative detail while filtering out all positive aspects.",
        "cbt_prescription": "Zoom out: What are 2 positive or neutral facts you are currently filtering out?"
    },
    {
        "distortion": "Mind Reading",
        "keywords": ["they secretly hate me", "i know what they think", "they think i'm stupid", "talking behind my back"],
        "definition": "Arbitrarily assuming you know what others are thinking without objective evidence.",
        "cbt_prescription": "Ask yourself: Do I have direct proof of their thoughts, or am I projecting my own fears?"
    },
    {
        "distortion": "Fortune Telling",
        "keywords": ["i know i will fail", "going to be a disaster", "no chance i succeed", "doomed"],
        "definition": "Predicting that events will turn out badly as an established fact before they occur.",
        "cbt_prescription": "Stay in the present: Treat this prediction as a thought, not a guaranteed future."
    },
    {
        "distortion": "Personalization",
        "keywords": ["it's all my fault", "i am to blame", "because of me everyone", "my fault entirely"],
        "definition": "Holding yourself personally responsible for events that are outside your full control.",
        "cbt_prescription": "Divide the pie: What external factors or other people also contributed to this outcome?"
    },
    {
        "distortion": "Emotional Reasoning",
        "keywords": ["i feel useless so i am", "i feel stupid so it's true", "my anxiety means danger"],
        "definition": "Assuming that your negative emotions reflect the objective reality of the situation.",
        "cbt_prescription": "Separate feelings from facts: Feelings are real emotional experiences, but they are not objective facts."
    },
    {
        "distortion": "Should Statements",
        "keywords": ["i should have", "i must be", "i ought to", "should never"],
        "definition": "Trying to motivate yourself with rigid 'shoulds' and 'musts', creating guilt and resentment.",
        "cbt_prescription": "Replace 'should' with 'I would prefer to' or 'It is understandable that'."
    },
    {
        "distortion": "Disqualifying the Positive",
        "keywords": ["that compliment doesn't count", "just luck", "anyone could do that", "doesn't mean anything"],
        "definition": "Rejecting positive experiences by insisting they don't count for some arbitrary reason.",
        "cbt_prescription": "Allow positive feedback to land: What if you accepted this accomplishment at face value?"
    }
]

def detect_cognitive_distortions(text: str) -> dict:
    """
    Scans patient text for 10 CBT cognitive distortions and returns structured diagnostic mapping.
    """
    text_lower = text.lower()
    detected = []
    
    for rule in COGNITIVE_DISTORTION_RULES:
        if any(kw in text_lower for kw in rule["keywords"]):
            detected.append({
                "distortion": rule["distortion"],
                "definition": rule["definition"],
                "cbt_prescription": rule["cbt_prescription"]
            })
            
    primary_distortion = detected[0]["distortion"] if detected else "None Detected / Balanced Thinking"
    cbt_reframe_action = detected[0]["cbt_prescription"] if detected else "Maintain objective self-reflection."
    
    return {
        "primary_distortion": primary_distortion,
        "detected_count": len(detected),
        "all_detected": detected,
        "cbt_reframe_action": cbt_reframe_action,
        "status": "Cognitive Distortion Mapping Active"
    }
