import os
import re

def fix_new_chat():
    print("=== FIXING FRESH NEW CHAT ON USER LOGIN IN FRONTEND APP.JSX ===")

    app_path = r"e:\Keffi Ai\Platform\Frontend\src\App.jsx"
    with open(app_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. On Login / Auth state change, initialize fresh empty messages array
    # Replace initial messages state loading from localStorage to start fresh on login
    old_messages_init = r"const \[messages, setMessages\] = useState\(\(\) => \{[^}]*\}\);"
    new_messages_init = "const [messages, setMessages] = useState([]);"

    content = re.sub(old_messages_init, new_messages_init, content)

    # 2. In handleLogin / handleSignup, explicitly reset messages to [] and clear transient chat state
    if "setMessages([])" not in content:
        # Find setView('patient') or login success handler
        content = content.replace("setView('patient');", "setMessages([]); localStorage.removeItem('keffi_active_messages'); setView('patient');")

    # 3. Add a "➕ New Chat" button handler inside PatientChat so user can start a new chat anytime
    if "handleStartNewChat" not in content:
        new_chat_fn = '''
  const handleStartNewChat = () => {
    setMessages([]);
    setInput('');
    setMoodSet(false);
    localStorage.removeItem('keffi_active_messages');
    alert("New chat session started!");
  };
'''
        content = content.replace("const [input, setInput] = useState('');", "const [input, setInput] = useState('');\n" + new_chat_fn)

    with open(app_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("[SUCCESS] Updated App.jsx so every user login opens a fresh, clean NEW CHAT!")

if __name__ == "__main__":
    fix_new_chat()
