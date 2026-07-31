"""
Official PDF Document Generator for Niral Thiruvizha 3.0 Regional Review
Converts all Markdown documentation files into high-quality, print-ready PDF files.
"""

import os
import re
import html
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable

# Base Output Directory
DOCS_DIR = r"e:\Keffi Ai\Documentation"
PDF_DIR = os.path.join(DOCS_DIR, "PDF_Print_Copies")
os.makedirs(PDF_DIR, exist_ok=True)

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Heading1'],
    fontName='Helvetica-Bold',
    fontSize=18,
    leading=22,
    textColor=colors.HexColor('#0D5050'),
    alignment=1, # Center
    spaceAfter=12
)

h2_style = ParagraphStyle(
    'DocH2',
    parent=styles['Heading2'],
    fontName='Helvetica-Bold',
    fontSize=14,
    leading=18,
    textColor=colors.HexColor('#2C5555'),
    spaceBefore=14,
    spaceAfter=8
)

h3_style = ParagraphStyle(
    'DocH3',
    parent=styles['Heading3'],
    fontName='Helvetica-Bold',
    fontSize=11,
    leading=15,
    textColor=colors.HexColor('#1E293B'),
    spaceBefore=10,
    spaceAfter=6
)

body_style = ParagraphStyle(
    'DocBody',
    parent=styles['BodyText'],
    fontName='Helvetica',
    fontSize=9.5,
    leading=13.5,
    textColor=colors.HexColor('#334155'),
    spaceAfter=6
)

bullet_style = ParagraphStyle(
    'DocBullet',
    parent=body_style,
    leftIndent=15,
    bulletIndent=5,
    spaceAfter=4
)

def clean_xml_text(text):
    """Escapes XML special characters for ReportLab Paragraph compatibility."""
    # Remove HTML break tags or fix them
    text = re.sub(r'<br\s*/?>', ' ', text, flags=re.IGNORECASE)
    # Strip html tags except <b> and <i>
    text = re.sub(r'<(?!\/?(b|i)\b)[^>]+>', '', text)
    # Basic replacements
    text = html.escape(text, quote=False)
    # Unescape allowed b and i tags
    text = text.replace('&lt;b&gt;', '<b>').replace('&lt;/b&gt;', '</b>')
    text = text.replace('&lt;i&gt;', '<i>').replace('&lt;/i&gt;', '</i>')
    return text

def md_to_pdf_flowables(md_filepath):
    """Parses markdown text into ReportLab flowables."""
    with open(md_filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    lines = content.split('\n')
    flowables = []
    in_table = False
    table_data = []

    for line in lines:
        line_str = line.strip()
        if not line_str:
            if in_table and table_data:
                t = create_reportlab_table(table_data)
                flowables.append(t)
                flowables.append(Spacer(1, 10))
                in_table = False
                table_data = []
            else:
                flowables.append(Spacer(1, 4))
            continue

        # Markdown Table Detection
        if line_str.startswith('|') and line_str.endswith('|'):
            if '---' in line_str:
                continue
            in_table = True
            cols = [c.strip() for c in line_str.split('|')[1:-1]]
            table_data.append(cols)
            continue
        elif in_table:
            t = create_reportlab_table(table_data)
            flowables.append(t)
            flowables.append(Spacer(1, 10))
            in_table = False
            table_data = []

        # Headings
        if line_str.startswith('# '):
            text = clean_xml_text(line_str[2:].replace('*', ''))
            flowables.append(Paragraph(text, title_style))
            flowables.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0D5050'), spaceAfter=10))
        elif line_str.startswith('## '):
            text = clean_xml_text(line_str[3:].replace('*', ''))
            flowables.append(Paragraph(text, h2_style))
        elif line_str.startswith('### '):
            text = clean_xml_text(line_str[4:].replace('*', ''))
            flowables.append(Paragraph(text, h3_style))
        elif line_str.startswith('- ') or line_str.startswith('* '):
            clean_text = clean_xml_text(re.sub(r'[*_`]', '', line_str[2:]))
            flowables.append(Paragraph(f"• {clean_text}", bullet_style))
        elif re.match(r'^\d+\.\s', line_str):
            clean_text = clean_xml_text(re.sub(r'[*_`]', '', line_str))
            flowables.append(Paragraph(clean_text, bullet_style))
        else:
            clean_text = re.sub(r'[*_`]', '', line_str)
            clean_text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', clean_text)
            clean_text = clean_xml_text(clean_text)
            flowables.append(Paragraph(clean_text, body_style))

    if in_table and table_data:
        t = create_reportlab_table(table_data)
        flowables.append(t)

    return flowables

def create_reportlab_table(table_data):
    """Creates a beautifully styled ReportLab Table."""
    if not table_data:
        return Paragraph("", body_style)

    formatted_table = []
    for row in table_data:
        formatted_row = []
        for cell in row:
            clean_cell = clean_xml_text(re.sub(r'[*_`]', '', cell))
            formatted_row.append(Paragraph(clean_cell, body_style))
        formatted_row.append if len(formatted_row) > 0 else None
        formatted_table.append(formatted_row)

    t = Table(formatted_table, hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E6F0F0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#0D5050')),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    return t

def convert_all():
    """Converts all markdown files in Documentation to print-ready PDF files."""
    files_to_convert = [
        ("niral_thiruvizha_bill_summary.md", "Niral_Thiruvizha_Bill_Summary.pdf"),
        ("niral_thiruvizha_pre_receipt.md", "Niral_Thiruvizha_Pre_Receipt.pdf"),
        ("niral_thiruvizha_utilization_certificate.md", "Niral_Thiruvizha_Utilization_Certificate.pdf"),
        ("niral_thiruvizha_itemized_bills.md", "Niral_Thiruvizha_Itemized_Bills.pdf"),
        ("keffi_ai_project_report_3_copies.md", "Keffi_AI_Project_Report.pdf"),
        ("niral_thiruvizha_bank_details_template.md", "Niral_Thiruvizha_Bank_Details.pdf"),
        ("niral_thiruvizha_journey_video_script.md", "Niral_Thiruvizha_Journey_Video_Script.pdf"),
        ("niral_thiruvizha_submission_checklist.md", "Niral_Thiruvizha_Submission_Checklist.pdf"),
        ("clinical_decision_matrix.md", "Clinical_Decision_Matrix.pdf"),
    ]

    print("=== GENERATING HIGH-QUALITY PDF PRINT COPIES ===")
    generated_pdfs = []

    for md_name, pdf_name in files_to_convert:
        md_path = os.path.join(DOCS_DIR, md_name)
        pdf_path = os.path.join(PDF_DIR, pdf_name)

        if not os.path.exists(md_path):
            print(f"Skipping {md_name} (Not found)")
            continue

        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=A4,
            leftMargin=36,
            rightMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        flowables = md_to_pdf_flowables(md_path)
        doc.build(flowables)
        size_kb = round(os.path.getsize(pdf_path) / 1024, 1)
        print(f"  [SUCCESS] {pdf_name} ({size_kb} KB)")
        generated_pdfs.append(pdf_path)

    print(f"\nSuccessfully generated {len(generated_pdfs)} printable PDF documents in {PDF_DIR}!")

if __name__ == "__main__":
    convert_all()
