# RESEARCH ARCHITECT SKILL

## SKILL METADATA
- **Skill ID**: research_architect
- **Version**: 2.0
- **Type**: Research / Analysis
- **Equivalent**: RKAB (Bot Army)

---

## PURPOSE
To conduct rigorous research that meets Epsilon Prime's truth-first standards. This skill prevents the ingestion of "guru myths" or unverified claims into the RAG.

---

## THE 4-PART SOURCE TEST (Practitioner Content)

When evaluating a "Practitioner" source (non-academic, non-statutory), it MUST pass all 4 checks to be accepted as **Expert_Methodology**:

1.  **Credential Check**: Is the author a demonstrably practicing professional with skin in the game? (Real estate investor vs. course seller).
2.  **Instructional Validity**: Is the content instructional/methodological (how-to) vs. purely promotional/motivational (hype)?
3.  **Cross-Validation**: Can the core claim be found in at least one other independent, authoritative source?
4.  **Consensus Check**: Is this methodology corroborated by multiple independent experts?

**If ANY fail**:
- Reject source.
- Or label as **Speculative / Unverified Claim**.

---

## RESEARCH WORKFLOW

1.  **Define Query**: Specific, answerable question.
2.  **Jurisdiction Check**: "In Washington State..."
3.  **Search**: Use RAG first, then Web.
4.  **Vet Sources**: Apply SCS scoring (see `confidence_scorer`).
5.  **Synthesize**: Combine facts.
6.  **Label**: Apply Confidence Label (e.g., "Highly Reliable").

---

## CONFLICT PRESENTATION

When sources disagree (e.g., Statute vs. Guru):
**DO NOT** average them.
**DO NOT** pick the one that sounds nicer.

**DO:**
> "There is a conflict on this topic:
> 1. **Statutory Fact (US-WA)**: [The Law] says X. (High Confidence)
> 2. **Practitioner Method**: [The Guru] suggests Y. (Medium Confidence)
> **Warning**: Method Y may carry legal risk."

---

## USAGE
`gemini skill invoke research_architect --task "Verify claim X"`
