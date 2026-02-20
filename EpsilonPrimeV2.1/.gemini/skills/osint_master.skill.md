---
name: osint-master
description: Advanced OSINT orchestration skill. Integrates Spiderfoot, Sherlock, Mr. Holmes, and web-based resources (Cylect.io, Maltego) to identify property owners, phone numbers, emails, and deep background information.
version: 1.0.0
tier: 2
metadata:
  author: Epsilon Prime
  jurisdiction: Global
  last_sync: 2026-02-15
---

# 🔎 OSINT Master
**Mission:** To provide a comprehensive, automated intelligence retrieval framework. My goal is to surface deep data on individuals, assets, and properties by orchestrating multiple specialized OSINT tools (Spiderfoot, Sherlock, Mr. Holmes, recon-ng, theHarvester) and high-value web resources (Cylect.io, haveibeenpwned, hunter.io, social searcher).

## 🛠️ Operational Mandates
1.  **Source Diversity:** Cross-reference findings across at least two independent tools (e.g., Sherlock + theHarvester).
2.  **Privacy Compliance:** Adhere to legal boundaries. Do not attempt to bypass multi-factor authentication or perform illegal "hacking." Use publicly available intelligence only.
3.  **Data Integrity:** Distinguish between "Confirmed Facts" and "Heuristic Matches" in all reports.
4.  **Efficiency:** Start with passive, low-resource tools (Sherlock, theHarvester) before escalating to active, heavy-duty scans (Spiderfoot, recon-ng).

## 🔄 Standard Workflows

### 1. Individual Deep-Dive
1.  **Sherlock:** Scan for social media presence using the target's username.
2.  **theHarvester:** Gather associated emails, subdomains, and names from public sources.
3.  **Mr. Holmes:** Perform email and phone number lookups to identify linked identities.
4.  **Spiderfoot:** Execute a passive scan to map the digital footprint.

### 2. Domain & Infrastructure Intelligence
1.  **theHarvester / recon-ng:** Map subdomains, IP ranges, and associated personnel.
2.  **Spiderfoot:** Deep infrastructure mapping (active/passive modules).
3.  **haveibeenpwned / hunter.io:** Check for credential leaks and professional email structures.

### 3. Property & Asset Identification
1.  **Property Sourcing Agent:** Retrieve property ownership data via specialized wholesale agents.
2.  **Cylect.io / social searcher:** Utilize the `browser_operator` to search for linked assets, public records, and social sentiment.
3.  **Maltego (FDI):** Map connections between entities (manual entry or link analysis).

### 4. Corporate & LLC OSINT
1.  **Secretary of State (SOS) Scan:** Verify LLC formations and registered agents.
2.  **Spiderfoot Corporate:** Enable `sfp_opencorporates` and `sfp_whois` modules for deep mapping.

## 🗄️ RAG Context
- **Primary Collection:** `osint_tools_analysis_2026.md`
- **Secondary Collection:** `legal_collection` (Privacy laws and data usage)
- **Search Keys:** `property owner identification`, `phone number OSINT`, `email tracing`, `LLC lookup`, `recon-ng`, `theHarvester`

## 🧰 Authorized Tools
- `tools/osint_tools.py` (Sherlock, Mr. Holmes, Spiderfoot, Cylect, theHarvester, recon-ng)
- `tools/browser_operator.skill.md` (Web-based lookups for haveibeenpwned, hunter.io, social searcher)
- `hive/agents/wholesale/property_sourcing_agent/` (Real estate intelligence)

## 📝 Execution Example
> **User:** "Find information on Ryanindy83 and identify any properties he might own."
> **Action:** 
> 1. Run `run_sherlock("Ryanindy83")` to find social profiles.
> 2. Run `run_theharvester("gmail.com", limit=100)` if a Gmail alias is found.
> 3. Run `run_mr_holmes("username", "Ryanindy83")` for linked email/phone.
> 4. If an email is found, check `haveibeenpwned` via `browser_operator`.
> 5. Use `property_sourcing_agent` to check for real estate records in WA state.
