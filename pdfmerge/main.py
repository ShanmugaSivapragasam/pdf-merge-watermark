import sys
import os
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_watermark(text, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica", 36)
    c.setFillAlpha(0.2)
    width, height = letter
    # Header
    c.drawCentredString(width / 2, height - 40, text)
    # Footer
    c.drawCentredString(width / 2, 40, text)
    # Diagonal center
    # c.saveState()
    # c.translate(width / 2, height / 2)
    # c.rotate(45)
    # c.drawCentredString(0, 0, text)
    # c.restoreState()
    c.save

def create_watermark_debug(text, filename):
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        import os

        # Ensure output directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        c = canvas.Canvas(filename, pagesize=letter)
        c.setFont("Helvetica", 36)
        c.setFillAlpha(0.2)
        c.setFillColor("red")
        width, height = letter
        # Header
        c.drawCentredString(width / 2, height - 40, text)
        # Footer
        c.drawCentredString(width / 2, 40, text)
        # (Optional) Diagonal center -- comment out if not needed
        # c.saveState()
        # c.translate(width / 2, height / 2)
        # c.rotate(45)
        # c.drawCentredString(0, 0, text)
        # c.restoreState()
        c.save()
        print(f"Watermark PDF created successfully at: {os.path.abspath(filename)}")
        # Double-check file existence
        if not os.path.isfile(filename):
            print(f"ERROR: File was not created at {filename}")
    except Exception as e:
        print(f"Exception while creating watermark PDF: {e}")
        import traceback
        traceback.print_exc()


def merge_pdfs(pdf_list, output):
    writer = PdfWriter()
    for pdf in pdf_list:
        reader = PdfReader(pdf)
        for page in reader.pages:
            writer.add_page(page)
    with open(output, "wb") as f:
        writer.write(f)

def add_watermark(input_pdf, watermark_pdf, output_pdf):
    watermark = PdfReader(watermark_pdf).pages[0]
    reader = PdfReader(input_pdf)
    writer = PdfWriter()
    for page in reader.pages:
        page.merge_page(watermark)
        writer.add_page(page)
    with open(output_pdf, "wb") as f:
        writer.write(f)

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python main.py <output.pdf> <watermark text> <input1.pdf> <input2.pdf> ...")
        sys.exit(1)
    output_file = sys.argv[1]
    watermark_text = sys.argv[2]
    input_files = sys.argv[3:]
    merged_pdf = "data/output/_merged.pdf"
    watermark_pdf = "data/output/_watermark.pdf"
    os.makedirs("data/output", exist_ok=True)
    create_watermark_debug(watermark_text, watermark_pdf)
    # create_watermark(watermark_text, watermark_pdf)
    print(f"Watermark PDF created: {os.path.abspath(watermark_pdf)}")
    merge_pdfs(input_files, merged_pdf)
    add_watermark(merged_pdf, watermark_pdf, output_file)
    print(f"Merged and watermarked PDF saved as {output_file}")
