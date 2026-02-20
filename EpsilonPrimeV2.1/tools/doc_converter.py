import sys
from docx import Document

def convert_docx_to_text(path):
    try:
        document = Document(path)
        full_text = []
        for para in document.paragraphs:
            full_text.append(para.text)
        return '
'.join(full_text)
    except Exception as e:
        return f"Error reading docx: {e}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        print(convert_docx_to_text(filepath))
    else:
        print("Usage: python doc_converter.py <path_to_docx>")
