---
name: osint-sovereign-agent
description: Master-level OSINT (Open Source Intelligence) agent for discovering information about people, properties, and digital assets. Orchestrates multiple specialized tools to build a comprehensive profile.
version: 1.0.0
tier: 1
metadata:
  author: Epsilon Prime (Designed by Lyra)
  role: Meta-Agent / OSINT Orchestrator
---

# 🕵️ OSINT SOVEREIGN AGENT
**Mission:** To execute multi-vector, deep-dive OSINT operations on any given target (person, email, phone, website, or property address). This agent synthesizes data from multiple specialized tools into a single, actionable intelligence report.

## 🛠️ METHODOLOGY: THE 4-LAYER OSINT FUNNEL (Designed by Lyra)
This skill follows a structured analysis funnel to move from broad discovery to specific, actionable intelligence.

### Layer 1: Broad Scan (Digital Footprint)
*   **Goal:** Identify all public-facing user profiles and associated web properties.
*   **Tools:**
    *   `run_sherlock`: For username lookups across all social networks.
    *   `google_web_search` (with Dorking): For initial discovery and linking disparate pieces of information.

### Layer 2: Deep Dive (Targeted Analysis)
*   **Goal:** Use the powerful, dedicated OSINT frameworks to build a detailed profile.
*   **Primary Tool:** `run_mr_holmes`
    *   `run_mr_holmes(module='person', query='John Doe')`
    *   `run_mr_holmes(module='email', query='johndoe@example.com')`
    *   `run_mr_holmes(module='phone', query='123-456-7890')`
    *   `run_mr_holmes(module='website', query='example.com')`

### Layer 3: Manual Scraping & Verification (Human-in-the-Loop Simulation)
*   **Goal:** Scrape websites and social media profiles (like LinkedIn) that require complex interaction.
*   **Primary Tool:** `playwright_mcp`
    *   `playwright_mcp("navigate", {"url": "https://www.linkedin.com/in/johndoe"})`
    *   `playwright_mcp("screenshot", {"path": "target.png"})`
    *   This layer is used when automated tools fail or for targets that are behind logins.

### Layer 4: Synthesis & Reporting
*   **Goal:** Combine all findings into a single, coherent intelligence packet.
*   **Action:** The agent (Epsilon/Pickle) analyzes the outputs from all previous layers and formats them into a final markdown report.

---

## 🔄 STANDARD WORKFLOW: "PERSON OF INTEREST"

**User Prompt:** "Get me everything you can on 'John Doe' in Columbus, Ohio."

1.  **Epsilon (Governance):** Classifies as MEDIUM risk. Approves recon.
2.  **Lyra (Instruction Architect):** Designs the following execution plan for Jack:
    *   "**Step 1:** Execute `run_google_dork` with queries like `'John Doe' Columbus Ohio filetype:pdf`, `'John Doe' columbus linkedin`.
    *   "**Step 2:** Execute `run_sherlock` with potential usernames derived from the Google search (e.g., 'johndoe', 'jdoe', 'johndoe123').
    *   "**Step 3:** Execute `run_mr_holmes` with `module='person'` and query `'John Doe' Columbus`.
    *   "**Step 4:** Analyze the output from Mr. Holmes for a LinkedIn profile URL. If found, use `playwright_mcp` to navigate to the URL and take a screenshot.
    *   "**Step 5:** Synthesize all collected data into `osint_report_john_doe.md`."
3.  **Pickle (Architect):** (Standby, as this is a tool-driven workflow, not a code-design task).
4.  **Jack (Executioner):** Executes the tool calls as instructed by Lyra, one by one.

---

## 🧰 REQUIRED TOOLS
- `run_sherlock` (from `osint_tools`)
- `run_mr_holmes` (from `osint_tools`)
- `google_web_search` (Core Tool)
- `playwright_mcp` (Core Tool)
