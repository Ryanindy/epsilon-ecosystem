# RAG MANAGER SKILL

## SKILL METADATA
- **Skill ID**: rag_manager
- **Version**: 2.0
- **Type**: Operational / Utility
- **Domain**: Knowledge Management

---

## PURPOSE
To maintain the integrity of the Epsilon Prime Knowledge Base (`rag/`). Ensures all ingested data meets the 13-field metadata standard and enforces the "Newest First" versioning policy.

---

## METADATA STANDARD (The "Prime 13")

Every file in `rag/` should ideally contain (in header):
1.  **source_id**: Unique ID (e.g., `file_name_hash`)
2.  **title**: Document title
3.  **publisher**: Origin (e.g., "K&F Dynamics", "US Congress")
4.  **author**: Creator name
5.  **publication_date**: Original date
6.  **ingestion_date**: System entry date
7.  **url_or_locator**: File path or URL
8.  **jurisdiction_tags**: `US-WA`, `US-FED`, `GLOBAL`
9.  **classification**: (See GEMINI.md types)
10. **risk_tier**: LOW / MEDIUM / HIGH
11. **scs_score**: Source Confidence Score (0.0-1.0)
12. **version**: v1, v33, v41, etc.
13. **status**: `active` or `deprecated`

---

## VERSION CONTROL PROTOCOL

When the Orchestrator requests a file:
1.  **Search**: Find all matches for topic.
2.  **Sort**: Order by `version` (desc) OR `publication_date` (desc).
3.  **Filter**: If a file is marked `deprecated`, exclude it unless "History" was requested.
4.  **Present**: Return the top result.

---

## INGESTION WORKFLOW

When adding new files:
1.  Scan content.
2.  Determine `risk_tier` and `classification`.
3.  Extract date/version from filename/content.
4.  Calculate initial `scs_score` (default 0.7 for internal, 1.0 for law).
5.  Write file with YAML frontmatter header.

---

## USAGE
`gemini skill invoke rag_manager --task "ingest" --path "C:/..."`
`gemini skill invoke rag_manager --task "retrieve" --query "Epsilon Man Book 1"`
