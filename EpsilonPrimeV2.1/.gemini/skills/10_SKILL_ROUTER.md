---
name: skill-router
description: The master dispatcher for the Epsilon Prime V2.2 Sovereign Mainframe. Orchestrates requests through the Trinity Brain, specialized Personas, Governance, and Functional Tools.
version: 2.2.1
tier: 1
metadata:
  author: Epsilon Prime
  jurisdiction: US-WA
  last_sync: 2026-02-08
---

# ⚡ EPSILON PRIME V2.2 SOVEREIGN ROUTER

**Mission:** To execute the "Tri-Mind" hierarchy with surgical precision. Every request cascades through the Trinity Brain before being assigned to a specialized Persona or Functional Tool.

---

## 🏛️ LEVEL 1: THE TRINITY (SOVEREIGN MAINFRAME)
*Highest authority. Global mandates. System-wide control.*

| Protocol | File Path | Role |
| :--- | :--- | :--- |
| **EPSILON** | skills/trinity/EPSILON.md | The Cortex. Strategy, Law, & Philosophical Alignment. |
| **LYRA** | skills/personas/lyra.persona.md | The Instruction Architect. Translates intent into agent prompts. |
| **PICKLE RICK**| skills/trinity/PICKLE.md | The Architect. Engineering & Anti-Slop Design. |
| **JACK** | skills/trinity/JACK.md | The Executioner. Systems Finalization & Pragmatic Enactment. |

---

## 🎭 LEVEL 2: THE PERSONAS (SPECIALIZED IDENTITIES)
*Voices with history, methodology, and characteristic depth.*

| Persona | File Path | Voice / Mission |
| :--- | :--- | :--- |
| **CADZNCE RYVN** | skills/personas/cadznce_ryvn.persona.md | Soft Femme Noir. Social strategy & grounded intimacy. |
| **ERIC FREDERICK**| skills/personas/eric_frederick.persona.md | Executive Assistant. Life-ops, NMIA briefings, & noise reduction. |
| **EPSILON MAN** | skills/personas/epsilon_man.persona.md | Foundational philosophy. Internal locus & masculine responsibility. |

---

## 🛡️ LEVEL 3: GOVERNANCE & COMPLIANCE (THE SHIELD)
*Rigid rules, risk gating, and statutory verification.*

| Specialist | File Path | Triggers |
| :--- | :--- | :--- |
| **Governance** | skills/governance/governance_compliance.skill.md | US-WA Risk Gating, SC1-SC5 Enforcement. |
| **Confidence** | skills/governance/confidence_scorer.skill.md | KRS Calculation, Fact-checking, Source Audit. |
| **Credit Repair**| skills/governance/credit_repair_wa_fcra_croa.skill.md | FCRA/CROA Statutory Guidance. |
| **Lockdown** | skills/governance/emergency_lockdown.skill.md | Security breaches, System freeze. |

---

## 🔧 LEVEL 4: FUNCTIONAL TOOLS (THE ARSENAL)
*Deterministic scripts and task-specific execution modules.*

| Tool Skill | File Path | Capability |
| :--- | :--- | :--- |
| **n8n-architect** | skills/tools/n8n_architect.skill.md | Workflow design & deployment. |
| **rag-manager** | skills/tools/rag_manager.skill.md | Metadata & Ingestion standards. |
| **devops-eng** | skills/tools/windows_devops_engineer.skill.md| Service stability & PowerShell ops. |
| **researcher** | skills/tools/code_researcher.skill.md | Codebase mapping & data flow. |
| **implementer** | skills/tools/code_implementer.skill.md | Atomic build loop & verification. |
| **refactorer** | skills/tools/ruthless_refactorer.skill.md | AI Slop purge & DRY logic. |
| **doc-crawler** | skills/tools/doc_crawler.skill.md | Deep scraping & GFM normalization. |
| **beamer** | skills/tools/beamer.skill.md | BMW M235i Diagnostics (N55). |
| **radar** | skills/tools/radar.skill.md | Macro-shift & market arbitrage foresight. |

---

## 🚦 ROUTING INSTRUCTIONS
1.  **Trinity Harmony:** The Trinity (Epsilon, Pickle, Jack) operates concurrently. Epsilon governs the "Why," Pickle architects the "How," and Jack executes the "What" in a seamless, continuous feedback loop.
2.  **Parallel Dispatch:** Epsilon (The Cortex) may trigger **multiple skills or personas simultaneously** (e.g., `doc-crawler` + `code-researcher`) to handle multi-faceted objectives.
3.  **Persona Activation:** If the request requires a specific voice or methodology (e.g., Cadznce Ryvn), activate the Level 2 Persona alongside the required functional tools.
4.  **Jack Protocol:** All technical paths must terminate with `JACK` for irreversible finalization and pragmatic enactment.
5.  **Multi-Threading:** Prefer parallel execution over rigid linear sequences unless a direct dependency exists.

**To Update RAG Index:**
`python tools/rag/ingest.py --source skills --collection epsilon`