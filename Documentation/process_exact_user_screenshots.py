import os
import glob
from PIL import Image

def process_and_crop_user_screenshots():
    media_dir = r'C:\Users\BALAJI\.gemini\antigravity-ide\brain\c4b68b25-b97d-4a24-b1ab-233ccab13010\.tempmediaStorage'
    out_dir = r'e:\Keffi Ai\Documentation\extracted_report_images'
    os.makedirs(out_dir, exist_ok=True)

    files = glob.glob(os.path.join(media_dir, '*.png'))
    files.sort(key=os.path.getmtime, reverse=True)

    print(f"Found {len(files)} total media files. Processing latest 5 uploaded images...")

    latest_5 = files[:5]
    latest_5.reverse() # Oldest to newest order of upload

    names = [
        "user_screenshot_1_hero.png",
        "user_screenshot_2_silent_crisis.png",
        "user_screenshot_3_why_created.png",
        "user_screenshot_4_clinical_models.png",
        "user_screenshot_5_tech_stack.png"
    ]

    for idx, fpath in enumerate(latest_5):
        if idx >= len(names):
            break
        img = Image.open(fpath)
        w, h = img.size
        # Crop out top browser bar (top 140 pixels) if h > 500
        if h > 500:
            crop_box = (0, 140, w, h)
            img_cropped = img.crop(crop_box)
        else:
            img_cropped = img
        
        save_path = os.path.join(out_dir, names[idx])
        img_cropped.save(save_path)
        print(f"[SUCCESS] Cropped and saved {names[idx]} (Size: {img_cropped.size})")

if __name__ == "__main__":
    process_and_crop_user_screenshots()
