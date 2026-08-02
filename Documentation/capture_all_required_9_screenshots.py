import os
from playwright.sync_api import sync_playwright

out_dir = r'e:\Keffi Ai\Documentation\extracted_report_images'
os.makedirs(out_dir, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--disable-web-security', '--disable-remote-fonts'])
    context = browser.new_context(viewport={'width': 1280, 'height': 800})
    page = context.new_page()

    # 1. LANDING PAGE SCREENSHOTS (3)
    print("1. Capturing Landing Page 3 Screenshots...")
    page.goto("http://localhost:5173/", wait_until="commit")
    page.wait_for_timeout(2000)
    page.screenshot(path=os.path.join(out_dir, "shot_1_landing_hero.png"), timeout=0)

    # Scroll to Silent Crisis
    page.evaluate("window.scrollBy(0, 700)")
    page.wait_for_timeout(1000)
    page.screenshot(path=os.path.join(out_dir, "shot_2_landing_silent_crisis.png"), timeout=0)

    # Scroll to Tech Architecture
    page.evaluate("window.scrollBy(0, 1800)")
    page.wait_for_timeout(1000)
    page.screenshot(path=os.path.join(out_dir, "shot_3_landing_tech_architecture.png"), timeout=0)

    # 2. LOGIN PAGE SCREENSHOT (1)
    print("2. Capturing Patient Login Page...")
    page.goto("http://localhost:5173/", wait_until="commit")
    page.evaluate("localStorage.clear()")
    page.goto("http://localhost:5173/", wait_until="commit")
    page.click("text=Log in")
    page.wait_for_timeout(1500)
    page.screenshot(path=os.path.join(out_dir, "shot_4_patient_login.png"), timeout=0)

    # 3. CHAT PAGE & MENU SIDEBAR SCREENSHOTS (2)
    print("3. Capturing Active Chat & Menu Sidebar...")
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
    try:
        page.click("text=Anxious")
        page.wait_for_timeout(2000)
    except Exception as e:
        print("Anxious click fallback:", e)
    page.screenshot(path=os.path.join(out_dir, "shot_5_sanctuary_active_chat.png"), timeout=0)

    # Menu Sidebar click
    try:
        page.click("text=Peace Log")
        page.wait_for_timeout(1500)
    except Exception as e:
        pass
    page.screenshot(path=os.path.join(out_dir, "shot_6_sanctuary_menu_sidebar.png"), timeout=0)

    # 4. ADMIN CLINICAL HUB SCREENSHOTS (3)
    print("4. Capturing Admin Clinical Hub 3 Screenshots...")
    page.evaluate("""() => {
        localStorage.setItem('keffi_user', JSON.stringify({
            name: 'Dr. Sivanesh',
            role: 'admin'
        }));
    }""")
    page.goto("http://localhost:5173/", wait_until="commit")
    page.wait_for_timeout(2500)
    page.screenshot(path=os.path.join(out_dir, "shot_7_admin_dashboard_roster.png"), timeout=0)

    # Days Inactive metrics scroll
    page.evaluate("window.scrollBy(0, 400)")
    page.wait_for_timeout(1000)
    page.screenshot(path=os.path.join(out_dir, "shot_8_admin_days_inactive_metrics.png"), timeout=0)

    # Transcript Inspector scroll
    page.evaluate("window.scrollBy(0, 600)")
    page.wait_for_timeout(1000)
    page.screenshot(path=os.path.join(out_dir, "shot_9_admin_transcript_inspector.png"), timeout=0)

    browser.close()

print("[SUCCESS] All 9 Required Live Screenshots Captured!")
