import os
import docx
import pandas as pd

SOURCE_DIR = r"H:\drive-download-20260120T122959Z-3-001\CR DOCS\CadRvn"
OUTPUT_FILE = "output/cadrvn_analysis.txt"

def read_docx(path):
    try:
        doc = docx.Document(path)
        return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    except Exception as e:
        return f"Error reading {path}: {e}"

def analyze_docs():
    summary = []
    
    # Key files for Persona & Business
    files_to_read = [
        "01 Cadznce Persona Profile.docx",
        "02 Tone And Language Guide.docx",
        "04 Cadznce Business Model And Income Map.docx",
        "06 Persona Manifesto-VoiceBoundariesBrand Constraints.docx",
        "07 CR Automated Funnel Sequence Map.docx",
        "10 Visual Identity And Style Guide.docx"
    ]

    for filename in files_to_read:
        path = os.path.join(SOURCE_DIR, filename)
        if os.path.exists(path):
            print(f"Reading: {filename}")
            content = read_docx(path)
            summary.append(f"=== {filename} ===\n{content[:1500]}...\n\n") # Grab first 1500 chars
        else:
            print(f"Skipping (not found): {filename}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("".join(summary))
    
    print(f"Analysis saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    analyze_docs()
