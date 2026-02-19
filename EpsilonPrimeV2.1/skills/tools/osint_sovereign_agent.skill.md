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

## 🛠️ METHODOLOGY: THE RECURSIVE OSINT COGNITIVE LOOP (V2.0)
This skill utilizes a multi-agent swarm to execute automated "Rabbit-Hole" discovery.

### Phase 0: Vector Initialization
*   **Action:** Lead Agent (Epsilon) parses the target for initial vectors (Name, Handle, Email, Phone).
*   **Blackboard:** Sets up the shared memory for the swarm.

### Phase 1: Specialized Execution (Sub-Agents)
The Lead Agent dispatches executors based on the current vector type:
*   **Agent Sherlock:** Multi-platform username tracking.
*   **Agent Footprint:** Spiderfoot infrastructure mapping.
*   **Agent Harvester:** Domain and personnel scraping.
*   **Agent Holmes:** Deep person lookups (Phone/Email/Address).
*   **Agent Web:** Interactive Playwright verification.

### Phase 2: Autonomous Extraction & Recursion
*   **Cognitive Loop:** After each tool run, the Lead Agent scans the output for *new* unique vectors.
*   **Recursion:** If a new email is found during a Sherlock scan, it is automatically queued as a new search target.
*   **Depth Control:** Recursion is managed up to a depth of 5 layers to ensure exhaustive but focused discovery.

### Phase 3: Synthesis & "The Rabbit Hole" Report
*   **Action:** Compiles a master Markdown report that tracks the discovery lineage (how one clue led to another).

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
