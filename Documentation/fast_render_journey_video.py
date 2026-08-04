import os
import sys
import wave
import contextlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2
import imageio_ffmpeg
import pyttsx3

def build_fast_journey_video():
    print("=== STARTING FAST HIGH-PERFORMANCE VIDEO RENDER ===")

    work_dir = r"e:\Keffi Ai"
    temp_dir = os.path.join(work_dir, "fast_video_temp")
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
            "photo": None,
            "badge": "Clinical Need | 167 Unmonitored Hours Between Sessions",
            "target_duration": 22.0
        },
        {
            "id": 3,
            "title": "TEAM RESEARCH & SCIENTIFIC VALIDATION",
            "subtitle": "Peer-Reviewed CBT, ACT & Stanford Woebot Study Foundations",
            "narrative": "To solve this care gap, Team Hackers, Madhumathi, Balaji, and Malini, conducted an extensive literature survey, analyzing peer-reviewed studies by Hofmann, Norcross, and the landmark Stanford Woebot RCT trial to design an evidence-based digital therapeutics platform.",
            "photo": p2,
            "badge": "Team Hackers — Literature Survey & Brainstorming",
            "target_duration": 22.0
        },
        {
            "id": 4,
            "title": "MULTIMODAL SENSING & WEBCAM RETICLE",
            "subtitle": "FINGERS HD Webcam 68-Landmark Vision & ZEBRONICS Voice Prosody",
            "narrative": "Overcoming text-only deception, Keffi A I introduces a Multimodal Sensor Fusion Engine. Real-time computer vision via FINGERS HD Webcam tracks 68 facial landmarks to scan eyebrow contraction, lip mobility, and jaw tension, while ZEBRONICS mic Librosa audio processing measures pitch variance and speech pause duration.",
            "photo": p3,
            "badge": "Biometric Sensing | FINGERS Webcam Reticle + ZEBRONICS Mic",
            "target_duration": 23.0
        },
        {
            "id": 5,
            "title": "96-EMOTION BERT MODEL & SHAP EXPLAINABLE AI",
            "subtitle": "Fine-Tuned NLP, Smiling Depression & Token Attribution Heatmaps",
            "narrative": "Our fine-tuned BERT transformer model classifies patient text across a 96-state clinical emotion taxonomy with 94 point 8 percent accuracy, detecting hidden Smiling Depression. To eliminate black-box A I risks, SHAP and LIME token attribution heatmaps color-code word weights for clinician auditing.",
            "photo": p4,
            "badge": "Clinical AI Brain | 96-Emotion BERT & SHAP Clinician Auditing",
            "target_duration": 23.0
        },
        {
            "id": 6,
            "title": "PRODUCTION DEVELOPMENT & AUTOMATION",
            "subtitle": "Widescreen Live Video Call, n8n Webhooks & Admin Hub",
            "narrative": "Team Hackers integrated full multimodal video calling with a continuous hands-free voice loop, automated n8n crisis webhooks, and an Executive Admin Clinical Hub featuring 1-click doctor appointment booking, deploying the cloud backend live on Hugging Face Space.",
            "photo": p5,
            "badge": "Team Hackers — System Integration & Cloud Deployment",
            "target_duration": 22.0
        },
        {
            "id": 7,
            "title": "CONCLUSION & SOCIETAL IMPACT",
            "subtitle": "Democratizing 24/7 Affective Mental Healthcare in Tamil Nadu",
            "narrative": "Keffi A I democratizes 24/7 accessible affective mental healthcare across Tamil Nadu, closing the 167-hour outpatient care gap. We express our sincere gratitude to Anna University, TNSDC Naan Mudhalvan, and our Guide Doctor S Sivanesh. Thank you!",
            "photo": p6,
            "badge": "Live Production: keffi-test.vercel.app | Team Hackers",
            "target_duration": 18.0
        }
    ]

    # Generate Audio Tracks via pyttsx3
    print("Generating TTS voiceover audio tracks...")
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    if len(voices) > 1:
        engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 150)

    audio_files = []
    durations = []

    for sc in scenes:
        wav_path = os.path.join(temp_dir, f"audio_{sc['id']}.wav")
        engine.save_to_file(sc['narrative'], wav_path)
        engine.runAndWait()

        with contextlib.closing(wave.open(wav_path, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)

        audio_files.append(wav_path)
        durations.append(max(duration + 1.5, sc['target_duration']))

    total_video_duration = sum(durations)
    print(f"Total Video Duration: {total_video_duration:.2f}s ({total_video_duration/60:.2f} mins)")

    concat_txt = os.path.join(temp_dir, "audio_concat.txt")
    with open(concat_txt, "w") as f:
        for a_file in audio_files:
            abs_a = os.path.abspath(a_file).replace('\\', '/')
            f.write(f"file '{abs_a}'\n")

    master_wav = os.path.join(temp_dir, "master_narration.wav")
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

    import subprocess
    cmd_audio = [
        ffmpeg_exe, "-y", "-f", "concat", "-safe", "0",
        "-i", concat_txt, "-c", "copy", master_wav
    ]
    subprocess.run(cmd_audio, check=True)

    # FAST RENDERING OPTIMIZATION: Render 1 Slide Image per Scene & use FFmpeg image loop!
    print("Pre-rendering static 1080p scene images for ultra-fast video encoding...")
    width, height = 1920, 1080

    scene_images = []

    for sc in scenes:
        img = Image.new("RGB", (width, height), (27, 59, 59))
        draw = ImageDraw.Draw(img)

        draw.rectangle([(0, 0), (width, 140)], fill=(44, 85, 85))
        draw.rectangle([(0, height-80), (width, height)], fill=(20, 45, 45))

        try:
            font_title = ImageFont.truetype("times.ttf", 46)
            font_sub = ImageFont.truetype("times.ttf", 26)
            font_badge = ImageFont.truetype("arial.ttf", 24)
            font_text = ImageFont.truetype("arial.ttf", 26)
            font_footer = ImageFont.truetype("arial.ttf", 20)
        except:
            font_title = ImageFont.load_default()
            font_sub = font_title
            font_badge = font_title
            font_text = font_title
            font_footer = font_title

        draw.text((60, 25), f"KEFFI AI — PROJECT JOURNEY DEMO | SCENE {sc['id']}/7", fill=(143, 169, 137), font=font_sub)
        draw.text((60, 65), sc['title'], fill=(255, 255, 255), font=font_title)

        draw.text((60, height-55), "TNSDC Naan Mudhalvan Niral Thiruvizha 3.0 | Project ID: NMNTSTD42260064", fill=(143, 169, 137), font=font_footer)
        draw.text((width-450, height-55), "Anna University Panruti | Team Hackers", fill=(212, 163, 115), font=font_footer)

        photo_path = sc['photo']
        if photo_path and os.path.exists(photo_path):
            try:
                photo_img = Image.open(photo_path).convert("RGB")
                photo_img = photo_img.resize((840, 630), Image.Resampling.LANCZOS)
                img.paste(photo_img, (60, 180))
                draw.rectangle([(55, 175), (905, 815)], outline=(143, 169, 137), width=4)
            except Exception as e:
                print("Photo load error:", e)

            draw.rectangle([(940, 180), (1860, 810)], fill=(38, 75, 75), outline=(143, 169, 137), width=2)
            draw.text((970, 220), sc['subtitle'], fill=(212, 163, 115), font=font_sub)

            draw.rectangle([(970, 280), (1830, 340)], fill=(58, 112, 112))
            draw.text((990, 295), sc['badge'], fill=(255, 255, 255), font=font_badge)

            bullets = [
                "• Multimodal Affective AI Triage Platform",
                "• 68-Landmark Facial Reticle & Librosa Prosody",
                "• Fine-Tuned BERT 96-Emotion Model (94.8% F1)",
                "• SHAP & LIME Token Attribution Heatmaps",
                "• Live Cloud Deployment: HuggingFace & Vercel"
            ]
            y_off = 380
            for b in bullets:
                draw.text((970, y_off), b, fill=(240, 245, 240), font=font_text)
                y_off += 55

        else:
            draw.rectangle([(60, 180), (1860, 810)], fill=(38, 75, 75), outline=(143, 169, 137), width=3)
            draw.text((100, 220), sc['subtitle'], fill=(212, 163, 115), font=font_title)

            draw.rectangle([(100, 300), (1200, 365)], fill=(58, 112, 112))
            draw.text((120, 318), sc['badge'], fill=(255, 255, 255), font=font_badge)

            lines = [
                "1. 167-Hour Outpatient Care Gap: Outpatients receive 1 hr/week therapy, leaving 167 hrs unmonitored.",
                "2. Multimodal Sensor Fusion: Fuses FINGERS HD Webcam vision, ZEBRONICS mic voice prosody & BERT NLP.",
                "3. Triple-Tier Therapeutics: Empathetic Validation -> Biological Psychoeducation -> CBT Somatic Skills.",
                "4. Explainable AI (XAI): SHAP/LIME token attribution heatmaps for transparent clinician auditing.",
                "5. Crisis Automation: Automated n8n webhooks dispatch instant emergency WhatsApp/SMS alerts."
            ]
            y_off = 400
            for line in lines:
                draw.text((100, y_off), line, fill=(245, 250, 245), font=font_text)
                y_off += 65

        sc_png = os.path.join(temp_dir, f"scene_slide_{sc['id']}.png")
        img.save(sc_png)
        scene_images.append((sc_png, durations[sc['id']-1]))

    # Combine Scene Images and Audio using FFmpeg in under 10 seconds!
    print("Muxing scene slides and audio narration into final 1080p MP4...")
    
    # Create FFmpeg video filter concat string
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

    print(f"[SUCCESS] FAST 2:30 Minute Project Journey Demo Video Rendered & Saved at:\n  1. {out_mp4_1}\n  2. {out_mp4_2}")

if __name__ == "__main__":
    build_fast_journey_video()
