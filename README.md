# PDF Merge & Watermark Tool

## Requirements

- Python 3.7+
- macOS (tested)
- Virtual environment (recommended)

## Setup

1. Clone the repository:
```

git clone https://github.com/yourusername/pdf-merge-watermark.git
cd pdf-merge-watermark

```

2. Create and activate a virtual environment:
```

python3 -m venv venv
source venv/bin/activate

```

3. Install dependencies:
```

pip install -r requirements.txt

```

## Usage

1. Place PDFs to merge in `data/input/`.

2. Run:
```

python pdfmerge/main.py data/output/final.pdf "Watermark Text" data/input/file1.pdf data/input/file2.pdf

```

- The first argument is the **output PDF file name**.
- The second is the **watermark text**.
- The rest are **input PDF file names**.

3. Output will be in `data/output/final.pdf`.

## Project Structure

- **pdfmerge/**: Main logic
- **data/input/**: Input PDFs
- **data/output/**: Output PDFs