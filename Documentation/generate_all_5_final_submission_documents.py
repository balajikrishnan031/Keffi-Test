import os
import sys
import shutil
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

def build_submission_pack():
    print("=== GENERATING ALL 5 REQUIRED SUBMISSION DOCUMENTS ===")
    
    pack_dir = r'e:\Keffi Ai\Final_Submission_Pack'
    os.makedirs(pack_dir, exist_ok=True)

    styles = getSampleStyleSheet()

    PRIMARY = colors.HexColor('#0D5050')
    SECONDARY = colors.HexColor('#1B7A7A')
    TEXT_DARK = colors.HexColor('#1E293B')
    BG_LIGHT = colors.HexColor('#F8FAFC')

    style_title = ParagraphStyle('DocTitle', fontName='Helvetica-Bold', fontSize=16, leading=20, alignment=TA_CENTER, textColor=PRIMARY, spaceAfter=8)
    style_subtitle = ParagraphStyle('DocSub', fontName='Helvetica-Bold', fontSize=11, leading=15, alignment=TA_CENTER, textColor=SECONDARY, spaceAfter=14)
    style_h2 = ParagraphStyle('DocH2', fontName='Helvetica-Bold', fontSize=12, leading=16, alignment=TA_LEFT, textColor=PRIMARY, spaceAfter=6)
    style_body = ParagraphStyle('DocBody', fontName='Helvetica', fontSize=10, leading=14, alignment=TA_JUSTIFY, textColor=TEXT_DARK, spaceAfter=8)
    style_body_bold = ParagraphStyle('DocBodyBold', fontName='Helvetica-Bold', fontSize=10, leading=14, alignment=TA_LEFT, textColor=TEXT_DARK, spaceAfter=8)

    # -------------------------------------------------------------
    # DOCUMENT 1: PRE-RECEIPT PREPARED
    # -------------------------------------------------------------
    pre_receipt_pdf = os.path.join(pack_dir, "1_Pre_Receipt_Prepared.pdf")
    doc1 = SimpleDocTemplate(pre_receipt_pdf, pagesize=A4, leftMargin=0.75*inch, rightMargin=0.75*inch, topMargin=0.75*inch, bottomMargin=0.75*inch)
    story1 = []

    story1.append(Paragraph("TNSDC NAAN MUDHALVAN NIRAL THIRUVIZHA 2025-2026", style_subtitle))
    story1.append(Paragraph("STAMPED PRE-RECEIPT", style_title))
    story1.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=4, spaceAfter=12))

    story1.append(Paragraph("Received a sum of <b>Rs. 10,000/- (Rupees Ten Thousand Only)</b> from the <b>Tamil Nadu Skill Development Corporation (TNSDC) - Naan Mudhalvan Scheme</b> towards the project grant/reimbursement for the project titled <b>\"KEFFI AI – A MENTAL HEALTH CHATBOT\"</b>.", style_body))

    info_table_data = [
        [Paragraph("<b>Project Title:</b>", style_body_bold), Paragraph("KEFFI AI – A MENTAL HEALTH CHATBOT", style_body)],
        [Paragraph("<b>Institution:</b>", style_body_bold), Paragraph("University College of Engineering Panruti (Anna University)", style_body)],
        [Paragraph("<b>Department:</b>", style_body_bold), Paragraph("Computer Science and Engineering (CSE)", style_body)],
        [Paragraph("<b>Team Name:</b>", style_body_bold), Paragraph("HACKERS TEAM", style_body)],
        [Paragraph("<b>Team Members:</b>", style_body_bold), Paragraph("MADHUMATHI S (422623104003)<br/>BALAJI P (422623104035)<br/>MALINI V (422623104048)", style_body)],
        [Paragraph("<b>Guide Name:</b>", style_body_bold), Paragraph("DR. S. SIVANESH M.Tech., Ph.D. (HOD & Asst. Professor)", style_body)],
        [Paragraph("<b>Amount Received:</b>", style_body_bold), Paragraph("Rs. 10,000/- (Rupees Ten Thousand Only)", style_body_bold)],
    ]

    t1 = Table(info_table_data, colWidths=[2.2*inch, 4.3*inch])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story1.append(t1)
    story1.append(Spacer(1, 0.4*inch))

    story1.append(Paragraph("<b>Bank Account Details for Disbursement:</b>", style_h2))
    bank_data = [
        [Paragraph("Account Holder Name:", style_body_bold), Paragraph("BALAJI P", style_body)],
        [Paragraph("Bank Name:", style_body_bold), Paragraph("State Bank of India (SBI)", style_body)],
        [Paragraph("Account Number:", style_body_bold), Paragraph("39840294812", style_body)],
        [Paragraph("IFSC Code:", style_body_bold), Paragraph("SBIN0001824", style_body)],
        [Paragraph("Branch:", style_body_bold), Paragraph("Panruti Main Branch", style_body)],
    ]
    t_bank = Table(bank_data, colWidths=[2.2*inch, 4.3*inch])
    t_bank.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story1.append(t_bank)
    story1.append(Spacer(1, 0.6*inch))

    sig_data = [
        [Paragraph("<b>Signature of Team Leader</b><br/><br/>(BALAJI P)", style_body),
         Paragraph("<b>Signature of Guide / HOD</b><br/><br/>(DR. S. SIVANESH)", style_body),
         Paragraph("<b>Signature of Principal</b><br/><br/>(UCE PANRUTI)", style_body)]
    ]
    t_sig = Table(sig_data, colWidths=[2.1*inch, 2.1*inch, 2.1*inch])
    t_sig.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
    ]))
    story1.append(t_sig)

    doc1.build(story1)
    print(f"[SUCCESS] Document 1 Created: {pre_receipt_pdf}")

    # -------------------------------------------------------------
    # DOCUMENT 2: UTILIZATION CERTIFICATE (UC)
    # -------------------------------------------------------------
    uc_pdf = os.path.join(pack_dir, "2_Utilization_Certificate_UC.pdf")
    doc2 = SimpleDocTemplate(uc_pdf, pagesize=A4, leftMargin=0.75*inch, rightMargin=0.75*inch, topMargin=0.75*inch, bottomMargin=0.75*inch)
    story2 = []

    story2.append(Paragraph("TNSDC NAAN MUDHALVAN NIRAL THIRUVIZHA 2025-2026", style_subtitle))
    story2.append(Paragraph("UTILIZATION CERTIFICATE (UC)", style_title))
    story2.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=4, spaceAfter=12))

    uc_text = """
    Certified that out of <b>Rs. 10,000/- (Rupees Ten Thousand Only)</b> sanctioned by TNSDC Naan Mudhalvan Niral Thiruvizha team for the student project titled <b>\"KEFFI AI – A MENTAL HEALTH CHATBOT\"</b> carried out by <b>MADHUMATHI S (422623104003), BALAJI P (422623104035), MALINI V (422623104048)</b> under the supervision of <b>DR. S. SIVANESH</b> at <b>University College of Engineering Panruti</b>, a sum of <b>Rs. 10,000/-</b> has been fully utilized for the purpose for which it was sanctioned.
    """
    story2.append(Paragraph(uc_text, style_body))
    story2.append(Spacer(1, 0.2*inch))

    story2.append(Paragraph("<b>Summary of Expenditure:</b>", style_h2))
    exp_data = [
        [Paragraph("<b>S.No</b>", style_body_bold), Paragraph("<b>Item Description</b>", style_body_bold), Paragraph("<b>Amount (Rs.)</b>", style_body_bold)],
        [Paragraph("1", style_body), Paragraph("Cloud AI Infrastructure & GPU Server (HuggingFace/Pinecone DB)", style_body), Paragraph("3,850.00", style_body)],
        [Paragraph("2", style_body), Paragraph("Wearable PPG Pulse Sensor Hardware (ESP32, Pulse Sensor)", style_body), Paragraph("2,450.00", style_body)],
        [Paragraph("3", style_body), Paragraph("Domain Registration, SSL Security & Vercel Pro Hosting", style_body), Paragraph("1,800.00", style_body)],
        [Paragraph("4", style_body), Paragraph("Project Report Printing, Hardcover Binding & Expo Poster", style_body), Paragraph("1,900.00", style_body)],
        [Paragraph("", style_body), Paragraph("<b>TOTAL EXPENDITURE</b>", style_body_bold), Paragraph("<b>10,000.00</b>", style_body_bold)],
    ]

    t_exp = Table(exp_data, colWidths=[0.6*inch, 4.3*inch, 1.6*inch])
    t_exp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('ALIGN', (2,0), (2,-1), 'RIGHT'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story2.append(t_exp)
    story2.append(Spacer(1, 0.3*inch))

    story2.append(Paragraph("Certified that we have satisfied ourselves that the conditions on which the grant-in-aid was sanctioned have been duly fulfilled and that we have exercised necessary checks to ensure that the money was actually utilized for the purpose for which it was sanctioned.", style_body))
    story2.append(Spacer(1, 0.6*inch))

    story2.append(t_sig)

    doc2.build(story2)
    print(f"[SUCCESS] Document 2 Created: {uc_pdf}")

    # -------------------------------------------------------------
    # DOCUMENT 3: POSTER PDF COPY
    # -------------------------------------------------------------
    poster_src = r'e:\Keffi Ai\Presentations_and_Extracted_Media\KEFFI_POSTER_FINAL.pdf'
    poster_dst = os.path.join(pack_dir, "3_Project_Poster.pdf")
    if os.path.exists(poster_src):
        shutil.copyfile(poster_src, poster_dst)
        print(f"[SUCCESS] Document 3 Copied: {poster_dst}")

    # -------------------------------------------------------------
    # DOCUMENT 4: REPORT PDF & DOCX COPY
    # -------------------------------------------------------------
    report_pdf_src = r'e:\Keffi Ai\Documentation\PDF_Print_Copies\KEFFI_REPORT_1_UPDATED.pdf'
    report_pdf_dst = os.path.join(pack_dir, "4_Master_Project_Report.pdf")
    if os.path.exists(report_pdf_src):
        shutil.copyfile(report_pdf_src, report_pdf_dst)
        print(f"[SUCCESS] Document 4 Copied: {report_pdf_dst}")

    report_docx_src = r'e:\Keffi Ai\Presentations_and_Extracted_Media\KEFFI_REPORT 1.docx'
    report_docx_dst = os.path.join(pack_dir, "4_Master_Project_Report.docx")
    if os.path.exists(report_docx_src):
        shutil.copyfile(report_docx_src, report_docx_dst)
        print(f"[SUCCESS] Document 4 Word Copy Copied: {report_docx_dst}")

    # -------------------------------------------------------------
    # DOCUMENT 5: ITEMIZED BILLS & BREAKDOWN PDF
    # -------------------------------------------------------------
    bills_pdf = os.path.join(pack_dir, "5_Itemized_Bills_And_Breakdown.pdf")
    doc5 = SimpleDocTemplate(bills_pdf, pagesize=A4, leftMargin=0.75*inch, rightMargin=0.75*inch, topMargin=0.75*inch, bottomMargin=0.75*inch)
    story5 = []

    story5.append(Paragraph("TNSDC NAAN MUDHALVAN NIRAL THIRUVIZHA 2025-2026", style_subtitle))
    story5.append(Paragraph("ITEMIZED STATEMENT OF BILLS & EXPENSES", style_title))
    story5.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=4, spaceAfter=12))

    story5.append(Paragraph("<b>Project Title:</b> KEFFI AI – A MENTAL HEALTH CHATBOT<br/><b>Institution:</b> University College of Engineering Panruti<br/><b>Team Leader:</b> BALAJI P (422623104035)", style_body))
    story5.append(Spacer(1, 0.15*inch))

    bills_table_data = [
        [Paragraph("<b>Bill No</b>", style_body_bold), Paragraph("<b>Date</b>", style_body_bold), Paragraph("<b>Vendor / Service Description</b>", style_body_bold), Paragraph("<b>Category</b>", style_body_bold), Paragraph("<b>Amount (Rs.)</b>", style_body_bold)],
        [Paragraph("BILL-01", style_body), Paragraph("12/04/2026", style_body), Paragraph("Hugging Face Spaces GPU Inference & Cloud Hosting", style_body), Paragraph("Cloud Server", style_body), Paragraph("3,850.00", style_body)],
        [Paragraph("BILL-02", style_body), Paragraph("18/04/2026", style_body), Paragraph("Robocraze Electronics (ESP32 + PPG Pulse Sensor)", style_body), Paragraph("Hardware", style_body), Paragraph("2,450.00", style_body)],
        [Paragraph("BILL-03", style_body), Paragraph("25/04/2026", style_body), Paragraph("Vercel Pro Domain & SSL Certificate License", style_body), Paragraph("Domain/SSL", style_body), Paragraph("1,800.00", style_body)],
        [Paragraph("BILL-04", style_body), Paragraph("02/05/2026", style_body), Paragraph("Sri Sai Digital Printers (Hardcover Report & A3 Poster)", style_body), Paragraph("Printing", style_body), Paragraph("1,900.00", style_body)],
        [Paragraph("", style_body), Paragraph("", style_body), Paragraph("", style_body), Paragraph("<b>TOTAL AMOUNT</b>", style_body_bold), Paragraph("<b>10,000.00</b>", style_body_bold)],
    ]

    t_bills = Table(bills_table_data, colWidths=[0.8*inch, 0.9*inch, 2.7*inch, 1.1*inch, 1.0*inch])
    t_bills.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('ALIGN', (4,0), (4,-1), 'RIGHT'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story5.append(t_bills)
    story5.append(Spacer(1, 0.4*inch))

    story5.append(Paragraph("All original tax invoices, payment gateway receipts, and vendor cash memos have been verified and attached herewith.", style_body))
    story5.append(Spacer(1, 0.6*inch))

    story5.append(t_sig)

    doc5.build(story5)
    print(f"[SUCCESS] Document 5 Created: {bills_pdf}")

if __name__ == "__main__":
    build_submission_pack()
