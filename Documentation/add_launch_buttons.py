import os

def add_buttons():
    print("=== ADDING VIDEO CALL LAUNCH BUTTONS TO PATIENT INTERFACE ===")

    app_path = r"e:\Keffi Ai\Platform\Frontend\src\App.jsx"
    with open(app_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Search for header action area or buttons
    if "startVideoCall" in content and "Start Live Video Call" not in content:
        btn_jsx = '''
        <button onClick={startVideoCall} className="px-4 py-2 rounded-2xl bg-gradient-to-r from-teal-600 to-emerald-600 hover:from-teal-700 hover:to-emerald-700 text-white font-bold text-xs shadow-lg shadow-teal-500/20 flex items-center gap-2 transition-all cursor-pointer hover:scale-102">
          <PhoneCall size={16} /> Start Live Video Call (Camera + Voice AI)
        </button>
        '''
        # Add button in main header or top bar
        content = content.replace('<button onClick={() => setView(\'landing\')}', btn_jsx + '\n<button onClick={() => setView(\'landing\')}')

    with open(app_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("[SUCCESS] Added Video Call launch button to header!")

if __name__ == "__main__":
    add_buttons()
