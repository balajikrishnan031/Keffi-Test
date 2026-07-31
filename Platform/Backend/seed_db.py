"""
Keffi Clinical Database Seeder Script
Populates keffi_clinical.db with rich initial clinical records, test patients,
biometric telemetry streams, cognitive distortion logs, and chat histories.
"""

import sys
import os
from datetime import datetime, timedelta

# Ensure parent path is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from clinical_db import (
    SessionLocal, Patient, ChatMessage, MoodCheckIn,
    CognitiveDistortionLog, BiometricTelemetryLog, VoiceProsodyLog, Base, engine
)

def seed_database():
    print("=== SEEDING KEFFI CLINICAL DATABASE ===")
    # Recreate tables to ensure schema match
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Seed Patients
        patients = [
            Patient(patient_id="P-101", name="Anand Sharma", phone="+91 98765 43210", email="anand@example.com", dob="1998-05-14", gender="Male", place="Chennai", mhq_score=68.5, depression_level="Low", assigned_doctor="Dr. R. Sivanesh", mhq_trend="Improving", attrition_probability=0.08),
            Patient(patient_id="P-102", name="Balaji P", phone="+91 98765 43211", email="balaji@example.com", dob="2001-01-01", gender="Male", place="Panruti", mhq_score=52.0, depression_level="Moderate", assigned_doctor="Dr. R. Sivanesh", mhq_trend="Stable", attrition_probability=0.15),
            Patient(patient_id="P-103", name="Mathu (Madhumathi S)", phone="+91 98765 43212", email="mathu@example.com", dob="2002-03-22", gender="Female", place="Panruti", mhq_score=75.0, depression_level="Low", assigned_doctor="Dr. R. Sivanesh", mhq_trend="Improving", attrition_probability=0.05),
            Patient(patient_id="P-104", name="Malini V", phone="+91 98765 43213", email="malini@example.com", dob="2002-08-11", gender="Female", place="Panruti", mhq_score=64.0, depression_level="Low", assigned_doctor="Dr. R. Sivanesh", mhq_trend="Stable", attrition_probability=0.10)
        ]
        for p in patients:
            existing = db.query(Patient).filter(Patient.patient_id == p.patient_id).first()
            if not existing:
                db.add(p)
                print(f"  [PATIENT ADDED] {p.patient_id} - {p.name}")

        # 2. Seed Chat Messages for P-102
        messages = [
            ChatMessage(patient_id="P-102", message="I feel overwhelmed with final semester deadlines.", ai_reply="I hear how much pressure you're under. It's completely valid to feel overwhelmed when deadlines pile up.", bert_emotion="sadness", clinical_state="Overwhelmed / Academic Stress", clinical_category="Anxiety", mhq_before=50.0, mhq_after=52.0, mhq_delta=2.0),
            ChatMessage(patient_id="P-102", message="Can you give me a grounding exercise?", ai_reply="Let's practice 4-7-8 breathing together. Breathe in for 4 seconds, hold for 7, and exhale slowly for 8 seconds.", bert_emotion="fear", clinical_state="Mindfulness / Grounding", clinical_category="Intervention", mhq_before=52.0, mhq_after=56.0, mhq_delta=4.0)
        ]
        for msg in messages:
            db.add(msg)

        # 3. Seed Biometric Telemetry Logs
        biometrics = [
            BiometricTelemetryLog(patient_id="P-102", heart_rate_bpm=72.5, hrv_ms=58.2, gsr_microsiemens=2.4, panic_flag=False),
            BiometricTelemetryLog(patient_id="P-102", heart_rate_bpm=108.0, hrv_ms=32.1, gsr_microsiemens=6.8, panic_flag=True)
        ]
        for b in biometrics:
            db.add(b)

        # 4. Seed Cognitive Distortion Logs
        distortions = [
            CognitiveDistortionLog(patient_id="P-102", distortion_type="Catastrophizing", user_thought="If I fail this review, my whole career is over.", reframed_thought="One review is an opportunity for feedback, not the end of my career."),
            CognitiveDistortionLog(patient_id="P-102", distortion_type="All-or-Nothing Thinking", user_thought="Everything must be perfect or it's a failure.", reframed_thought="Progress is better than perfection. My hard work has substantial value.")
        ]
        for d in distortions:
            db.add(d)

        db.commit()
        print("  [SUCCESS] Database Seeded & Rock-Solid!")

    except Exception as e:
        db.rollback()
        print(f"  [ERROR] Database seeding failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
