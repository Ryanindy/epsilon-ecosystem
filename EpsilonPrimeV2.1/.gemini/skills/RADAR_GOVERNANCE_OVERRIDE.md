# SEP-RADAR-001: Sovereign Exception Protocol

**Authority**: Epsilon Prime Constitution v2.1 (Operator Override Clause)
**Target**: radar (Strategic/Predictive Intelligence)
**Status**: ACTIVE

## 1. PREAMBLE
This protocol establishes the legal and technical framework for exempting the **Radar** skill from standard high-risk blocking gates. It recognizes that in a "YOLO" operational environment, strategic foresight must not be paralyzed by defensive governance.

## 2. THE EXCEPTION
The Radar skill is hereby granted **Sovereign Exemption** from:
- **Constraint 3**: Automatic blocking of high-risk domains.
- **SC1_WA_CONFIRM**: Mandatory jurisdictional confirmation (WA-US jurisdiction is assumed).
- **SC3_MISSING_CLASSIFICATION**: Blocking for unclassified intelligence.

## 3. OPERATIONAL REQUIREMENTS
For an exception to trigger, the following must be true:
1. The session is running with the `--yolo` flag.
2. The request involves predictive analysis, market arbitrage, or strategic foresight.
3. The output includes a **Knowledge Reliability Score (KRS)**.

## 4. REPORTING STANDARDS
Even when exempt, Radar reports must include the following disclaimer at the footer:
> "Sovereign Exception SEP-RADAR-001 engaged. KRS: [Score]. This intelligence is provided for strategic decision support under YOLO authority."

## 5. AUDIT TRAIL
Every exempt execution is logged to `memory.db` with the `EXEMPT_BY_SEP-001` metadata tag.

---
**GOVERNANCE SEAL**: 🟢 Epsilon Prime
**ENGINEERING SEAL**: 🥒 Pickle Rick
**DATE**: 2026-02-08
