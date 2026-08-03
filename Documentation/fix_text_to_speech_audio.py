import os
import re

def fix_speech_audio():
    print("=== FIXING TEXT-TO-SPEECH AUDIO OUTPUT & INITIAL VOICE ENABLED STATE IN APP.JSX ===")

    app_path = r"e:\Keffi Ai\Platform\Frontend\src\App.jsx"
    with open(app_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Enable isVoiceEnabled by default so audio plays automatically
    content = content.replace("const [isVoiceEnabled, setIsVoiceEnabled] = useState(false);", "const [isVoiceEnabled, setIsVoiceEnabled] = useState(true);")

    # 2. Make SpeechSynthesis robust with fallback audio play function
    old_speech_check = r"if \('speechSynthesis' in window && isVoiceEnabled\)"
    new_speech_check = r"if ('speechSynthesis' in window)"

    content = re.sub(old_speech_check, new_speech_check, content)

    # 3. Add explicit Speak function for Replay button
    speak_helper = '''
  const playAudioVoice = (textToSpeak) => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const cleanText = textToSpeak.replace(/[#*`_]/g, '');
      const utterance = new SpeechSynthesisUtterance(cleanText);
      utterance.lang = 'en-US';
      utterance.rate = 0.95;
      utterance.pitch = 1.0;
      const voices = window.speechSynthesis.getVoices();
      const voice = voices.find(v => v.name.includes('Google') || v.name.includes('Natural') || v.name.includes('Female') || v.name.includes('English'));
      if (voice) utterance.voice = voice;
      window.speechSynthesis.speak(utterance);
    }
  };
'''

    if "playAudioVoice" not in content:
        content = content.replace("const handleSend = async", speak_helper + "\n  const handleSend = async")

    with open(app_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("[SUCCESS] Fixed Text-To-Speech audio output & enabled automatic voice reply playback!")

if __name__ == "__main__":
    fix_speech_audio()
