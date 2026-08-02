import os
from playwright.sync_api import sync_playwright

out_dir = r'e:\Keffi Ai\Documentation\extracted_report_images'
os.makedirs(out_dir, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--disable-web-security', '--disable-remote-fonts'])
    context = browser.new_context(viewport={'width': 1280, 'height': 800})
    page = context.new_page()

    # 1. Landing Page
    print("1. Capturing Landing Page...")
    page.goto("http://localhost:5173/", wait_until="commit")
    page.wait_for_timeout(2000)
    page.screenshot(path=os.path.join(out_dir, "live_landing_page.png"), timeout=0)

    # 2. Sanctuary Active Chatting Interface
    print("2. Capturing Sanctuary Active Chatting Page...")
    page.goto("http://localhost:5173/", wait_until="commit")
    page.evaluate("""() => {
        localStorage.setItem('keffi_user', JSON.stringify({
            name: 'Balaji P',
            phone: '9342636595',
            email: 'balaji@gmail.com',
            patient_id: 'P-934263',
            role: 'patient'
        }));
    }""")
    page.goto("http://localhost:5173/", wait_until="commit")
    page.wait_for_timeout(2000)
    # Click Anxious mood button
    try:
        page.click("text=Anxious")
        page.wait_for_timeout(2500)
    except Exception as e:
        print("Mood button click:", e)
    page.screenshot(path=os.path.join(out_dir, "live_sanctuary_chat.png"), timeout=0)

    # 3. Admin Clinical Hub Dashboard
    print("3. Capturing Admin Clinical Hub Dashboard...")
    page.evaluate("""() => {
        localStorage.setItem('keffi_user', JSON.stringify({
            name: 'Dr. Sivanesh',
            role: 'admin'
        }));
    }""")
    page.goto("http://localhost:5173/", wait_until="commit")
    page.wait_for_timeout(2500)
    page.screenshot(path=os.path.join(out_dir, "live_admin_clinical_hub.png"), timeout=0)

    browser.close()

print("[SUCCESS] All Interactive UI Screenshots Captured!")
