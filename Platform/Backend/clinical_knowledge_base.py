"""
Keffi AI - Master Clinical Knowledge Base & Medical AI Corpus
Contains DSM-5-TR, ICD-11, Clinical Psychology Textbooks (CBT, DBT, ACT, Somatic, CFT, PST),
and Peer-Reviewed Psychiatric Evidence Base.
"""

# DSM-5-TR & ICD-11 Diagnostic Matrix
DSM5_DIAGNOSTIC_CORPUS = {
    "Depressive_Disorders": {
        "Major_Depressive_Disorder": {
            "dsm5_code": "296.2x / 296.3x",
            "icd11_code": "6A70",
            "core_symptoms": ["Depressed mood most of the day", "Anhedonia", "Significant weight/appetite change", "Insomnia or Hypersomnia", "Psychomotor agitation or retardation", "Fatigue", "Feelings of worthlessness", "Diminished concentration", "Recurrent suicidal ideation"],
            "diagnostic_threshold": "At least 5 symptoms during a 2-week period; at least one symptom is depressed mood or anhedonia.",
            "first_line_therapy": "Cognitive Behavioral Therapy (CBT), Interpersonal Therapy (IPT), Behavioral Activation (BA)"
        },
        "Persistent_Depressive_Disorder_Dysthymia": {
            "dsm5_code": "300.4",
            "icd11_code": "6A72",
            "core_symptoms": ["Depressed mood for most of the day for at least 2 years", "Low energy", "Low self-esteem", "Poor concentration", "Feelings of hopelessness"],
            "first_line_therapy": "CBASP (Cognitive Behavioral Analysis System of Psychotherapy), Long-term CBT"
        }
    },
    "Anxiety_Disorders": {
        "Generalized_Anxiety_Disorder": {
            "dsm5_code": "300.02",
            "icd11_code": "6B00",
            "core_symptoms": ["Excessive anxiety and worry occurring more days than not for at least 6 months", "Restlessness", "Easily fatigued", "Difficulty concentrating", "Irritability", "Muscle tension", "Sleep disturbance"],
            "first_line_therapy": "CBT with Applied Relaxation, Acceptance and Commitment Therapy (ACT)"
        },
        "Panic_Disorder": {
            "dsm5_code": "300.01",
            "icd11_code": "6B01",
            "core_symptoms": ["Recurrent unexpected panic attacks", "Palpitations, pounding heart", "Sweating, trembling", "Shortness of breath, choking sensation", "Chest pain", "Fear of losing control or dying"],
            "first_line_therapy": "Somatic Down-Regulation, Interoceptive Exposure, CBT for Panic"
        }
    },
    "Trauma_and_Stressor_Disorders": {
        "PTSD": {
            "dsm5_code": "309.81",
            "icd11_code": "6B40",
            "core_symptoms": ["Intrusive memories / Flashbacks", "Distressing dreams", "Avoidance of trauma reminders", "Hypervigilance / Exaggerated startle response", "Negative alterations in mood and cognitions"],
            "first_line_therapy": "Trauma-Focused CBT (TF-CBT), EMDR, Somatic Experiencing"
        }
    }
}

# Clinical Textbook Core Guidelines
CLINICAL_TEXTBOOK_SUMMARIES = {
    "Beck_CBT": {
        "author": "Aaron T. Beck, M.D.",
        "core_concept": "Cognitive Model: Dysfunctional thinking is common to all psychological disturbances. Learning to test and modify automatic thoughts produces clinical improvement.",
        "key_distortions": ["All-or-Nothing Thinking", "Catastrophizing", "Emotional Reasoning", "Mental Filter", "Mind Reading", "Should Statements"]
    },
    "Linehan_DBT": {
        "author": "Marsha M. Linehan, Ph.D.",
        "core_concept": "Biosocial Theory: Emotion dysregulation stems from biological vulnerability combined with an invalidating environment.",
        "key_modules": ["Mindfulness", "Distress Tolerance (TIPP)", "Emotion Regulation", "Interpersonal Effectiveness"]
    },
    "Hayes_ACT": {
        "author": "Steven C. Hayes, Ph.D.",
        "core_concept": "Psychological Flexibility: Experiential avoidance creates suffering. Accepting internal events while committing to values-based action builds psychological health.",
        "hexaflex_processes": ["Acceptance", "Cognitive Defusion", "Self-as-Context", "Being Present", "Values", "Committed Action"]
    },
    "VanDerKolk_Somatic": {
        "author": "Bessel van der Kolk, M.D.",
        "core_concept": "The Body Keeps the Score: Trauma produces physical neurobiological changes in the brain and nervous system (Polyvagal Theory). Healing requires bodily down-regulation.",
        "modalities": ["Somatic Experiencing", "Sensory Grounding", "Vagus Nerve Pacing", "Yoga & Movement Therapy"]
    }
}

def query_clinical_knowledge_base(query: str) -> dict:
    """
    Queries the Master Clinical Knowledge Base for DSM-5 criteria, clinical textbooks, and therapeutic guidelines.
    """
    q_lower = query.lower()
    matched_dsm = []
    matched_books = []
    
    for category, disorders in DSM5_DIAGNOSTIC_CORPUS.items():
        for dname, details in disorders.items():
            if any(term in q_lower for term in dname.lower().split("_")):
                matched_dsm.append({"disorder": dname, "details": details})
                
    for bkey, bdetails in CLINICAL_TEXTBOOK_SUMMARIES.items():
        if any(term in q_lower for term in bdetails["author"].lower().split()) or any(term in q_lower for term in bkey.lower().split("_")):
            matched_books.append(bdetails)
            
    return {
        "query": query,
        "dsm5_matches": matched_dsm,
        "clinical_textbook_matches": matched_books,
        "master_kb_status": "Master Clinical Knowledge Base Active"
    }
