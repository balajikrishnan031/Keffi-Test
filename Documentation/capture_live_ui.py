import os
from playwright.sync_api import sync_playwright

out_dir = r'e:\Keffi Ai\Documentation\extracted_report_images'
os.makedirs(out_dir, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--disable-web-security', '--disable-remote-fonts'])
    context = browser.new_context(viewport={'width': 1280, 'height': 800})
    page = context.new_page()

    # 1. Landing Page
    print("Capturing Landing Page...")
    page.goto("http://localhost:5173/", wait_until="commit")
    page.wait_for_timeout(1000)
    page.screenshot(path=os.path.join(out_dir, "live_landing_page.png"), timeout=0)
    print("Landing Page captured!")

    # 2. Sanctuary / Chatting Page
    print("Capturing Sanctuary Chat Page...")
    page.goto("http://localhost:5173/#/sanctuary", wait_until="commit")
    page.wait_for_timeout(1000)
    page.screenshot(path=os.path.join(out_dir, "live_sanctuary_chat.png"), timeout=0)
    print("Sanctuary Chat captured!")

    # 3. Clinical Hub Dashboard
    print("Capturing Clinical Hub Page...")
    page.goto("http://localhost:5173/#/clinical-hub", wait_until="commit")
    page.wait_for_timeout(1000)
    page.screenshot(path=os.path.join(out_dir, "live_admin_clinical_hub.png"), timeout=0)
    print("Clinical Hub captured!")

    browser.close()

print("[SUCCESS] All Live UI Screenshots Captured!")
