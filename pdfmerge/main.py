import os
import sys
import argparse
import tempfile
from pathlib import Path
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import Color

def create_watermark(text, output_path, position="center"):
    width, height = letter
    c = canvas.Canvas(output_path, pagesize=letter)
    c.setFont("Helvetica-Bold", 36)

    if position == "center":
        c.setFillColor(Color(0, 0, 0, alpha=0.1))  # Light gray
        c.saveState()
        c.translate(width / 2, height / 2)
        c.rotate(45)
        c.drawCentredString(0, 0, text)
        c.restoreState()
    elif position == "header":
        c.setFillColor(Color(0.2, 0.2, 0.2, alpha=0.8))  # Darker
        c.drawCentredString(width / 2, height - 40, text)
    elif position == "footer":
        c.setFillColor(Color(0.2, 0.2, 0.2, alpha=0.8))  # Darker
        c.drawCentredString(width / 2, 40, text)
    else:
        raise ValueError("Invalid position. Choose from: center, header, footer")

    c.save()

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

    # Ensure output folder exists
    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)

    with open(output_pdf, "wb") as f:
        writer.write(f)

def get_input_files(folder=None, files=None):
    if folder:
        return sorted([str(f) for f in Path(folder).glob("*.pdf")])
    if files:
        return files
    return []

def main():
    parser = argparse.ArgumentParser(description="Merge PDFs and apply watermark.")
    parser.add_argument("output", help="Output PDF file name")
    parser.add_argument("text", help="Watermark text")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--files", nargs="+", help="List of PDF files to merge")
    group.add_argument("--folder", help="Folder containing PDF files")
    parser.add_argument("--position", choices=["center", "header", "footer"], default="center",
                        help="Watermark position (default: center)")

    args = parser.parse_args()

    input_files = get_input_files(args.folder, args.files)
    if not input_files:
        print("No input PDF files found.")
        sys.exit(1)

    with tempfile.TemporaryDirectory() as tmpdir:
        merged_pdf = os.path.join(tmpdir, "merged.pdf")
        watermark_pdf = os.path.join(tmpdir, "watermark.pdf")

        print(f"Creating watermark ({args.position})...")
        create_watermark(args.text, watermark_pdf, args.position)

        print(f"Merging {len(input_files)} PDF(s)...")
        merge_pdfs(input_files, merged_pdf)

        print(f"Applying watermark...")
        add_watermark(merged_pdf, watermark_pdf, args.output)

        print(f"✅ Watermarked PDF saved as: {args.output}")

if __name__ == "__main__":
    main()