import os
import sys
import win32com.client

def convert_docx_to_pdf(docx_path, pdf_path):
    print(f"=== CONVERTING DOCX TO PDF ===")
    print(f"  Input:  {docx_path}")
    print(f"  Output: {pdf_path}")
    
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    try:
        doc = word.Documents.Open(os.path.abspath(docx_path))
        doc.SaveAs(os.path.abspath(pdf_path), FileFormat=17) # 17 = wdFormatPDF
        doc.Close()
        print(f"[SUCCESS] PDF Generated Successfully: {pdf_path}")
    except Exception as e:
        print(f"[ERROR] PDF Conversion failed: {e}")
    finally:
        word.Quit()

if __name__ == "__main__":
    docx_file = r"e:\Keffi Ai\Documentation\KEFFI_MASTER_FINAL_PROJECT_REPORT.docx"
    pdf_file = r"e:\Keffi Ai\Documentation\PDF_Print_Copies\KEFFI_MASTER_FINAL_PROJECT_REPORT.pdf"
    os.makedirs(os.path.dirname(pdf_file), exist_ok=True)
    convert_docx_to_pdf(docx_file, pdf_file)
