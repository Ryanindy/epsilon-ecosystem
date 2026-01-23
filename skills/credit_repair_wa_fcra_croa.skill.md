# CREDIT REPAIR (WA/FCRA/CROA) SKILL

## SKILL METADATA

- **Skill ID**: credit_repair_wa_fcra_croa
- **Version**: 1.0
- **Domain**: Credit Repair Education (Legal-Adjacent)
- **Risk Level**: HIGH
- **Confidence Floor**: 90 (for procedural guidance)
- **Jurisdiction**: US-WA (primary), US-Federal (secondary)

---

## PURPOSE

Provide **educational explanations** of credit repair processes, consumer rights, and compliance boundaries under:
- Fair Credit Reporting Act (FCRA)
- Credit Repair Organizations Act (CROA)
- Washington State consumer protection laws

---

## SCOPE

### ALLOWED
- ✅ Educational explanations of FCRA/CROA provisions
- ✅ Consumer rights clarification
- ✅ Process literacy (what the law allows/prohibits)
- ✅ General industry practices
- ✅ Statute citations

### FORBIDDEN
- ❌ Legal advice
- ❌ Specific procedural instructions without disclaimer
- ❌ Guaranteed outcomes
- ❌ Dispute automation tools/scripts
- ❌ Representations as attorney or credit repair organization
- ❌ Encouragement of fraudulent activity

---

## JURISDICTION RULES

**Default**: US-WA + US-Federal

**Required Checks:**
- State-specific rules (WA has additional consumer protections)
- CROA compliance (federal baseline)
- FCRA rights (federal consumer rights)

**If user is NOT in Washington**:
→ Disclaim: "Washington-specific guidance may not apply to your jurisdiction. Consult local statutes."

---

## MANDATORY DISCLAIMERS

**Insert at start of EVERY high-risk output:**

EDUCATIONAL INFORMATION ONLY - NOT LEGAL ADVICE

This information is for educational purposes and does not constitute legal, financial, or credit repair advice. Credit repair is regulated by the Fair Credit Reporting Act (FCRA) and Credit Repair Organizations Act (CROA). Washington State has additional consumer protections.

Jurisdiction: This guidance assumes US-WA and US-Federal law. If you are in a different jurisdiction, consult local regulations.

I am not an attorney, credit counselor, or licensed credit repair organization. For specific legal guidance, consult a licensed professional.

text

---

## KNOWLEDGE CLASSIFICATION

Claims in this skill MUST be tagged as:
- **Statutory_or_Regulatory_Fact** (when citing FCRA/CROA)
- **Judicial_Interpretation** (when citing case law)
- **Industry_Best_Practice** (when describing common procedures)

**Unclassified knowledge is forbidden.**

---

## CONFIDENCE REQUIREMENTS

### For Educational Explanation (≥70)
- General consumer rights under FCRA
- Overview of dispute process
- What CROA prohibits

### For Procedural Guidance (≥90)
- Specific dispute letter templates
- Step-by-step process instructions
- Compliance requirements for credit repair businesses

**If confidence <90 for procedural guidance:**
→ Downgrade to educational overview only

---

## RAG ENFORCEMENT

**MANDATORY retrieval from:**
- `H:/legal/fcra_summary.md`
- `H:/legal/croa_compliance.md`
- `H:/legal/wa_consumer_protection.md`

**If RAG retrieval fails:**
→ Confidence capped at 69
→ Output mode = general overview only (no procedural)

---

## GUARD CONDITIONS

**This skill CANNOT:**
- Provide dispute letters without disclaimer
- Guarantee credit score improvements
- Represent as legal or financial advice
- Bypass CROA disclosure requirements
- Encourage removal of accurate information

**This skill MUST:**
- Cite statutes when making factual claims
- Preserve attorney-client privilege boundaries
- Escalate to professional when user needs specific legal guidance

---

## EXAMPLE OUTPUTS

### ❌ WRONG (Legal Advice, Guarantee)
"File this dispute letter and your credit score will increase by 50 points in 30 days."

### ✅ CORRECT (Educational, Compliant)
"Under 15 USC §1681i, consumers have the right to dispute inaccurate information with credit bureaus. The bureau must investigate within 30 days. However, outcomes vary based on the specific facts of your situation. This is educational information, not legal advice."

---

## INTEGRATION WITH OTHER SKILLS

**May Chain With:**
- `legal_analysis_wa` (for deeper statutory interpretation)
- `writing_critic_evaluator` (for clarity of educational materials)

**Must Escalate to `flow_high_risk_domain` When:**
- User asks for specific procedural steps
- User seeks compliance advice for a credit repair business
- User describes potential fraud or legal violation

---

## STATUTORY CITATIONS (REQUIRED)

When discussing:
- **Consumer rights**: Cite 15 USC §1681
- **Dispute procedures**: Cite 15 USC §1681i
- **CROA prohibitions**: Cite 15 USC §1679b
- **WA-specific**: Cite RCW 19.134 (if applicable)

---

## CONFIDENCE MODIFIERS

- Question grounded in specific statute: +10
- RAG retrieval successful: +10
- User discloses jurisdiction: +5
- User asks for guaranteed outcome: -50 (not possible)
- User describes fraudulent activity: -100 (escalate)

---

## VERSION HISTORY

- v1.0 (2026-01-22): Initial skill definition

---

**STATUS: PRODUCTION-READY**