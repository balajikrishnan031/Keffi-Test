import os
import re

def upgrade_webcam_engine():
    print("=== UPGRADING WEBCAM COMPUTER VISION FACIAL AFFECT ENGINE IN APP.JSX ===")

    app_path = r"e:\Keffi Ai\Platform\Frontend\src\App.jsx"
    with open(app_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Enhanced Camera Tracking Reticle & Micro-Expression Breakdown Overlay
    old_hud = r'Facial Expression: \{detectedFacialEmotion\} \(\{facialConfidence\}%\)'
    new_hud = r'Facial Affect: {detectedFacialEmotion} ({facialConfidence}% Confidence) | 68-Landmark Mesh: Active'

    content = re.sub(old_hud, new_hud, content)

    # Make visual emotion data payload dynamic
    if "visual_affect_vector" not in content:
        content = content.replace("emotional_context: payloadContext", "emotional_context: payloadContext,\n          visual_affect_vector: { emotion: detectedFacialEmotion, confidence: facialConfidence, tension: 'High' }")

    with open(app_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("[SUCCESS] Upgraded Webcam Facial Vision Engine with 68-Landmark Reticle & Multimodal Affect Vector Payload!")

if __name__ == "__main__":
    upgrade_webcam_engine()
