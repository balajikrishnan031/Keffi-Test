import os
from playwright.sync_api import sync_playwright

out_dir = r'e:\Keffi Ai\Documentation\extracted_report_images'
os.makedirs(out_dir, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--disable-web-security', '--disable-remote-fonts'])
    context = browser.new_context(viewport={'width': 1280, 'height': 800})
    page = context.new_page()

    # 1. Landing Page
    print("Capturing 1. Landing Page...")
    page.goto("http://localhost:5173/", wait_until="commit")
    page.wait_for_timeout(2000)
    page.screenshot(path=os.path.join(out_dir, "live_landing_page.png"), timeout=0)
    print("   [OK] Landing Page captured!")

    # 2. Patient Sanctuary Chatting Page
    print("Capturing 2. Patient Sanctuary Chatting Page...")
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
    page.wait_for_timeout(3000)
    page.screenshot(path=os.path.join(out_dir, "live_sanctuary_chat.png"), timeout=0)
    print("   [OK] Patient Sanctuary Chat Page captured!")

    # 3. Admin Clinical Hub Dashboard
    print("Capturing 3. Admin Clinical Hub Dashboard...")
    page.goto("http://localhost:5173/", wait_until="commit")
    # Click Clinical Hub or login admin
    try:
        page.evaluate("""() => {
            localStorage.clear();
        }""")
        page.goto("http://localhost:5173/", wait_until="commit")
        page.click("text=Clinical Hub")
        page.wait_for_timeout(2000)
        page.screenshot(path=os.path.join(out_dir, "live_admin_clinical_hub.png"), timeout=0)
        print("   [OK] Admin Clinical Hub captured!")
    except Exception as e:
        print("   [WARN] Admin click fallback:", e)

    browser.close()

print("[SUCCESS] All Pristine Live UI Screenshots Captured!")
