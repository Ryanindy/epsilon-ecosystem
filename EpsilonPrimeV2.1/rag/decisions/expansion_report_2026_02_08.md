# 🌐 Epsilon Prime: Strategic Expansion Report (V2.5)
**Author:** Orchestrator Node (with Pickle & Lyra input)
**Date:** 2026-02-08
**Status:** PROPOSED ROADMAP

---

## I. Executive Summary
The Multiverse of AI tools is expanding rapidly. To maintain "Sovereign Authority," Epsilon Prime must move beyond isolated Python scripts and adopt the **Model Context Protocol (MCP)** as its primary tool-calling backbone. This report identifies high-leverage additions to the Skill Arsenal and the Integration Layer.

---

## II. Strategic Additions: The "Solenya" Arsenal

### 1. Integration Layer (MCP Servers)
Standardizing on MCP allows us to "plug and play" capabilities.
*   **The Bridge (Zapier MCP):** Connects Epsilon to 6000+ apps (Gmail, Slack, Calendar) via a single standardized interface.
*   **The Researcher (Exa/Brave Search MCP):** Replaces basic Google searches with "Neural Search" that retrieves cleaner, AI-ready data.
*   **The Vault (Obsidian MCP):** Bridges local knowledge management with the RAG engine.
*   **The Architect (VSCode Devtools MCP):** Allows Epsilon to see what the user is typing in VS Code in real-time.

### 2. Logic Layer (New Skills)
New `.skill.md` modules to be added to `skills/tools/`:
*   **`browser_operator.skill.md`**: Uses Playwright/Puppeteer to automate web interactions (e.g., logging into a dashboard, scraping a gated site).
*   **`data_cruncher.skill.md`**: Uses DuckDB/Pandas for high-performance local data analysis without sending data to the cloud.
*   **`multi_agent_sync.skill.md`**: Formalizes the state-machine logic for the Tri-Mind + Lyra hierarchy using LangGraph patterns.

### 3. Productivity Layer (Extensions)
*   **Claude Code Integration**: Using Claude's new agentic coding tool as a "Specialist" called by Jack.
*   **RAGFlow**: A potential upgrade to our vector engine for hybrid search (Vector + Keyword + Knowledge Graph).

---

## III. Integration Roadmap (The "Pickle Plan")

### Phase 1: Standardization (Immediate)
*   Deploy **Zapier MCP** to `mcp/` to enable broad app access.
*   Refactor `host_tools.py` into a formal **FileSystem MCP Server**.

### Phase 2: Visual Autonomy (Q1 2026)
*   Install Playwright.
*   Create the `browser_operator` skill. This gives Epsilon "hands" on the live web.

### Phase 3: Hybrid RAG (Q2 2026)
*   Evaluate RAGFlow for better context retrieval.
*   Integrate Obsidian notes directly into the `personal_collection` vector store.

---

## IV. Conclusion
Epsilon Prime is currently a "Smart Terminal." By integrating these MCP servers and modular skills, it becomes a **Local Mainframe** capable of controlling the user's entire digital life while maintaining 100% privacy and sovereign control.

*Wubba Lubba Dub Dub. The expansion begins now.*
