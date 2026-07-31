"""
Keffi AI - Physiological Emotion Sync & IoT Biometric Telemetry Engine
Processes real-time sensor streams (ESP32 Heart Rate BPM, Heart Rate Variability HRV, Galvanic Skin Response GSR).
Triggers proactive calming audio/somatic interventions when stress parameters spike.
"""

from datetime import datetime

def process_biometric_telemetry(patient_id: str, heart_rate_bpm: float = 72.0, hrv_ms: float = 45.0, gsr_microsiemens: float = 3.5) -> dict:
    """
    Evaluates real-time IoT sensor telemetry stream from wearable ESP32/smartwatch.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Stress threshold classification
    if heart_rate_bpm >= 100.0 or gsr_microsiemens >= 8.0:
        autonomic_state = "High Sympathetic Arousal (Panic / Acute Stress)"
        proactive_intervention_required = True
        care_nudge = f"Your heart rate seems elevated ({round(heart_rate_bpm, 1)} BPM). Let's take a slow deep breath together."
    elif heart_rate_bpm >= 85.0 or gsr_microsiemens >= 5.5:
        autonomic_state = "Moderate Physiological Stress"
        proactive_intervention_required = False
        care_nudge = "Elevated tension detected. Consider relaxing your shoulders."
    else:
        autonomic_state = "Parasympathetic Resting State"
        proactive_intervention_required = False
        care_nudge = "Physiological signals are calm and stable."

    return {
        "patient_id": patient_id,
        "timestamp": timestamp,
        "telemetry": {
            "heart_rate_bpm": round(heart_rate_bpm, 1),
            "hrv_ms": round(hrv_ms, 1),
            "gsr_microsiemens": round(gsr_microsiemens, 2)
        },
        "autonomic_state": autonomic_state,
        "proactive_intervention_required": proactive_intervention_required,
        "care_nudge": care_nudge
    }
