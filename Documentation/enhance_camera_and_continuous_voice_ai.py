import os
import re

def enhance_camera_and_voice():
    print("=== ENHANCING CAMERA VIDEO SIZE & CONTINUOUS VOICE CONVERSATION LOOP IN APP.JSX ===")

    app_path = r"e:\Keffi Ai\Platform\Frontend\src\App.jsx"
    with open(app_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update Camera Tracker component size & styling to make face large, crisp & 100% visible
    # Find CameraEmotionTracker or video rendering elements
    old_camera_box = r'className="w-24 h-24 rounded-full overflow-hidden'
    new_camera_box = r'className="w-80 h-80 rounded-[2.5rem] border-4 border-[#3A7070]/40 shadow-2xl overflow-hidden'
    content = re.sub(old_camera_box, new_camera_box, content)

    # Replace small camera container styles
    content = content.replace("w-28 h-28", "w-80 h-80")
    content = content.replace("w-32 h-32", "w-80 h-80")

    # 2. Update Speech Synthesis onend handler to AUTOMATICALLY restart mic for continuous back-and-forth conversation
    speech_onend_handler = '''
          utterance.onend = () => {
            // Continuous Back-and-Forth Loop: Auto-restart mic to listen for patient's next question!
            if (recognitionRef.current && isVoiceEnabled) {
              try {
                setTimeout(() => {
                  recognitionRef.current.start();
                  setIsRecording(true);
                }, 400);
              } catch (e) {
                console.log("Mic auto-restart:", e);
              }
            }
          };
'''

    if "utterance.onend =" not in content:
        content = content.replace("window.speechSynthesis.speak(utterance);", speech_onend_handler + "\n          window.speechSynthesis.speak(utterance);")

    with open(app_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("[SUCCESS] Camera size expanded to 80x80 (large HD face view) & Continuous Voice Loop implemented!")

if __name__ == "__main__":
    enhance_camera_and_voice()
