# PDF Merge & Watermark Tool

## Requirements

- Python 3.7+
- macOS/Linux/Windows (tested on macOS)
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
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

## Usage

### Mode 1: Merge multiple files and apply a single watermark
```
python3 pdfmerge/main.py <output.pdf> <"Watermark Text"> --files file1.pdf file2.pdf ... [--position center|header|footer]
```

Examples:
```
python3 pdfmerge/main.py data/output/final.pdf "Watermark Text" --files data/input/a.pdf data/input/b.pdf
python3 pdfmerge/main.py data/output/reports.pdf "Confidential" --files ./data/input/*.pdf --position center
```

### Mode 2: Process a folder of PDFs with filenames as watermark (header & footer in red, optional center)
```
python3 pdfmerge/main.py --folder <folder_path> [--position center]
```

Example:
```
python3 pdfmerge/main.py --folder ./data/input
python3 pdfmerge/main.py --folder ./data/input --position center
```

- Outputs will be saved to: `data/output/<folder_name>/`
- Header/Footer text will be in red. Center (if enabled) will be light gray.

## Project Structure

- **pdfmerge/**: Main logic
- **data/input/**: Input PDFs
- **data/output/**: Output PDFs