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

def build_exact_poster():
    print("=== RECREATING EXACT ORIGINAL KEFFI_POSTER.PDF LAYOUT WITH LOGOS & UPPERCASE HEADINGS ===")
    
    target_pdf = r'e:\Keffi Ai\Presentations_and_Extracted_Media\KEFFI_POSTER_FINAL.pdf'
    submission_pdf = r'e:\Keffi Ai\Final_Submission_Pack\3_Project_Poster.pdf'
    
    img_logo_left = r'e:\Keffi Ai\Documentation\extracted_poster_images\poster_img_1.png'   # TNSDC Logo
    img_logo_right = r'e:\Keffi Ai\Documentation\extracted_poster_images\poster_img_3.jpg'  # College Logo
    img_arch = r'e:\Keffi Ai\Documentation\extracted_poster_images\poster_img_4.jpg'        # Architecture / System Image

    os.makedirs(os.path.dirname(target_pdf), exist_ok=True)
    os.makedirs(os.path.dirname(submission_pdf), exist_ok=True)

    # Original Poster Dimensions: 960 x 540 pt (13.33 x 7.5 inches landscape)
    POSTER_WIDTH = 960
    POSTER_HEIGHT = 540

    doc = SimpleDocTemplate(
        target_pdf,
        pagesize=(POSTER_WIDTH, POSTER_HEIGHT),
        leftMargin=12,
        rightMargin=12,
        topMargin=10,
        bottomMargin=10
    )

    styles = getSampleStyleSheet()

    # Original Color Palette: Dark Forest Green Headers & Mint Card Accents
    DARK_GREEN = colors.HexColor('#0F3838')     # Dark forest green header
    CARD_BG = colors.HexColor('#F0F7F5')        # Soft mint card background
    CARD_BORDER = colors.HexColor('#8FA989')    # Muted green border
    TEXT_DARK = colors.HexColor('#0F172A')      # Dark slate text
    ACCENT_TEAL = colors.HexColor('#0D7070')    # Bold accent teal

    style_title = ParagraphStyle(
        'PosterTitle',
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=21,
        alignment=TA_CENTER,
        textColor=colors.white
    )

    style_sub = ParagraphStyle(
        'PosterSub',
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#EAF4F0')
    )

    style_meta = ParagraphStyle(
        'PosterMeta',
        fontName='Helvetica',
        fontSize=8.0,
        leading=10.5,
        alignment=TA_CENTER,
        textColor=colors.white
    )

    style_head = ParagraphStyle(
        'CardHead',
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=11.5,
        alignment=TA_LEFT,
        textColor=DARK_GREEN
    )

    style_body = ParagraphStyle(
        'CardBody',
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.2,
        alignment=TA_JUSTIFY,
        textColor=TEXT_DARK,
        spaceAfter=3
    )

    style_bullet = ParagraphStyle(
        'CardBullet',
        fontName='Helvetica',
        fontSize=7.0,
        leading=9.0,
        alignment=TA_LEFT,
        textColor=TEXT_DARK,
        spaceAfter=2
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

    header_table = Table([[img_l, p_header, img_r]], colWidths=[75, 786, 75])
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
    story.append(Spacer(1, 6))

    # Helper function to generate clean card containers
    def make_card(heading_text, content_elements, width_pt, height_pt=None):
        card_story = []
        p_h = Paragraph(f"<b>{heading_text.upper()}</b>", style_head)
        card_story.append(p_h)
        card_story.append(HRFlowable(width="100%", thickness=1.0, color=CARD_BORDER, spaceBefore=2, spaceAfter=4))
        for item in content_elements:
            card_story.append(item)
        
        t = Table([[card_story]], colWidths=[width_pt])
        t_style = [
            ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
            ('BOX', (0,0), (-1,-1), 1, CARD_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]
        t.setStyle(TableStyle(t_style))
        return t

    # COLUMN 1 (LEFT COLUMN - WIDTH: 300pt)
    c1_1 = Paragraph("Mental healthcare accessibility remains a major global challenge due to high therapy costs, psychiatrist shortages, and social stigma. Psychotherapy is restricted to 1 hour per week, leaving patients unmonitored during the remaining 167 hours of weekly vulnerability. Keffi AI is a clinical digital therapeutics platform developed to bridge this gap, providing 24/7 continuous affective monitoring, hands-free voice interaction, and structured psychological interventions.", style_body)
    card_abstract = make_card("1. ABSTRACT", [c1_1], 304)

    c1_2 = [
        Paragraph("• <b>BERT 96-Emotion Classifier:</b> Classifies complex user statements into 96 distinct emotional categories with 94.2% accuracy.", style_bullet),
        Paragraph("• <b>3-Tier Clinical Response:</b> Combines Rogerian empathy, neurobiological psychoeducation, and CBT grounding skills.", style_bullet),
        Paragraph("• <b>Hands-Free Voice AI:</b> Real-time Web Speech API audio processing for patients in acute panic unable to type.", style_bullet),
        Paragraph("• <b>Write-Ahead Logging (WAL) DB:</b> High-concurrency database eliminating locking crashes during peak usage.", style_bullet),
        Paragraph("• <b>SHAP / LIME Explainable AI:</b> Visual feature attribution maps empowering psychiatrists to audit decisions.", style_bullet),
        Paragraph("• <b>Admin Clinical Hub:</b> Displays Days Inactive metrics and complete scrollable conversation transcripts.", style_bullet),
    ]
    card_highlights = make_card("2. HIGHLIGHTS OF THE PROJECT", c1_2, 304)

    c1_3 = Paragraph("Keffi AI employs a multi-modal affective computing pipeline. User inputs (text or voice) pass through a dual-model cascade: BERT classifies fine-grained emotion vectors while a Librosa audio prosody analyzer extracts acoustic biomarkers (F0 pitch, RMS energy). Context is maintained via WAL relational DB and vector memory. If crisis signals occur, automated n8n workflows alert emergency contacts immediately.", style_body)
    card_methodology = make_card("3. METHODOLOGY", [c1_3], 304)

    col1_cards = [card_abstract, Spacer(1, 4), card_highlights, Spacer(1, 4), card_methodology]

    # COLUMN 2 (CENTER COLUMN - WIDTH: 320pt)
    c2_1 = [
        Paragraph("<b>Step 1: Multimodal Ingestion:</b> Capture user text or voice audio via Web Speech API endpoints.", style_bullet),
        Paragraph("<b>Step 2: BERT Emotion Classification:</b> Classify input across 96 fine-grained emotional state vectors.", style_bullet),
        Paragraph("<b>Step 3: Isolated Context Retrieval:</b> Query WAL database and vector memory using patient ID.", style_bullet),
        Paragraph("<b>Step 4: 3-Tier Therapeutic Generation:</b> Synthesize Rogerian care, neurobiology, and CBT skills.", style_bullet),
        Paragraph("<b>Step 5: Acoustic Prosody & Risk Triage:</b> Compute pitch deltas; trigger n8n crisis alerts if suicidal ideation is flagged.", style_bullet),
        Paragraph("<b>Step 6: Clinician Hub Sync:</b> Update Mental Health Quotient (MHQ) telemetry and log transcripts in Admin Hub.", style_bullet),
    ]
    card_procedure = make_card("4. STEP BY STEP PROCEDURE OR ALGORITHM", c2_1, 318)

    c2_2 = [
        Paragraph("• <b>GoEmotions Multi-Label Dataset:</b> 58,000 curated Reddit comments annotated across 27 emotion categories, extended to 96 clinical psychological states for fine-tuning.", style_bullet),
        Paragraph("• <b>DAIC-WOZ Depression Audio Corpus:</b> Clinical interviews containing acoustic voice prosody benchmarks used to calibrate pitch (F0) and speech pause indicators.", style_bullet),
    ]
    card_dataset = make_card("5. DATASET USED IF ANY", c2_2, 318)

    c2_3 = Paragraph("Keffi AI validates the integration of fine-grained emotion classification, high-concurrency database storage, hands-free voice therapeutics, and clinician tracking into a unified digital platform, closing the 167-hour weekly care gap.", style_body)
    card_conclusion = make_card("7. CONCLUSION", [c2_3], 318)

    col2_cards = [card_procedure, Spacer(1, 4), card_dataset, Spacer(1, 4), card_conclusion]

    # COLUMN 3 (RIGHT COLUMN - WIDTH: 300pt)
    c3_1 = [
        Paragraph("<b>User Input:</b><br/>Spoken audio or text statement:<br/><i>\"I feel completely overwhelmed by exam deadlines, my heart is racing, and I can't sleep.\"</i>", style_bullet),
        Paragraph("<b>System Output:</b><br/>• <b>Tier 1 Validation:</b> <i>\"I hear how much pressure you're under. It's valid to feel overwhelmed.\"</i><br/>• <b>Tier 2 Psychoeducation:</b> <i>\"Your brain's amygdala is triggering a surge in cortisol.\"</i><br/>• <b>Tier 3 CBT Skill:</b> <i>\"Try 4-7-8 breathing: Breathe in for 4s, hold for 7s, exhale for 8s.\"</i><br/>• <b>Voice Readout & Chips:</b> Spoken therapeutic readout and interactive grounding chips.", style_bullet),
    ]
    card_io = make_card("6. INPUT AND OUTPUT", c3_1, 304)

    # Embedded Architecture / System Outcome Diagram Image
    c3_img_element = Image(img_arch, width=290, height=135) if os.path.exists(img_arch) else Paragraph("", style_body)
    card_system_img = make_card("DEVELOPED SYSTEM ARCHITECTURE", [c3_img_element], 304)

    col3_cards = [card_io, Spacer(1, 4), card_system_img]

    # ASSEMBLE 3 COLUMNS SIDE BY SIDE
    main_grid = Table([[col1_cards, col2_cards, col3_cards]], colWidths=[310, 324, 310])
    main_grid.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))

    story.append(main_grid)

    doc.build(story)
    print(f"[SUCCESS] Recreated Exact Poster PDF Generated at: {target_pdf}")

    shutil.copyfile(target_pdf, submission_pdf)
    print(f"[SUCCESS] Synced Recreated Poster PDF to Submission Pack: {submission_pdf}")

if __name__ == "__main__":
    build_exact_poster()
