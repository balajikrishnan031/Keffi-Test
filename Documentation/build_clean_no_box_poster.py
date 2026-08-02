import os
import sys
import shutil
from reportlab.lib.pagesizes import landscape
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

def build_clean_no_box_poster():
    print("=== BUILDING CLEAN NO-BOX POSTER WITH LOGOS & UPPERCASE HEADINGS ===")
    
    target_pdf = r'e:\Keffi Ai\Presentations_and_Extracted_Media\KEFFI_POSTER_FINAL.pdf'
    target_pdf_main = r'e:\Keffi Ai\Presentations_and_Extracted_Media\KEFFI_POSTER.pdf'
    submission_pdf = r'e:\Keffi Ai\Final_Submission_Pack\3_Project_Poster.pdf'
    
    img_logo_left = r'e:\Keffi Ai\Documentation\extracted_poster_images\poster_img_1.png'   # TNSDC Logo
    img_logo_right = r'e:\Keffi Ai\Documentation\extracted_poster_images\poster_img_3.jpg'  # College Logo
    img_arch = r'e:\Keffi Ai\Documentation\extracted_poster_images\poster_img_4.jpg'        # Architecture / System Image

    os.makedirs(os.path.dirname(target_pdf), exist_ok=True)

    # Poster Dimensions: 960 x 540 pt (16:9 Landscape Ratio)
    POSTER_WIDTH = 960
    POSTER_HEIGHT = 540

    doc = SimpleDocTemplate(
        target_pdf,
        pagesize=(POSTER_WIDTH, POSTER_HEIGHT),
        leftMargin=14,
        rightMargin=14,
        topMargin=10,
        bottomMargin=10
    )

    styles = getSampleStyleSheet()

    DARK_GREEN = colors.HexColor('#0F3838')     # Dark forest green header banner
    PRIMARY_TEAL = colors.HexColor('#0D5050')   # Section heading color
    TEXT_DARK = colors.HexColor('#1E293B')      # Main text slate 800
    DIVIDER_COLOR = colors.HexColor('#0D7070')  # Section line divider

    style_title = ParagraphStyle(
        'PosterTitle',
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=21,
        alignment=TA_CENTER,
        textColor=colors.white
    )

    style_head = ParagraphStyle(
        'CleanSectionHead',
        fontName='Helvetica-Bold',
        fontSize=10.0,
        leading=12.0,
        alignment=TA_LEFT,
        textColor=PRIMARY_TEAL,
        spaceAfter=2
    )

    style_body = ParagraphStyle(
        'CleanBody',
        fontName='Helvetica',
        fontSize=7.4,
        leading=9.5,
        alignment=TA_JUSTIFY,
        textColor=TEXT_DARK,
        spaceAfter=4
    )

    style_bullet = ParagraphStyle(
        'CleanBullet',
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.2,
        alignment=TA_LEFT,
        textColor=TEXT_DARK,
        spaceAfter=2.5
    )

    story = []

    # 1. TOP HEADER BANNER (WITH BOTH LOGOS)
    header_html = """
    <font size="18"><b>KEFFI AI – A MENTAL HEALTH CHATBOT</b></font><br/>
    <font size="9.5"><b>UNIVERSITY COLLEGE OF ENGINEERING PANRUTI</b></font><br/>
    <font size="8"><i>(A Constituent College of Anna University, Chennai) • Department of Computer Science and Engineering</i></font><br/>
    <font size="7.5"><b>TEAM:</b> HACKERS TEAM &nbsp;|&nbsp; 
    <b>MEMBERS:</b> MADHUMATHI S (422623104003), BALAJI P (422623104035), MALINI V (422623104048) &nbsp;|&nbsp; 
    <b>GUIDE:</b> DR. S. SIVANESH M.Tech., Ph.D.</font>
    """
    p_header = Paragraph(header_html, style_title)

    img_l = Image(img_logo_left, width=65, height=65) if os.path.exists(img_logo_left) else Paragraph("", style_body)
    img_r = Image(img_logo_right, width=65, height=65) if os.path.exists(img_logo_right) else Paragraph("", style_body)

    header_table = Table([[img_l, p_header, img_r]], colWidths=[75, 782, 75])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), DARK_GREEN),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 8))

    # Helper function to generate clean NO-BOX sections
    def make_no_box_section(heading_text, content_elements, width_pt):
        sec_story = []
        p_h = Paragraph(f"<b>{heading_text.upper()}</b>", style_head)
        sec_story.append(p_h)
        sec_story.append(HRFlowable(width="100%", thickness=1.2, color=DIVIDER_COLOR, spaceBefore=1, spaceAfter=4))
        for item in content_elements:
            sec_story.append(item)
        
        t = Table([[sec_story]], colWidths=[width_pt])
        t_style = [
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 2),
            ('RIGHTPADDING', (0,0), (-1,-1), 2),
            ('TOPPADDING', (0,0), (-1,-1), 2),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]
        t.setStyle(TableStyle(t_style))
        return t

    # COLUMN 1 (LEFT COLUMN - WIDTH: 304pt)
    c1_1 = Paragraph("Mental healthcare accessibility remains a major global challenge due to high therapy costs, psychiatrist shortages, and social stigma. Psychotherapy is restricted to 1 hour per week, leaving patients unmonitored during the remaining 167 hours of weekly vulnerability. Keffi AI is a clinical digital therapeutics platform developed to bridge this gap, providing 24/7 continuous affective monitoring, hands-free voice interaction, and structured psychological interventions.", style_body)
    sec_abstract = make_no_box_section("1. ABSTRACT", [c1_1], 304)

    c1_2 = [
        Paragraph("• <b>BERT 96-Emotion Classifier:</b> Classifies complex user statements into 96 distinct emotional categories with 94.2% accuracy.", style_bullet),
        Paragraph("• <b>3-Tier Clinical Response:</b> Combines Rogerian empathy, neurobiological psychoeducation, and CBT grounding skills.", style_bullet),
        Paragraph("• <b>Hands-Free Voice AI:</b> Real-time Web Speech API audio processing for patients in acute panic unable to type.", style_bullet),
        Paragraph("• <b>Write-Ahead Logging (WAL) DB:</b> High-concurrency database eliminating locking crashes during peak usage.", style_bullet),
        Paragraph("• <b>SHAP / LIME Explainable AI:</b> Visual feature attribution maps empowering psychiatrists to audit decisions.", style_bullet),
        Paragraph("• <b>Admin Clinical Hub:</b> Displays Days Inactive metrics and complete scrollable conversation transcripts.", style_bullet),
    ]
    sec_highlights = make_no_box_section("2. HIGHLIGHTS OF THE PROJECT", c1_2, 304)

    c1_3 = Paragraph("Keffi AI employs a multi-modal affective computing pipeline. User inputs (text or voice) pass through a dual-model cascade: BERT classifies fine-grained emotion vectors while a Librosa audio prosody analyzer extracts acoustic biomarkers (F0 pitch, RMS energy). Context is maintained via WAL relational DB and vector memory. If crisis signals occur, automated n8n workflows alert emergency contacts immediately.", style_body)
    sec_methodology = make_no_box_section("3. METHODOLOGY", [c1_3], 304)

    col1_sections = [sec_abstract, Spacer(1, 4), sec_highlights, Spacer(1, 4), sec_methodology]

    # COLUMN 2 (CENTER COLUMN - WIDTH: 318pt)
    c2_1 = [
        Paragraph("<b>Step 1: Multimodal Ingestion:</b> Capture user text or voice audio via Web Speech API endpoints.", style_bullet),
        Paragraph("<b>Step 2: BERT Emotion Classification:</b> Classify input across 96 fine-grained emotional state vectors.", style_bullet),
        Paragraph("<b>Step 3: Isolated Context Retrieval:</b> Query WAL database and vector memory using patient ID.", style_bullet),
        Paragraph("<b>Step 4: 3-Tier Therapeutic Generation:</b> Synthesize Rogerian care, neurobiology, and CBT skills.", style_bullet),
        Paragraph("<b>Step 5: Acoustic Prosody & Risk Triage:</b> Compute pitch deltas; trigger n8n crisis alerts if suicidal ideation is flagged.", style_bullet),
        Paragraph("<b>Step 6: Clinician Hub Sync:</b> Update Mental Health Quotient (MHQ) telemetry and log transcripts in Admin Hub.", style_bullet),
    ]
    sec_procedure = make_no_box_section("4. STEP BY STEP PROCEDURE OR ALGORITHM", c2_1, 318)

    c2_2 = [
        Paragraph("• <b>GoEmotions Multi-Label Dataset:</b> 58,000 curated Reddit comments annotated across 27 emotion categories, extended to 96 clinical psychological states for fine-tuning.", style_bullet),
        Paragraph("• <b>DAIC-WOZ Depression Audio Corpus:</b> Clinical interviews containing acoustic voice prosody benchmarks used to calibrate pitch (F0) and speech pause indicators.", style_bullet),
    ]
    sec_dataset = make_no_box_section("5. DATASET USED IF ANY", c2_2, 318)

    c2_3 = Paragraph("Keffi AI validates the integration of fine-grained emotion classification, high-concurrency database storage, hands-free voice therapeutics, and clinician tracking into a unified digital platform, closing the 167-hour weekly care gap.", style_body)
    sec_conclusion = make_no_box_section("7. CONCLUSION", [c2_3], 318)

    col2_sections = [sec_procedure, Spacer(1, 4), sec_dataset, Spacer(1, 4), sec_conclusion]

    # COLUMN 3 (RIGHT COLUMN - WIDTH: 304pt)
    c3_1 = [
        Paragraph("<b>User Input:</b><br/>Spoken audio or text statement:<br/><i>\"I feel completely overwhelmed by exam deadlines, my heart is racing, and I can't sleep.\"</i>", style_bullet),
        Paragraph("<b>System Output:</b><br/>• <b>Tier 1 Validation:</b> <i>\"I hear how much pressure you're under. It's valid to feel overwhelmed.\"</i><br/>• <b>Tier 2 Psychoeducation:</b> <i>\"Your brain's amygdala is triggering a surge in cortisol.\"</i><br/>• <b>Tier 3 CBT Skill:</b> <i>\"Try 4-7-8 breathing: Breathe in for 4s, hold for 7s, exhale for 8s.\"</i><br/>• <b>Voice Readout & Chips:</b> Spoken therapeutic readout and interactive grounding chips.", style_bullet),
    ]
    sec_io = make_no_box_section("6. INPUT AND OUTPUT", c3_1, 304)

    c3_img_element = Image(img_arch, width=290, height=135) if os.path.exists(img_arch) else Paragraph("", style_body)
    sec_system_img = make_no_box_section("DEVELOPED SYSTEM ARCHITECTURE", [c3_img_element], 304)

    col3_sections = [sec_io, Spacer(1, 4), sec_system_img]

    # ASSEMBLE 3 COLUMNS SIDE BY SIDE
    main_grid = Table([[col1_sections, col2_sections, col3_sections]], colWidths=[310, 324, 310])
    main_grid.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))

    story.append(main_grid)

    doc.build(story)
    print(f"[SUCCESS] Clean No-Box Poster Generated at: {target_pdf}")

    # Copy to both main target PDF & submission pack
    try:
        shutil.copyfile(target_pdf, target_pdf_main)
        print(f"[SUCCESS] Synced Poster PDF to KEFFI_POSTER.pdf: {target_pdf_main}")
    except Exception as e:
        print(f"[NOTE] KEFFI_POSTER.pdf sync note: {e}")

    shutil.copyfile(target_pdf, submission_pdf)
    print(f"[SUCCESS] Synced Poster PDF to Submission Pack: {submission_pdf}")

if __name__ == "__main__":
    build_clean_no_box_poster()
