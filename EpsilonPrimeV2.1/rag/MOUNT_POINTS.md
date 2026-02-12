# RAG MOUNT POINTS (EXTERNAL STORAGE)

The following external directories are recognized as valid Knowledge Sources for Epsilon Prime V2.1.
Tools like `fs_god.py` and `rag_query.py` may access these paths if the drive is mounted.

## DRIVE I: (The Archive)
**Status:** Mounted
**Path:** `I:`
**Contents:**
*   `I:\business` -> Business entities, tax docs, plans.
*   `I:\legal` -> Case files, statutes (RCW/USC), evidence.
*   `I:\engineering` -> Schematics, STL files, older codebases.
*   `I:\decisions` -> Session Consolidator logs (Legacy).

## USAGE
To ingest data from these sources, run:
`gemini run task ingest --source "I:\legal"`
