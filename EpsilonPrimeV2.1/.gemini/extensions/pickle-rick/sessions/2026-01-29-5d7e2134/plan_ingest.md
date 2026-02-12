# Ingest Legacy Personal Docs - Implementation Plan

## Overview
We need to ingest the user's "Personal history docs" folder into the RAG system. This folder contains legacy binary formats (.doc, .xls, .ppt) from 2003-2009. We will create a specialized script to extract text from these legacy files and save them as Markdown artifacts in `rag/identity/archives/`.

## Current State Analysis
- **Source**: `C:\Users\Media Server\Desktop\Personal history docs`
- **Formats**: `.doc` (Word 97-2003), `.xls` (Excel 97-2003), `.ppt` (PowerPoint 97-2003).
- **Tools**: Standard `python-docx` and `openpyxl` do NOT support these binary formats. We need `olefile` or `textract` (which requires external binaries) or `pypiwin32` (COM automation) since we are on Windows. **Decision**: Use `pypiwin32` (win32com.client) as it is the most reliable way to read legacy Office files on a Windows machine with Office installed, OR `textract`.
- **Constraint**: If Office is not installed, we fallback to strings extraction or specialized libraries (`xlrd` for xls).

## Implementation Approach
1.  **Dependencies**: Check for `pywin32`.
2.  **Script**: Create `ingest_legacy.py`.
3.  **Logic**:
    - Recursively scan `C:\Users\Media Server\Desktop\Personal history docs`.
    - Detect file type.
    - Extract text.
    - Create a Markdown file in `rag/identity/archives/` with metadata headers.

## Phase 1: Dependency Check & Setup
### Overview
Ensure we have the tools to read `.doc` and `.xls`.
### Changes Required:
#### 1. `ingest_legacy.py` (Skeleton)
- Check imports.
- Define `EXTRACTORS` map.

## Phase 2: Extraction Logic
### Overview
Implement specific extractors for each legacy type.
### Changes Required:
#### 1. `ingest_legacy.py` (Implementation)
- **DocExtractor**: Use `win32com` if available, else simple binary string scraping (low quality but safe).
- **XlsExtractor**: Use `pandas` with `xlrd` engine (supports .xls).
- **PptExtractor**: Use `win32com` or skip if too complex, maybe just binary strings.

## Phase 3: Execution
### Overview
Run the script and verify output.
### Changes Required:
#### 1. Run Command
`python ingest_legacy.py`

### Success Criteria:
#### Automated:
- [ ] Script runs without crashing.
- [ ] `rag/identity/archives/` contains .md files corresponding to the source files.
#### Manual:
- [ ] Verify content of a few generated MD files.

## Review Criteria
- **Safety**: Do not overwrite existing RAG files. Use unique names.
- **Privacy**: Ensure PII is handled (though this is local RAG, so low risk).
