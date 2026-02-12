import os
import docx
import pandas as pd
import datetime
import uuid

# Configuration
SOURCE_DIR = r"H:\drive-download-20260120T122959Z-3-001"
TARGET_DIR = r"H:\business"
LOG_FILE = r"H:\decisions\rag_update_log.md"

def log_update(filename, source, summary):
    entry = f"""
### {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} - {filename}
**Action**: Added
**Domain**: business
**Source**: {source}
**Confidence Tier**: 2
**Validation Status**: Automated Import
**Triggered By**: Cadznce Ryvn Ingestion
**Summary**: {summary}

***
"""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)

def read_docx(path):
    try:
        doc = docx.Document(path)
        return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    except Exception as e:
        print(f"Error reading DOCX {path}: {e}")
        return None

def read_xlsx(path):
    try:
        # Read all sheets
        xl = pd.read_excel(path, sheet_name=None)
        text = ""
        for sheet_name, df in xl.items():
            text += f"## Sheet: {sheet_name}\n\n"
            text += df.to_markdown(index=False) + "\n\n"
        return text
    except Exception as e:
        print(f"Error reading XLSX {path}: {e}")
        return None

def create_markdown_file(filename, title, content, source_path):
    if not content:
        return
        
    md_content = f"""# {title}

**Domain**: business
**Knowledge Classification**: Industry_Best_Practice
**Source**: {source_path}
**Date**: {datetime.datetime.now().strftime('%Y-%m-%d')}
**Confidence Tier**: 2
**Author/Authority**: Cadznce Ryvn Brand Team

***

## Summary
Ingested brand documentation for Cadznce Ryvn.

***

## Detailed Content

{content}

***

**Last Updated**: {datetime.datetime.now().strftime('%Y-%m-%d')}
**Status**: Active
"""
    
    output_path = os.path.join(TARGET_DIR, filename)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Created: {output_path}")
    
    log_update(filename, source_path, "Ingested Cadznce Ryvn brand document.")

def main():
    print(f"Scanning {SOURCE_DIR}...")
    
    for root, dirs, files in os.walk(SOURCE_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            content = None
            
            if file.endswith(".docx"):
                content = read_docx(file_path)
            elif file.endswith(".xlsx"):
                content = read_xlsx(file_path)
            
            if content:
                # Create safe filename
                safe_name = f"cadrvn_{file.replace(' ', '_').replace('.docx', '').replace('.xlsx', '')}.md"
                create_markdown_file(safe_name, f"Cadznce Ryvn: {file}", content, file_path)

if __name__ == "__main__":
    main()
