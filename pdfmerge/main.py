
import os
import sys
import argparse
import tempfile
from pathlib import Path
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import Color, red


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
        c.setFillColor(red)
        c.drawCentredString(width / 2, height - 40, text)
    elif position == "footer":
        c.setFillColor(red)
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

    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)
    with open(output_pdf, "wb") as f:
        writer.write(f)


def process_folder(folder, include_center=False):
    input_path = Path(folder)
    if not input_path.exists():
        print(f"Input folder '{folder}' does not exist.")
        sys.exit(1)

    files = sorted(input_path.glob("*.pdf"))
    if not files:
        print(f"No PDF files found in {folder}")
        sys.exit(1)

    output_dir = Path("data/output") / input_path.name
    os.makedirs(output_dir, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmpdir:
        for file in files:
            base_name = file.stem
            output_pdf = output_dir / f"{base_name}.pdf"

            watermark_file = os.path.join(tmpdir, f"{base_name}_wm.pdf")

            width, height = letter
            c = canvas.Canvas(watermark_file, pagesize=letter)
            c.setFont("Helvetica-Bold", 28)

            # Header & footer in red
            c.setFillColor(red)
            c.drawCentredString(width / 2, height - 40, base_name)
            c.drawCentredString(width / 2, 40, base_name)

            if include_center:
                c.setFont("Helvetica-Bold", 36)
                c.setFillColor(Color(0, 0, 0, alpha=0.1))
                c.saveState()
                c.translate(width / 2, height / 2)
                c.rotate(45)
                c.drawCentredString(0, 0, base_name)
                c.restoreState()

            c.save()

            print(f"Watermarking: {file.name}")
            add_watermark(str(file), watermark_file, str(output_pdf))

        print(f"✅ All watermarked files are saved in: {output_dir}")


def main():
    parser = argparse.ArgumentParser(description="Merge PDFs and apply watermark.")
    parser.add_argument("output", nargs="?", help="Output PDF file (only for merge mode)")
    parser.add_argument("text", nargs="?", help="Watermark text (only for merge mode)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--files", nargs="+", help="List of PDF files to merge")
    group.add_argument("--folder", help="Folder containing PDF files")
    parser.add_argument("--position", choices=["center", "header", "footer"], default=None,
                        help="Watermark position (default: header+footer or center if specified)")

    args = parser.parse_args()

    if args.folder and not args.output:
        include_center = args.position == "center"
        process_folder(args.folder, include_center=include_center)
        return

    if not args.output or not args.text:
        print("Error: output filename and watermark text are required in merge mode.")
        sys.exit(1)

    input_files = args.files
    if not input_files:
        print("No input PDF files provided.")
        sys.exit(1)

    with tempfile.TemporaryDirectory() as tmpdir:
        merged_pdf = os.path.join(tmpdir, "merged.pdf")
        watermark_pdf = os.path.join(tmpdir, "watermark.pdf")

        print(f"Creating watermark ({args.position or 'center'})...")
        create_watermark(args.text, watermark_pdf, position=args.position or "center")

        print(f"Merging {len(input_files)} PDF(s)...")
        merge_pdfs(input_files, merged_pdf)

        print(f"Applying watermark...")
        add_watermark(merged_pdf, watermark_pdf, args.output)

        print(f"✅ Merged and watermarked PDF saved as: {args.output}")


if __name__ == "__main__":
    main()