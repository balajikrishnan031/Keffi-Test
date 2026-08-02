import os
import sys
import shutil
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

def build_master_a3_white_poster():
    print("=== GENERATING MASTER A3 LANDSCAPE WHITE SHEET POSTER (NO BOXES) ===")
    
    target_pdf_main = r'e:\Keffi Ai\Presentations_and_Extracted_Media\KEFFI_POSTER.pdf'
    target_pdf_final = r'e:\Keffi Ai\Presentations_and_Extracted_Media\KEFFI_POSTER_FINAL.pdf'
    submission_pdf = r'e:\Keffi Ai\Final_Submission_Pack\3_Project_Poster.pdf'
    
    img_logo_left = r'e:\Keffi Ai\Documentation\extracted_poster_images\poster_img_1.png'   # TNSDC Logo
    img_logo_right = r'e:\Keffi Ai\Documentation\extracted_poster_images\poster_img_3.jpg'  # College Logo
    img_hero = r'e:\Keffi Ai\Documentation\extracted_report_images\shot_1_landing_hero.png'  # Live Hero UI
    img_arch = r'e:\Keffi Ai\Documentation\extracted_poster_images\poster_img_4.jpg'        # Architecture Diagram

    os.makedirs(os.path.dirname(target_pdf_final), exist_ok=True)
    os.makedirs(os.path.dirname(submission_pdf), exist_ok=True)

    # Standard A3 Landscape Page Dimensions: 1190.55 x 841.89 pt (16.54 x 11.69 inches)
    doc = SimpleDocTemplate(
        target_pdf_final,
        pagesize=landscape(A3),
        leftMargin=0.35 * inch,
        rightMargin=0.35 * inch,
        topMargin=0.35 * inch,
        bottomMargin=0.35 * inch
    )

    styles = getSampleStyleSheet()

    PRIMARY_GREEN = colors.HexColor('#0F3838')  # Deep forest green header
    TEAL_HEADING = colors.HexColor('#0D5050')   # Topic heading color
    TEXT_DARK = colors.HexColor('#1E293B')      # Slate 800 text
    DIVIDER_COLOR = colors.HexColor('#0D7070')  # Underline divider

    style_title = ParagraphStyle(
        'PosterTitle',
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        alignment=TA_CENTER,
        textColor=colors.white
    )

    style_topic_head = ParagraphStyle(
        'TopicHead',
        fontName='Helvetica-Bold',
        fontSize=12.0,
        leading=15.0,
        alignment=TA_LEFT,
        textColor=TEAL_HEADING,
        spaceAfter=3
    )

    style_body = ParagraphStyle(
        'PosterBody',
        fontName='Helvetica',
        fontSize=9.2,
        leading=12.5,
        alignment=TA_JUSTIFY,
        textColor=TEXT_DARK,
        spaceAfter=5
    )

    style_bullet = ParagraphStyle(
        'PosterBullet',
        fontName='Helvetica',
        fontSize=8.8,
        leading=12.0,
        alignment=TA_LEFT,
        textColor=TEXT_DARK,
        spaceAfter=3.5
    )

    story = []

    # 1. CORNER-TO-CORNER TOP HEADER BANNER (WITH BOTH CORNER LOGOS)
    header_html = """
    <font size="22"><b>KEFFI AI – A MENTAL HEALTH CHATBOT</b></font><br/>
    <font size="11.5"><b>UNIVERSITY COLLEGE OF ENGINEERING PANRUTI</b></font><br/>
    <font size="9.5"><i>(A Constituent College of Anna University, Chennai) • Department of Computer Science and Engineering</i></font><br/>
    <font size="9.0"><b>TEAM NAME:</b> HACKERS TEAM &nbsp;&nbsp;|&nbsp;&nbsp; 
    <b>MEMBERS:</b> MADHUMATHI S (422623104003), BALAJI P (422623104035), MALINI V (422623104048)<br/>
    <b>GUIDE NAME:</b> DR. S. SIVANESH M.Tech., Ph.D. (Assistant Professor & Head of Department)</font>
    """
    p_header = Paragraph(header_html, style_title)

    img_l = Image(img_logo_left, width=80, height=80) if os.path.exists(img_logo_left) else Paragraph("", style_body)
    img_r = Image(img_logo_right, width=80, height=80) if os.path.exists(img_logo_right) else Paragraph("", style_body)

    header_table = Table([[img_l, p_header, img_r]], colWidths=[90, 960, 90])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), PRIMARY_GREEN),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 14))

    # Helper function to generate clean NO-BOX topic sections
    def make_no_box_topic(heading_text, content_elements, width_pt):
        topic_story = []
        p_h = Paragraph(f"<b>{heading_text.upper()}</b>", style_topic_head)
        topic_story.append(p_h)
        topic_story.append(HRFlowable(width="100%", thickness=1.5, color=DIVIDER_COLOR, spaceBefore=2, spaceAfter=6))
        for item in content_elements:
            topic_story.append(item)
        
        t = Table([[topic_story]], colWidths=[width_pt])
        t_style = [
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ]
        t.setStyle(TableStyle(t_style))
        return t

    # COLUMN 1 (LEFT COLUMN - WIDTH: 370pt)
    c1_1 = Paragraph("Mental healthcare accessibility remains a critical global challenge due to high therapy costs, psychiatrist shortages, and social stigma. Standard psychotherapy is restricted to 1 hour per week, leaving patients completely unmonitored during the remaining 167 hours of weekly vulnerability. Keffi AI is a clinical digital therapeutics platform developed to bridge this gap, providing 24/7 continuous affective monitoring, hands-free voice interaction, and structured psychological interventions.", style_body)
    sec_abstract = make_no_box_topic("1. ABSTRACT", [c1_1], 370)

    c1_2 = [
        Paragraph("• <b>Fine-Tuned BERT 96-Emotion Classifier:</b> Classifies complex contextual user statements into 96 distinct emotional categories with 94.2% top-3 accuracy.", style_bullet),
        Paragraph("• <b>3-Tier Clinical Therapeutic Response:</b> Constructs responses combining Rogerian empathy, neurobiological psychoeducation, and CBT grounding skills.", style_bullet),
        Paragraph("• <b>Hands-Free Voice-to-Voice AI:</b> Integrated real-time Web Speech API audio processing for patients in acute panic unable to type.", style_bullet),
        Paragraph("• <b>Write-Ahead Logging (WAL) DB Engine:</b> High-concurrency database architecture eliminating locking crashes during peak concurrent usage.", style_bullet),
        Paragraph("• <b>Explainable AI (SHAP / LIME):</b> Visual token-level feature attribution maps empowering psychiatrists to audit automated decisions.", style_bullet),
        Paragraph("• <b>Admin Clinical Hub & Roster:</b> Real-time patient tracking displaying Days Inactive metrics and complete scrollable conversation transcripts.", style_bullet),
    ]
    sec_highlights = make_no_box_topic("2. HIGHLIGHTS OF THE PROJECT", c1_2, 370)

    c1_3 = Paragraph("Keffi AI employs a multi-modal affective computing pipeline. User inputs (text or voice audio) pass through a dual-model processing cascade. The BERT transformer classifies fine-grained emotion vectors, while an audio prosody analyzer extracts acoustic biomarkers (F0 pitch, RMS energy, speech rate). Context is maintained by retrieving chronological session memory from a WAL-enabled relational database and vector embedding store. If crisis signals occur, automated n8n workflows alert emergency contacts and clinical supervisors immediately.", style_body)
    sec_methodology = make_no_box_topic("3. METHODOLOGY", [c1_3], 370)

    col1_topics = [sec_abstract, Spacer(1, 10), sec_highlights, Spacer(1, 10), sec_methodology]

    # COLUMN 2 (CENTER COLUMN - WIDTH: 385pt)
    c2_1 = [
        Paragraph("<b>Step 1: Multimodal Data Ingestion:</b> Capture user text utterance or real-time voice audio via Web Speech API endpoints.", style_bullet),
        Paragraph("<b>Step 2: BERT Emotion Classification:</b> Tokenize text input and classify across 96 fine-grained emotional state vectors.", style_bullet),
        Paragraph("<b>Step 3: Isolated Context Retrieval:</b> Query WAL database and vector memory using patient ID to restore past chat timeline.", style_bullet),
        Paragraph("<b>Step 4: 3-Tier Therapeutic Response Synthesis:</b> Synthesize Rogerian validation, neurobiological explanations (cortisol/amygdala), and CBT grounding exercises.", style_bullet),
        Paragraph("<b>Step 5: Acoustic Prosody & Risk Triage:</b> Compute pitch variance deltas; trigger automated n8n crisis alerts if suicidal ideation is flagged.", style_bullet),
        Paragraph("<b>Step 6: Clinician Dashboard Synchronization:</b> Update Mental Health Quotient (MHQ) score telemetry and log complete transcripts in Admin Hub.", style_bullet),
    ]
    sec_procedure = make_no_box_topic("4. STEP BY STEP PROCEDURE OR ALGORITHM", c2_1, 385)

    c2_2 = [
        Paragraph("• <b>GoEmotions Multi-Label Dataset:</b> 58,000 carefully curated Reddit comments annotated across 27 fine-grained emotion categories, extended to 96 clinical psychological states for transformer fine-tuning.", style_bullet),
        Paragraph("• <b>DAIC-WOZ Depression Audio Corpus:</b> Clinical interviews containing acoustic voice prosody benchmarks used to calibrate Fundamental Frequency (F0) and speech pause indicators.", style_bullet),
    ]
    sec_dataset = make_no_box_topic("5. DATASET USED IF ANY", c2_2, 385)

    c2_3 = Paragraph("Keffi AI successfully validates the integration of fine-grained emotion classification, high-concurrency database storage, hands-free voice therapeutics, and clinician tracking into a unified digital mental health platform. By closing the 167-hour weekly care gap, Keffi AI empowers self-guided patient recovery while providing psychiatrists with real-time risk visibility.", style_body)
    sec_conclusion = make_no_box_topic("7. CONCLUSION", [c2_3], 385)

    col2_topics = [sec_procedure, Spacer(1, 10), sec_dataset, Spacer(1, 10), sec_conclusion]

    # COLUMN 3 (RIGHT COLUMN - WIDTH: 370pt)
    c3_1 = [
        Paragraph("<b>User Input:</b><br/>Spoken voice audio or written text statement:<br/><i>\"I feel completely overwhelmed by exam deadlines, my heart is racing, and I can't sleep.\"</i>", style_bullet),
        Paragraph("<b>System Output:</b><br/>• <b>Tier 1 Validation:</b> <i>\"I hear how much pressure you're under. It's valid to feel overwhelmed.\"</i><br/>• <b>Tier 2 Psychoeducation:</b> <i>\"Your brain's amygdala is triggering a surge in cortisol.\"</i><br/>• <b>Tier 3 CBT Skill:</b> <i>\"Try 4-7-8 breathing: Breathe in for 4s, hold for 7s, exhale for 8s.\"</i><br/>• <b>Voice Readout & Chips:</b> Spoken therapeutic readout and interactive grounding chips.", style_bullet),
    ]
    sec_io = make_no_box_topic("6. INPUT AND OUTPUT", c3_1, 370)

    # Embedding Live Landing Page UI & System Architecture Image
    img_ui_element = Image(img_hero, width=360, height=200) if os.path.exists(img_hero) else Paragraph("", style_body)
    img_arch_element = Image(img_arch, width=360, height=140) if os.path.exists(img_arch) else Paragraph("", style_body)
    
    sec_system_img = make_no_box_topic("LIVE PLATFORM UI & SYSTEM ARCHITECTURE", [img_ui_element, Spacer(1, 4), img_arch_element], 370)

    col3_topics = [sec_io, Spacer(1, 8), sec_system_img]

    # ASSEMBLE 3 COLUMNS SIDE BY SIDE ON A3 SHEET
    main_grid = Table([[col1_topics, col2_topics, col3_topics]], colWidths=[375, 390, 375])
    main_grid.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))

    story.append(main_grid)

    doc.build(story)
    print(f"[SUCCESS] Master A3 Landscape White Sheet Poster Generated at: {target_pdf_final}")

    # Copy to both main target PDF & submission pack
    try:
        shutil.copyfile(target_pdf_final, target_pdf_main)
        print(f"[SUCCESS] Synced Poster PDF to KEFFI_POSTER.pdf: {target_pdf_main}")
    except Exception as e:
        print(f"[NOTE] KEFFI_POSTER.pdf sync note: {e}")

    shutil.copyfile(target_pdf_final, submission_pdf)
    print(f"[SUCCESS] Synced Poster PDF to Submission Pack: {submission_pdf}")

if __name__ == "__main__":
    build_master_a3_white_poster()
