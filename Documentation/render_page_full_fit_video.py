import os
import sys
import wave
import contextlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2
import imageio_ffmpeg
import pyttsx3
import subprocess

def build_full_fit_video():
    print("=== BUILDING 100% PAGE-FULL FIT PROJECT JOURNEY DEMO VIDEO (NO BLANK WHITE GAP) ===")

    work_dir = r"e:\Keffi Ai"
    temp_dir = os.path.join(work_dir, "full_fit_temp")
    os.makedirs(temp_dir, exist_ok=True)

    out_mp4_1 = os.path.join(work_dir, "Final_Submission_Pack", "KEFFI_PROJECT_JOURNEY_DEMO.mp4")
    out_mp4_2 = os.path.join(work_dir, "Presentations_and_Extracted_Media", "KEFFI_PROJECT_JOURNEY_DEMO.mp4")

    # Team photos extracted
    photos_dir = os.path.join(work_dir, "extracted_attachments")
    p1 = os.path.join(photos_dir, "20260507_121228PMByGPSMapCamera.jpg")
    p2 = os.path.join(photos_dir, "20260507_121327PMByGPSMapCamera.jpg")
    p3 = os.path.join(photos_dir, "20260512_114133AMByGPSMapCamera.jpg")
    p4 = os.path.join(photos_dir, "20260512_114139AMByGPSMapCamera.jpg")
    p5 = os.path.join(photos_dir, "20260512_114145AMByGPSMapCamera.jpg")
    p6 = os.path.join(photos_dir, "20260512_114150AMByGPSMapCamera.jpg")

    # 3D Diagrams
    img_dir = r"C:\Users\BALAJI\.gemini\antigravity-ide\brain\c4b68b25-b97d-4a24-b1ab-233ccab13010"
    diag_fusion = os.path.join(img_dir, "keffi_3d_multimodal_fusion_architecture_1785782534839.png")
    diag_xai = os.path.join(img_dir, "keffi_3d_shap_lime_explainable_ai_1785782565856.png")

    scenes = [
        {
            "id": 1,
            "title": "TITLE & CREDENTIALS",
            "subtitle": "TNSDC Naan Mudhalvan Niral Thiruvizha 3.0 | ID: NMNTSTD42260064",
            "narrative": "Welcome to the official Project Journey of KEFFI A I, an affective computing platform for continuous mental healthcare, developed by Team Hackers from University College of Engineering Panruti under the guidance of Doctor S Sivanesh for TNSDC Naan Mudhalvan Niral Thiruvizha 3 point 0.",
            "photo": p1,
            "badge": "University College of Engineering Panruti | Team Hackers",
            "target_duration": 20.0
        },
        {
            "id": 2,
            "title": "THE 167-HOUR OUTPATIENT CARE GAP",
            "subtitle": "Unmonitored Vulnerability in Outpatient Psychiatric Treatment",
            "narrative": "Outpatient psychiatric care suffers from a severe structural gap. Outpatients visit therapists for only 1 hour weekly, leaving 167 hours completely unmonitored. Night hours and weekends represent statistically peak vulnerability windows for acute anxiety surges, self harm, and relapse.",
            "photo": p2,
            "badge": "Clinical Need | 167 Unmonitored Hours Between Sessions",
            "target_duration": 22.0
        },
        {
            "id": 3,
            "title": "TEAM RESEARCH & SCIENTIFIC VALIDATION",
            "subtitle": "Peer-Reviewed CBT, ACT & Stanford Woebot Study Foundations",
            "narrative": "To solve this care gap, Team Hackers, Madhumathi, Balaji, and Malini, conducted an extensive literature survey, analyzing peer-reviewed studies by Hofmann, Norcross, and the landmark Stanford Woebot RCT trial to design an evidence-based digital therapeutics platform.",
            "photo": p3,
            "badge": "Team Hackers — Literature Survey & Brainstorming",
            "target_duration": 22.0
        },
        {
            "id": 4,
            "title": "MULTIMODAL SENSING & WEBCAM RETICLE",
            "subtitle": "FINGERS HD Webcam 68-Landmark Vision & ZEBRONICS Voice Prosody",
            "narrative": "Overcoming text-only deception, Keffi A I introduces a Multimodal Sensor Fusion Engine. Real-time computer vision via FINGERS HD Webcam tracks 68 facial landmarks to scan eyebrow contraction, lip mobility, and jaw tension, while ZEBRONICS mic Librosa audio processing measures pitch variance and speech pause duration.",
            "photo": diag_fusion,
            "badge": "Biometric Sensing | FINGERS Webcam Reticle + ZEBRONICS Mic",
            "target_duration": 23.0
        },
        {
            "id": 5,
            "title": "96-EMOTION BERT MODEL & SHAP EXPLAINABLE AI",
            "subtitle": "Fine-Tuned NLP, Smiling Depression & Token Attribution Heatmaps",
            "narrative": "Our fine-tuned BERT transformer model classifies patient text across a 96-state clinical emotion taxonomy with 94 point 8 percent accuracy, detecting hidden Smiling Depression. To eliminate black-box A I risks, SHAP and LIME token attribution heatmaps color-code word weights for clinician auditing.",
            "photo": diag_xai,
            "badge": "Clinical AI Brain | 96-Emotion BERT & SHAP Clinician Auditing",
            "target_duration": 23.0
        },
        {
            "id": 6,
            "title": "PRODUCTION DEVELOPMENT & AUTOMATION",
            "subtitle": "Widescreen Live Video Call, n8n Webhooks & Admin Hub",
            "narrative": "Team Hackers integrated full multimodal video calling with a continuous hands-free voice loop, automated n8n crisis webhooks, and an Executive Admin Clinical Hub featuring 1-click doctor appointment booking, deploying the cloud backend live on Hugging Face Space.",
            "photo": p4,
            "badge": "Team Hackers — System Integration & Cloud Deployment",
            "target_duration": 22.0
        },
        {
            "id": 7,
            "title": "CONCLUSION & SOCIETAL IMPACT",
            "subtitle": "Democratizing 24/7 Affective Mental Healthcare in Tamil Nadu",
            "narrative": "Keffi A I democratizes 24/7 accessible affective mental healthcare across Tamil Nadu, closing the 167-hour outpatient care gap. We express our sincere gratitude to Anna University, TNSDC Naan Mudhalvan, and our Guide Doctor S Sivanesh. Thank you!",
            "photo": p5,
            "badge": "Live Production: keffi-test.vercel.app | Team Hackers",
            "target_duration": 18.0
        }
    ]

    # Generate SOFT HUMAN TONED VOICE OVER (Microsoft Zira tuned to 135 wpm rate)
    print("Generating Soft Human Voiceovers...")
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for v in voices:
        if 'zira' in v.name.lower():
            engine.setProperty('voice', v.id)
            break

    engine.setProperty('rate', 135)
    engine.setProperty('volume', 0.95)

    audio_files = []
    durations = []

    for sc in scenes:
        wav_path = os.path.join(temp_dir, f"audio_scene_{sc['id']}.wav")
        engine.save_to_file(sc['narrative'], wav_path)
        engine.runAndWait()

        with contextlib.closing(wave.open(wav_path, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)

        audio_files.append(wav_path)
        durations.append(max(duration + 1.5, sc['target_duration']))

    concat_txt = os.path.join(temp_dir, "audio_concat.txt")
    with open(concat_txt, "w") as f:
        for a_file in audio_files:
            abs_a = os.path.abspath(a_file).replace('\\', '/')
            f.write(f"file '{abs_a}'\n")

    master_wav = os.path.join(temp_dir, "master_narration.wav")
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

    cmd_audio = [
        ffmpeg_exe, "-y", "-f", "concat", "-safe", "0",
        "-i", concat_txt, "-c", "copy", master_wav
    ]
    subprocess.run(cmd_audio, check=True)

    # PAGE-FULL FIT 1080p FRAME RENDERING (1920x1080) — ZERO BLANK SPACE!
    print("Rendering 1080p PAGE-FULL FIT slide images...")
    width, height = 1920, 1080
    scene_images = []

    for sc in scenes:
        # Subtle Off-White Canvas (#F8F9FA) with full edge-to-edge dark teal styling
        img = Image.new("RGB", (width, height), (248, 249, 250))
        draw = ImageDraw.Draw(img)

        # Header Bar (Top 0 to 140px)
        draw.rectangle([(0, 0), (width, 140)], fill=(44, 85, 85))

        # Footer Bar (Bottom 1010 to 1080px)
        draw.rectangle([(0, 1010), (width, 1080)], fill=(30, 60, 60))

        # Typography Fonts
        try:
            font_title = ImageFont.truetype("timesbd.ttf", 46)
            font_sub = ImageFont.truetype("timesi.ttf", 26)
            font_badge = ImageFont.truetype("timesbd.ttf", 24)
            font_text = ImageFont.truetype("times.ttf", 26)
            font_footer = ImageFont.truetype("times.ttf", 22)
        except:
            font_title = ImageFont.load_default()
            font_sub = font_title
            font_badge = font_title
            font_text = font_title
            font_footer = font_title

        # Header Text (White on Dark Teal)
        draw.text((40, 20), f"KEFFI AI — PROJECT JOURNEY DEMO | SCENE {sc['id']}/7", fill=(212, 163, 115), font=font_sub)
        draw.text((40, 60), sc['title'], fill=(255, 255, 255), font=font_title)

        # Footer Text (White & Gold on Dark Teal)
        draw.text((40, 1030), "TNSDC Naan Mudhalvan Niral Thiruvizha 3.0 | Project ID: NMNTSTD42260064", fill=(255, 255, 255), font=font_footer)
        draw.text((width-500, 1030), "Anna University Panruti | Team Hackers", fill=(212, 163, 115), font=font_footer)

        # PAGE FULL FIT: Split Screen (Left: 910x840px, Right: 910x840px) — ZERO EMPTY SPACE!
        photo_path = sc['photo']
        if photo_path and os.path.exists(photo_path):
            try:
                photo_img = Image.open(photo_path).convert("RGB")
                # Stretch & Fit Photo/Diagram to 910x840px
                photo_img = photo_img.resize((910, 840), Image.Resampling.LANCZOS)
                img.paste(photo_img, (40, 155))
                draw.rectangle([(35, 150), (955, 999)], outline=(44, 85, 85), width=4)
            except Exception as e:
                print("Photo load error:", e)

            # Right Full Container (910x840px)
            draw.rectangle([(970, 155), (1880, 995)], fill=(255, 255, 255), outline=(44, 85, 85), width=3)
            
            # Inner Header Box
            draw.rectangle([(970, 155), (1880, 240)], fill=(44, 85, 85))
            draw.text((990, 180), sc['subtitle'], fill=(255, 255, 255), font=font_sub)

            # Badge Box
            draw.rectangle([(990, 260), (1860, 325)], fill=(212, 163, 115))
            draw.text((1010, 280), sc['badge'], fill=(0, 0, 0), font=font_badge)

            # Rich Full-Height Bullet List (Filling right panel completely!)
            bullets = [
                "• Multimodal Affective Digital Therapeutics Platform",
                "• 68-Landmark Facial Reticle Computer Vision Scanner",
                "• ZEBRONICS Mic Acoustic Voice Prosody Processing",
                "• Fine-Tuned BERT 96-Emotion Model (94.8% F1 Accuracy)",
                "• SHAP & LIME Token Attribution Heatmaps for Doctors",
                "• 0-100 Mental Health Quotient & PHQ-9 Risk Triage",
                "• n8n Automated Crisis Escalation & WhatsApp Webhooks",
                "• Executive Admin Clinical Hub (#2C5555) & Doctor Booking",
                "• Live Cloud Production Deployment on Vercel & HuggingFace"
            ]
            y_off = 350
            for b in bullets:
                draw.text((1000, y_off), b, fill=(20, 20, 20), font=font_text)
                y_off += 68

        sc_png = os.path.join(temp_dir, f"full_fit_slide_{sc['id']}.png")
        img.save(sc_png)
        scene_images.append((sc_png, durations[sc['id']-1]))

    # FAST MUXING VIA FFMPEG
    print("Muxing page-full fit slides and soft human narration into 1080p MP4...")
    input_args = []
    filter_parts = []
    
    for idx, (img_p, dur) in enumerate(scene_images):
        input_args.extend(["-loop", "1", "-t", str(dur), "-i", img_p])
        filter_parts.append(f"[{idx}:v]")
    
    filter_str = "".join(filter_parts) + f"concat=n={len(scene_images)}:v=1:a=0[v]"

    cmd_fast_mux1 = [
        ffmpeg_exe, "-y"
    ] + input_args + [
        "-i", master_wav,
        "-filter_complex", filter_str,
        "-map", "[v]", "-map", f"{len(scene_images)}:a",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
        "-shortest", out_mp4_1
    ]
    subprocess.run(cmd_fast_mux1, check=True)

    cmd_fast_mux2 = [
        ffmpeg_exe, "-y"
    ] + input_args + [
        "-i", master_wav,
        "-filter_complex", filter_str,
        "-map", "[v]", "-map", f"{len(scene_images)}:a",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
        "-shortest", out_mp4_2
    ]
    subprocess.run(cmd_fast_mux2, check=True)

    print(f"[SUCCESS] Page-Full Fit 2:30 Minute MP4 Video Rendered & Saved at:\n  1. {out_mp4_1}\n  2. {out_mp4_2}")

if __name__ == "__main__":
    build_full_fit_video()
