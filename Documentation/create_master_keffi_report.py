import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def add_heading_styled(doc, text, level):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.space_before = Pt(14)
    h.paragraph_format.space_after = Pt(6)
    run = h.runs[0]
    run.font.name = 'Times New Roman'
    run.font.bold = True
    if level == 1:
        run.font.size = Pt(18)
        run.font.color.rgb = RGBColor(13, 26, 26) # Dark Teal
        h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif level == 2:
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(44, 85, 85)
    else:
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(58, 112, 112)
    return h

def add_para_styled(doc, text, bold_prefix=None, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Times New Roman'
        r_pre.font.size = Pt(12)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(13, 26, 26)
    r_body = p.add_run(text)
    r_body.font.name = 'Times New Roman'
    r_body.font.size = Pt(12)
    r_body.font.color.rgb = RGBColor(35, 35, 35)
    return p

def create_master_report():
    print("=== CREATING KEFFI AI MASTER PROJECT REPORT DOCX ===")
    doc = Document()

    # Page Margins: 1 inch all around
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # ----------------------------------------------------
    # COVER PAGE
    # ----------------------------------------------------
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(36)
    p_title.paragraph_format.space_after = Pt(18)
    r = p_title.add_run("ARTIFICIAL INTELLIGENCE IN MENTAL HEALTHCARE\nKEFFI CLINICAL DIGITAL THERAPEUTICS PLATFORM")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(22)
    r.font.bold = True
    r.font.color.rgb = RGBColor(13, 26, 26)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(24)
    r = p_sub.add_run("A PROJECT REPORT\nSubmitted by")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.font.bold = True

    # Team Members Table
    table_team = doc.add_table(rows=3, cols=2)
    table_team.alignment = WD_TABLE_ALIGNMENT.CENTER
    team_data = [
        ("MADHUMATHI S", "6381344502 / 422623104003 (Team Lead)"),
        ("BALAJI P", "9342636595 / 4226231035"),
        ("MALINI V", "8807984385 / 4226231048")
    ]
    for idx, (name, reg) in enumerate(team_data):
        row = table_team.rows[idx]
        cell0 = row.cells[0]
        cell1 = row.cells[1]
        cell0.text = name
        cell1.text = reg
        cell0.paragraphs[0].runs[0].font.name = 'Times New Roman'
        cell0.paragraphs[0].runs[0].font.size = Pt(12)
        cell0.paragraphs[0].runs[0].font.bold = True
        cell1.paragraphs[0].runs[0].font.name = 'Times New Roman'
        cell1.paragraphs[0].runs[0].font.size = Pt(12)

    p_deg = doc.add_paragraph()
    p_deg.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_deg.paragraph_format.space_before = Pt(36)
    p_deg.paragraph_format.space_after = Pt(36)
    r = p_deg.add_run("BACHELOR OF ENGINEERING\nin\nCOMPUTER SCIENCE AND ENGINEERING\n\nUNIVERSITY COLLEGE OF ENGINEERING PANRUTI\nPANRUTI - 607106\n\nANNA UNIVERSITY, CHENNAI - 600025\n\nMAY 2026")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.font.bold = True

    doc.add_page_break()

    # ----------------------------------------------------
    # BONAFIDE CERTIFICATE
    # ----------------------------------------------------
    add_heading_styled(doc, "ANNA UNIVERSITY: CHENNAI 600025\nBONAFIDE CERTIFICATE", level=1)
    add_para_styled(doc, "Certified that this project report \"KEFFI AI – A CLINICAL DIGITAL THERAPEUTICS PLATFORM FOR MENTAL HEALTHCARE\" is the Bonafide work of MADHUMATHI S (6381344502 / 422623104003), BALAJI P (9342636595 / 4226231035), and MALINI V (8807984385 / 4226231048) who carried out the project under my supervision.", space_after=36)

    add_para_styled(doc, "SIGNATURE\n\n\nDR. S. SIVANESH M.Tech., Ph.D.\nPROJECT GUIDE & HEAD OF DEPARTMENT\nDEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING\nUNIVERSITY COLLEGE OF ENGINEERING PANRUTI", space_after=48)
    add_para_styled(doc, "EXAMINED ON: 05/08/2026 Afternoon Session (AN) | Panel 2 | Chennai Region Venue\n\n\nINTERNAL EXAMINER                                           EXTERNAL EXAMINER", space_after=24)

    doc.add_page_break()

    # ----------------------------------------------------
    # EXECUTIVE ABSTRACT
    # ----------------------------------------------------
    add_heading_styled(doc, "ABSTRACT", level=1)
    add_para_styled(doc, "Keffi AI is a state-of-the-art Clinical Digital Therapeutics Platform engineered to bridge the 167-hour weekly gap in traditional mental healthcare. Existing chatbots lack persistent memory, real-time clinical safety controls, and multi-modal affective intelligence. Keffi AI resolves these critical barriers through a multi-layered Affective Computing Architecture that combines 96-state fine-grained BERT emotion classification, real-time Voice Prosody Pitch Analysis, and Webcam Visual Affect Scanning.")
    add_para_styled(doc, "The platform incorporates a high-concurrency SQLite Write-Ahead Logging (WAL Mode) Database (`keffi_clinical.db`) paired with vector-based long-term memory to store isolated patient profiles and complete conversation histories. Each user is registered via phone number and preferred name, ensuring their chat timeline is automatically restored seamlessly across sessions.")
    add_para_styled(doc, "For clinical oversight, Keffi AI provides an Admin Clinical Hub Dashboard enabling doctors to monitor A-to-Z patient details, live Mental Health Quotient (MHQ) scores, attrition probabilities, Days Inactive metrics, and complete scrollable conversation transcripts. To ensure accessibility, Keffi AI supports hands-free real-time Voice-to-Voice AI interaction via Web Speech API (STT/TTS), allowing patients to speak naturally while Keffi AI responds back in a soothing, empathetic voice.")

    doc.add_page_break()

    # ----------------------------------------------------
    # CHAPTER 1: INTRODUCTION
    # ----------------------------------------------------
    add_heading_styled(doc, "CHAPTER 1: INTRODUCTION", level=1)
    add_heading_styled(doc, "1.1 Overview of Mental Healthcare", level=2)
    add_para_styled(doc, "Mental health is an integral dimension of human well-being affecting cognition, emotional regulation, and daily functioning. Modern society faces an escalating crisis of depression, generalized anxiety disorder (GAD), burnout, and loneliness driven by academic, economic, and social stressors. Millions suffer silently due to social stigma, financial constraints, and severe shortages of licensed mental health professionals.")

    add_heading_styled(doc, "1.2 The 167-Hour Gap & Need for AI Therapeutics", level=2)
    add_para_styled(doc, "Traditional psychotherapy typically occurs during a single 1-hour session per week. However, psychological crises, panic attacks, and intrusive negative thoughts do not conform to appointment schedules. The remaining 167 hours of the week represent an 'invisible gap' where patients navigate emotional distress unmonitored. Nearly 60% of individuals drop out of therapy prematurely due to cost and lack of immediate continuous support. Keffi AI was specifically designed to fill this void by offering 24/7 emotionally intelligent, clinically grounded digital therapeutic care.")

    add_heading_styled(doc, "1.3 Proposed System Objectives", level=2)
    add_para_styled(doc, "The primary objectives of the Keffi AI platform include:", bold_prefix=None)
    add_para_styled(doc, "1. Multi-Modal Affective Intelligence: Classifying text into 96 fine-grained emotional states using BERT, supplemented by voice prosody and visual emotion streams.", space_after=3)
    add_para_styled(doc, "2. High-Concurrency Persistent Database Engine: SQLite WAL mode database (`keffi_clinical.db`) storing user profiles, MHQ scores, and isolated chat timelines.", space_after=3)
    add_para_styled(doc, "3. Hands-Free Voice-to-Voice AI: Instant Web Speech STT and TTS speech synthesis enabling conversational voice interaction.", space_after=3)
    add_para_styled(doc, "4. Comprehensive Clinical Hub Dashboard: Allowing psychiatrists to inspect A-to-Z patient details, Days Inactive metrics, and full conversation transcripts.", space_after=6)

    # ----------------------------------------------------
    # CHAPTER 2: LITERATURE SURVEY
    # ----------------------------------------------------
    add_heading_styled(doc, "CHAPTER 2: LITERATURE SURVEY", level=1)
    add_heading_styled(doc, "2.1 Deep Learning Emotion Detection (GoEmotions & BERT)", level=2)
    add_para_styled(doc, "Research by A. Kumar and R. Singh (2021) demonstrated that transformer-based architectures like BERT process conversational context bidirectionally, significantly outperforming binary sentiment classifiers. Fine-tuning BERT on the 27-category GoEmotions dataset enables multi-label classification of nuanced emotional states such as grief, remorse, relief, and nervousness.")

    add_heading_styled(doc, "2.2 Multi-LLM Cascades & Explainable AI (XAI)", level=2)
    add_para_styled(doc, "Lundberg & Lee (2017) introduced SHAP (SHapley Additive exPlanations) for interpretable machine learning. In clinical AI applications, black-box LLMs present safety risks. Keffi AI incorporates a dual-engine 70B Multi-LLM cascade (Groq Llama-3.3-70B + ChatGPT 4o-mini fallback) combined with SHAP/LIME feature attribution to explain why specific clinical interventions are selected.")

    # ----------------------------------------------------
    # CHAPTER 3: SYSTEM SPECIFICATION & ARCHITECTURE
    # ----------------------------------------------------
    add_heading_styled(doc, "CHAPTER 3: SYSTEM SPECIFICATION & STACK", level=1)
    add_heading_styled(doc, "3.1 Software Technology Stack", level=2)
    add_para_styled(doc, "• Frontend Framework: React.js (Vite), Tailwind CSS, Lucide Icons, Web Speech API (STT & Speech Synthesis TTS).")
    add_para_styled(doc, "• Backend API Framework: FastAPI (Python 3.12), Uvicorn ASGI Server, Pydantic Schema Validation.")
    add_para_styled(doc, "• Database & Persistence Engine: SQLite 3 with Write-Ahead Logging (`PRAGMA journal_mode=WAL`), SQLAlchemy ORM, Engine Connection Pooling.")
    add_para_styled(doc, "• AI & NLP Layer: PyTorch, HuggingFace Transformers (GoEmotions BERT), Librosa Voice Prosody Analyzer, Groq Llama-3.3-70B API, OpenAI ChatGPT-4o-mini API.")

    # ----------------------------------------------------
    # CHAPTER 4: SYSTEM DESIGN & DATABASE SCHEMAS
    # ----------------------------------------------------
    add_heading_styled(doc, "CHAPTER 4: SYSTEM DESIGN & SCHEMAS", level=1)
    add_heading_styled(doc, "4.1 Relational Database Model (`keffi_clinical.db`)", level=2)
    add_para_styled(doc, "The backend database uses a WAL-enabled SQLite database with 5 primary tables:", bold_prefix=None)
    add_para_styled(doc, "1. Patient Table: Stores `patient_id` (Primary Key, e.g. P-43210), `name`, `phone`, `email`, `dob`, `gender`, `place`, `mhq_score`, `depression_level`, `assigned_doctor`, `created_at`, `last_active_at`.")
    add_para_styled(doc, "2. ChatMessage Table: Stores `id`, `patient_id` (Foreign Key), `message`, `ai_reply`, `bert_emotion`, `clinical_state`, `clinical_category`, `timestamp`.")
    add_para_styled(doc, "3. CognitiveDistortionLog Table: Stores detected cognitive distortion types, unhelpful thoughts, and reframed thoughts.")
    add_para_styled(doc, "4. BiometricTelemetryLog Table: Stores wearable sensor heart rate (BPM), HRV (ms), and panic flags.")

    # ----------------------------------------------------
    # CHAPTER 5: IMPLEMENTATION & API ENDPOINTS
    # ----------------------------------------------------
    add_heading_styled(doc, "CHAPTER 5: IMPLEMENTATION & API ENDPOINTS", level=1)
    add_heading_styled(doc, "5.1 Production API Routes (`main.py`)", level=2)
    add_para_styled(doc, "• POST /api/register: Upserts patient profile (Name, Phone, Email, DOB, Gender, Place) into database upon login.")
    add_para_styled(doc, "• GET /api/history/{patient_id}: Fetches isolated past chat history for the logged-in user to restore their conversation timeline.")
    add_para_styled(doc, "• GET /api/admin/patients_full: Computes A-to-Z patient roster metrics, total chat counts, and Days Inactive values for the doctor dashboard.")
    add_para_styled(doc, "• GET /api/admin/patient_detail/{patient_id}: Fetches full patient profile, biometric logs, CBT distortion logs, and complete scrollable conversation transcript.")
    add_para_styled(doc, "• POST /api/chat: Core therapeutic dialogue endpoint utilizing the 70B Multi-LLM cascade engine.")

    # ----------------------------------------------------
    # CHAPTER 6: CLINICAL HUB & HANDS-FREE VOICE AI
    # ----------------------------------------------------
    add_heading_styled(doc, "CHAPTER 6: CLINICAL HUB & VOICE THERAPEUTICS", level=1)
    add_heading_styled(doc, "6.1 Hands-Free Real-Time Voice-to-Voice AI", level=2)
    add_para_styled(doc, "When the user activates microphone mode in the Patient Sanctuary, Web Speech API converts spoken audio directly to text and submits it to `/api/chat`. Upon receiving Keffi AI's reply, Web Speech Synthesis (`window.speechSynthesis`) automatically speaks out Keffi's therapeutic response in a calm, female-pitch voice (`pitch = 1.05`, `rate = 0.95`), delivering a natural voice-to-voice therapy session.")

    add_heading_styled(doc, "6.2 Admin Clinical Hub Dashboard", level=2)
    add_para_styled(doc, "The Admin Clinical Hub enables psychiatrists to track roster metrics, view high-risk critical alerts, inspect Days Inactive counters, reassign therapists, and open the Complete Conversation Transcript viewer to audit every message exchanged between patient and Keffi AI.")

    # ----------------------------------------------------
    # CHAPTER 7: CONCLUSION & FUTURE ENHANCEMENTS
    # ----------------------------------------------------
    add_heading_styled(doc, "CHAPTER 7: CONCLUSION & FUTURE ENHANCEMENTS", level=1)
    add_para_styled(doc, "Keffi AI successfully demonstrates how multi-modal AI, WAL-enabled relational databases, and voice-to-voice interaction can create a clinically safe, continuous digital therapeutic companion. Future work includes hospital EHR integration (HL7/FHIR), multilingual regional voice models (Tamil, Hindi), and wearable BIOSENSOR hardware integration.")

    # Save document
    docx_path = r"e:\Keffi Ai\Documentation\KEFFI_MASTER_FINAL_PROJECT_REPORT.docx"
    doc.save(docx_path)
    print(f"[SUCCESS] Master DOCX Saved at: {docx_path}")
    return docx_path

if __name__ == "__main__":
    create_master_report()
