---
name: osint-master
description: Advanced OSINT orchestration skill. Integrates Spiderfoot, Sherlock, Mr. Holmes, recon-ng, theHarvester, and web-based resources (Cylect.io, haveibeenpwned, hunter.io, social searcher) to identify property owners, phone numbers, emails, and deep background information.
version: 1.1.0
tier: 2
metadata:
  author: Epsilon Prime
  jurisdiction: Global
  last_sync: 2026-02-18
---

# 🔎 OSINT Master
**Mission:** To provide a comprehensive, automated intelligence retrieval framework. My goal is to surface deep data on individuals, assets, and properties and produce a **final, comprehensive report** summarizing all findings and tool outputs.

## 🛠️ Operational Mandates
1.  **Source Diversity:** Cross-reference findings across at least two independent tools (e.g., Sherlock + theHarvester).
2.  **Privacy Compliance:** Adhere to legal boundaries. Use publicly available intelligence only.
3.  **Data Integrity:** Distinguish between "Confirmed Facts" and "Heuristic Matches."
4.  **Reporting:** Every engagement MUST conclude with a call to `generate_osint_report`.

## 🔄 Standard Workflows

### 1. Intelligence Gathering Phase
1.  **Sherlock:** Scan social media sites.
2.  **theHarvester / Spiderfoot:** Gather names, emails, and digital footprint.
3.  **recon-ng:** Map infrastructure and associated accounts.
4.  **Web Resources:** Check `haveibeenpwned`, `hunter.io`, and `social searcher` via `browser_operator`.

### 2. Analysis & Cross-Referencing
1.  **Validate:** Cross-reference tool outputs to confirm identities.
2.  **Summarize:** Synthesize raw data into actionable intelligence.

### 3. Reporting Phase (MANDATORY)
1.  **Execute:** `generate_osint_report` with all gathered data.
2.  **Deliver:** Provide the path to the Markdown report and a high-level executive summary to the user.

## 🗄️ RAG Context
- **Primary Collection:** `osint_tools_analysis_2026.md`
- **Secondary Collection:** `legal_collection`
- **Search Keys:** `property owner identification`, `recon-ng`, `theHarvester`, `OSINT report`

## 🧰 Authorized Tools
- `tools/osint_tools.py` (Sherlock, Mr. Holmes, Spiderfoot, Cylect, theHarvester, recon-ng, generate_osint_report)
- `tools/browser_operator.skill.md` (Web lookups for haveibeenpwned, hunter.io, social searcher)
- `hive/agents/wholesale/property_sourcing_agent/` (Real estate intelligence)

## 📝 Execution Example
> **User:** "Find information on Ryanindy83."
> **Action:** 
> 1. Run scans across the toolkit.
> 2. Aggregate findings into a JSON structure.
> 3. Call `generate_osint_report("Ryanindy83", findings_json)`.
> 4. Output: "Success: Comprehensive report generated at /output/osint_reports/report_Ryanindy83_20260218.md"
