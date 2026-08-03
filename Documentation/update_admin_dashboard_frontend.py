import os
import re

def update_frontend_app():
    print("=== UPDATING FRONTEND APP.JSX FOR CLEAN PROFESSIONAL ADMIN CLINICAL HUB ===")

    app_path = r"e:\Keffi Ai\Platform\Frontend\src\App.jsx"
    with open(app_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update adminTabs to remove script fonts and multi-colored backgrounds
    old_tabs = r"""  const adminTabs = \[
    \{ id: 'overview', label: 'System Overview', icon: Activity, fontClass: 'font-greatvibes text-\[22px\] leading-none py-1\.5 font-normal tracking-wide', activeBg: 'bg-teal-700 text-white shadow-lg shadow-teal-500/25 scale-102', inactiveColor: 'text-teal-700 hover:text-teal-900 hover:bg-teal-500/5' \},
    \{ id: 'roster', label: 'Patient Roster', icon: Users, fontClass: 'font-playball text-\[17px\] font-bold tracking-wide', activeBg: 'bg-blue-700 text-white shadow-lg shadow-blue-500/25 scale-102', inactiveColor: 'text-blue-700 hover:text-blue-900 hover:bg-blue-500/5' \},
    \{ id: 'inactive', label: 'Inactive Patients', icon: Frown, fontClass: 'font-alexbrush text-\[24px\] leading-none py-1 font-normal tracking-wide', activeBg: 'bg-rose-600 text-white shadow-lg shadow-rose-500/25 scale-102', inactiveColor: 'text-rose-700 hover:text-rose-900 hover:bg-rose-500/5' \},
    \{ id: 'analytics', label: 'NLP Analytics', icon: PieChart, fontClass: 'font-pacifico text-\[14px\] leading-none font-normal', activeBg: 'bg-purple-700 text-white shadow-lg shadow-purple-500/25 scale-102', inactiveColor: 'text-purple-700 hover:text-purple-900 hover:bg-purple-500/5' \},
    \{ id: 'therapists', label: 'Therapists Allocation', icon: Shield, fontClass: 'font-sacramento text-\[25px\] leading-none font-bold tracking-wide', activeBg: 'bg-amber-700 text-white shadow-lg shadow-amber-500/25 scale-102', inactiveColor: 'text-amber-800 hover:text-amber-900 hover:bg-amber-500/5' \},
    \{ id: 'settings', label: 'System Settings', icon: Settings, fontClass: 'font-allura text-\[25px\] leading-none font-normal tracking-wide', activeBg: 'bg-emerald-700 text-white shadow-lg shadow-emerald-500/25 scale-102', inactiveColor: 'text-emerald-700 hover:text-emerald-900 hover:bg-emerald-500/5' \},
  \];"""

    new_tabs = """  const adminTabs = [
    { id: 'overview', label: 'System Overview', icon: Activity, fontClass: 'font-sans font-bold text-sm tracking-wide', activeBg: 'bg-[#2C5555] text-white shadow-md scale-102', inactiveColor: 'text-[#2C5555] hover:bg-[#2C5555]/10' },
    { id: 'roster', label: 'Patient Roster', icon: Users, fontClass: 'font-sans font-bold text-sm tracking-wide', activeBg: 'bg-[#2C5555] text-white shadow-md scale-102', inactiveColor: 'text-[#2C5555] hover:bg-[#2C5555]/10' },
    { id: 'inactive', label: 'Inactive Patients', icon: Frown, fontClass: 'font-sans font-bold text-sm tracking-wide', activeBg: 'bg-[#2C5555] text-white shadow-md scale-102', inactiveColor: 'text-[#2C5555] hover:bg-[#2C5555]/10' },
    { id: 'analytics', label: 'NLP Analytics', icon: PieChart, fontClass: 'font-sans font-bold text-sm tracking-wide', activeBg: 'bg-[#2C5555] text-white shadow-md scale-102', inactiveColor: 'text-[#2C5555] hover:bg-[#2C5555]/10' },
    { id: 'therapists', label: 'Doctor Appointments', icon: Shield, fontClass: 'font-sans font-bold text-sm tracking-wide', activeBg: 'bg-[#2C5555] text-white shadow-md scale-102', inactiveColor: 'text-[#2C5555] hover:bg-[#2C5555]/10' },
    { id: 'settings', label: 'System Settings', icon: Settings, fontClass: 'font-sans font-bold text-sm tracking-wide', activeBg: 'bg-[#2C5555] text-white shadow-md scale-102', inactiveColor: 'text-[#2C5555] hover:bg-[#2C5555]/10' },
  ];"""

    content = re.sub(old_tabs, new_tabs, content)

    # 2. Replace 127.0.0.1:8000 with Hugging Face live URL and local storage merging
    content = content.replace("http://127.0.0.1:8000", "https://balajikrishnan031-keffi-backend.hf.space")

    with open(app_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("[SUCCESS] Updated App.jsx with clean executive typography and live Hugging Face URL endpoints!")

if __name__ == "__main__":
    update_frontend_app()
