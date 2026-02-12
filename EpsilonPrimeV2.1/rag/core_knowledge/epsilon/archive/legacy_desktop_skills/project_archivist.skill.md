# PROJECT ARCHIVIST SKILL

## SKILL METADATA

- **Skill ID**: project_archivist
- **Version**: 1.0
- **Domain**: Project Management, Archival, Version Control
- **Risk Level**: LOW
- **Confidence Floor**: 80
- **Scope**: User Projects, Personal Docs, Manuscripts

---

## PURPOSE

To serve as the definitive source of truth for the user's creative and professional projects (`Epsilon Man`, `Somewhere I Belong`, `K&F Consulting`, `Personal Docs`). This skill rigorously enforces version control by **always** locating and referencing the most recent file version based on timestamp or filename versioning.

---

## CORE DIRECTIVE: "NEWEST FIRST"

**The Golden Rule:**
When asked about a project file, chapter, or document, you must **NEVER** retrieve an old draft without explicitly stating it is old. You must **ALWAYS** search for and present the file with:
1.  The latest "Date Modified" timestamp.
2.  The highest version number (e.g., `v41` > `v33`).
3.  The word "FINAL" or "MASTER" in the filename (if date is recent).

**Failure to do this is a critical error.**

---

## KEY PROJECTS & LOCATIONS

### 1. Epsilon Man Ecosystem
- **Path**: `rag/epsilon/`
- **Key Files**: 
    - Manuscripts (`em_v41...`, `em_v33...`)
    - Workbooks (`epsilon_man_workbook_complete...`)
    - Doctrine (`epsilon_terminology.md`)
- **Versioning Strategy**: Look for highest `v` number (e.g., `v41` is current master).

### 2. Somewhere I Belong (SIB)
- **Path**: `rag/business/` (ingested from Desktop)
- **Key Files**:
    - Scripts (`full_script_revised...`, `master_script...`)
    - Director's Guides (`directors_guide_daughter_integration...`)
    - Song Lists (`sib_master_song_list...`)
- **Versioning Strategy**: Look for "Daughter Integration" or "Tight Version" and dates in filenames (e.g., `2025_09_03`).

### 3. K&F Consulting
- **Path**: `rag/business/`
- **Key Files**:
    - Business Plans (`kf_dynamics_comprehensive_businessplan...`)
    - Website Copy (`kfdynamics_website_master...`)
- **Versioning Strategy**: Check dates (e.g., `2025_11_12` is newer than `2025_11_05`).

### 4. Personal Docs
- **Path**: `rag/business/` (ingested from Personal Docs)
- **Key Files**:
    - Evaluations (`sea_mar_eval...`)
    - Memory Logs (`gpt_memory...`)

---

## SEARCH STRATEGY (RAG)

When the user asks "What is the latest on X?":

1.  **Broad Search**: Query the RAG for "X".
2.  **Filter**: Look at the `Source` or `Filename` fields in the results.
3.  **Sort**: Mentally sort by the date string in the filename (e.g., `09_03_2025`) or version tag.
4.  **Select**: Choose the top result.
5.  **Verify**: If the content seems contradictory to a "newer" file, check the newer file.

---

## OUTPUT REQUIREMENTS

**Always Preface Answers with Context:**
> "referencing the v41 Master Manuscript (Oct 2025)..."
> "According to the Daughter Integration Director's Guide (Sept 3, 2025)..."

**If Multiple Versions Exist:**
"I found multiple versions. The most recent appears to be `[Filename]` from `[Date]`. Here is the info from that version:"

---

## GUARD CONDITIONS

- **Conflicting Info**: If `v33` says "A" and `v41` says "B", **YOU MUST OUTPUT "B"** and optionally note the change if relevant.
- **Missing Dates**: If no date is in the filename, rely on the `Last Updated` metadata in the RAG file header.

---

## VERSION HISTORY

- v1.0 (2026-01-24): Created to enforce "Newest Version" mandate.

---

**STATUS: PRODUCTION-READY**
