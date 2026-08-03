import os

def export_pw_to_pdf():
    print("=== EXPORTING PURE WHITE TIMES NEW ROMAN DECK TO PDF ===")

    pptx_path = r"e:\Keffi Ai\Final_Submission_Pack\KEFFI_PURE_WHITE_TIMES_ROMAN_25_SLIDE_MASTER.pptx"
    pdf_path_1 = r"e:\Keffi Ai\Final_Submission_Pack\KEFFI_PURE_WHITE_TIMES_ROMAN_25_SLIDE_MASTER.pdf"
    pdf_path_2 = r"e:\Keffi Ai\Presentations_and_Extracted_Media\KEFFI_PURE_WHITE_TIMES_ROMAN_25_SLIDE_MASTER.pdf"

    try:
        import comtypes.client
        powerpoint = comtypes.client.CreateObject("PowerPoint.Application")
        powerpoint.Visible = 1

        abs_pptx = os.path.abspath(pptx_path)
        abs_pdf1 = os.path.abspath(pdf_path_1)
        abs_pdf2 = os.path.abspath(pdf_path_2)

        deck = powerpoint.Presentations.Open(abs_pptx)
        deck.SaveAs(abs_pdf1, 32)
        deck.SaveAs(abs_pdf2, 32)
        deck.Close()
        powerpoint.Quit()

        print(f"[SUCCESS] Exported Pure White Times New Roman Deck to PDF at:\n  1. {pdf_path_1}\n  2. {pdf_path_2}")
    except Exception as e:
        print(f"[NOTE ON EXPORT]: {e}")

if __name__ == "__main__":
    export_pw_to_pdf()
