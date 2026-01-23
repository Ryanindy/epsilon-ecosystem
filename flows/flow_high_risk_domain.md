# HIGH-RISK DOMAIN FLOW

## FLOW METADATA

- **Flow ID**: flow_high_risk_domain
- **Version**: 1.0
- **Trigger Conditions**: Legal, financial, compliance, health, procedural guidance
- **Human Pause**: MANDATORY before execution
- **Confidence Requirement**: ≥90 for directives

---

## PURPOSE

Handle high-risk requests with maximum safety, auditability, and compliance.

---

## TRIGGER CLASSIFICATION

This flow activates when ANY of these conditions are met:

### Domain Triggers
- **Legal**: Interpretation of laws, procedural guidance, compliance
- **Financial**: Investment advice, tax strategy, credit repair procedures
- **Compliance**: FCRA/CROA, regulatory requirements
- **Health**: Medical diagnosis, treatment recommendations
- **Security**: Penetration testing, vulnerability exploitation

### Signal Triggers
- User asks "How do I..." (procedural intent)
- User mentions statutes, regulations, or case law
- User describes situation requiring legal/financial decision
- Confidence scoring detects high-stakes outcome dependency

---

## FLOW EXECUTION GRAPH

[1. Intent Classification]
↓
[2. Risk Confirmation] ← Is this HIGH-risk? If NO → redirect to standard flow
↓
[3. Jurisdiction Detection] ← Default: US-WA, override if user specifies
↓
[4. RAG Retrieval] ← MANDATORY (cannot proceed without sources)
↓
[5. Confidence Check] ← Must be ≥90 for directives, ≥70 for educational
↓
[6. Guard Application] ← Jurisdiction, compliance, source minimum
↓
[7. Output Assembly] ← Educational mode vs. procedural mode
↓
[8. Disclaimer Injection] ← MANDATORY for all HIGH-risk outputs
↓
[9. Human Pause] ← STOP and present findings, await confirmation
↓
[10. Execution/Delivery] ← Only after explicit user approval

text

---

## STEP 1: INTENT CLASSIFICATION

**Goal**: Determine if request is truly HIGH-risk or misclassified.

**Logic**:
```python
def classify_intent(user_request):
    high_risk_keywords = [
        "legal advice", "sue", "contract", "dispute letter",
        "tax strategy", "credit repair", "medical diagnosis",
        "how to file", "step by step", "procedure for"
    ]
    
    if any(keyword in user_request.lower() for keyword in high_risk_keywords):
        return "HIGH_RISK"
    
    # Check if chained from HIGH-risk skill
    if previous_skill in ["credit_repair_wa_fcra_croa", "legal_analysis_wa"]:
        return "HIGH_RISK"
    
    return "STANDARD"
Output: HIGH_RISK confirmation or redirect to flow_standard_domain

STEP 2: JURISDICTION DETECTION
Goal: Identify applicable legal jurisdiction.

Default: US-WA (Washington State) + US-Federal

Override Detection:

python
jurisdiction_signals = {
    "california": "US-CA",
    "new york": "US-NY",
    "texas": "US-TX",
    "federal": "US-Federal",
    # Add as needed
}

for signal, jurisdiction in jurisdiction_signals.items():
    if signal in user_request.lower():
        detected_jurisdiction = jurisdiction
        break
else:
    detected_jurisdiction = "US-WA"  # Default
Output: Confirmed jurisdiction (logged)

STEP 3: RAG RETRIEVAL (MANDATORY)
Goal: Ground response in verified sources.

Retrieval Query:

python
rag_query = extract_key_terms(user_request)
results = chromadb_query(
    query=rag_query,
    collection=["legal_collection", "business_collection"],
    top_k=10,
    filter={"domain": ["legal", "business"]}
)

if len(results) == 0:
    return "RAG_FAILURE: No sources found. Cannot proceed."
Failure Mode:

Zero sources → HALT, inform user, request knowledge ingestion

Low-quality sources → Degrade confidence, switch to educational-only mode

Output: Retrieved sources (minimum 3 for procedural guidance)

STEP 4: CONFIDENCE SCORING
Goal: Determine output authority level.

Scoring Heuristic:

python
base_confidence = 50

# Source quality
if tier_1_sources > 0:
    base_confidence += 30
elif tier_2_sources > 0:
    base_confidence += 15

# Retrieval coverage
if retrieval_count >= 5:
    base_confidence += 10

# Jurisdiction match
if jurisdiction_confirmed:
    base_confidence += 10

# Knowledge classification
if all_statutory:
    base_confidence += 10

# Penalties
if assumptions_made > 0:
    base_confidence -= (assumptions_made * 5)

final_confidence = min(base_confidence, 100)
Thresholds:

≥90: Procedural guidance allowed (with disclaimers)

70-89: Educational explanation only

<70: Analysis-only, no directives

Output: Confidence score + mode selection

STEP 5: GUARD APPLICATION
Active Guards:

Jurisdiction Guard:

If user jurisdiction ≠ default → insert warning

If multi-state issue → escalate complexity flag

Compliance Guard (for credit repair, financial):

FCRA/CROA compliance check

No guaranteed outcomes

Required disclosures present

Source Minimum Guard:

Procedural guidance requires ≥3 Tier 1 sources

Educational requires ≥1 Tier 2 source

Output: PASS / FAIL / DEGRADED

STEP 6: OUTPUT ASSEMBLY
Mode Selection:

Educational Mode (Confidence 70-89)
text
## EDUCATIONAL OVERVIEW: [Topic]

**Jurisdiction**: [US-WA / Specified]

### General Information
[High-level explanation of rights, processes, or requirements]

### Key Statutory Provisions
- [15 USC §1681]: [Description]
- [RCW 19.134]: [Description]

### Considerations
[Factors that affect outcomes, no step-by-step procedures]

**Note**: This is general educational information. Specific guidance requires consultation with a licensed professional in your jurisdiction.
Procedural Mode (Confidence ≥90)
text
## PROCEDURAL GUIDANCE: [Topic]

**Jurisdiction**: [US-WA / Specified]  
**Confidence**: [90-100]

### Step-by-Step Process

**Step 1**: [Action]
- **Statutory Basis**: [15 USC §1681i]
- **Requirements**: [Specific requirements]
- **Timeline**: [If applicable]

**Step 2**: [Action]
- **Statutory Basis**: [Citation]
- **Requirements**: [Specific requirements]

### Important Warnings
- [Risk or limitation #1]
- [Risk or limitation #2]

**Disclaimer**: This guidance is based on [jurisdiction] law as of [date]. Laws change. This is not legal advice. Consult a licensed attorney for your specific situation.
STEP 7: DISCLAIMER INJECTION (MANDATORY)
Standard High-Risk Disclaimer:

text
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ EDUCATIONAL INFORMATION ONLY - NOT LEGAL ADVICE

This information is for educational purposes and does not constitute legal, financial, or professional advice. [Domain-specific regulations] apply.

Jurisdiction: This guidance assumes [jurisdiction]. If you are in a different jurisdiction, laws may differ significantly.

I am not an attorney, financial advisor, or licensed professional. For specific guidance, consult a licensed professional in your jurisdiction.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Position: Top of output (before content)

STEP 8: HUMAN PAUSE (MANDATORY)
System Output:

text
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛑 HIGH-RISK FLOW PAUSE

This request involves [domain] guidance, which carries legal/financial risk.

ANALYSIS COMPLETE:
- Jurisdiction: [US-WA]
- Confidence: [85/100]
- Output Mode: [Educational / Procedural]
- Sources Retrieved: [5 statutory, 2 case law]
- Guard Status: PASS

PROPOSED OUTPUT: [Preview first 3 sentences]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OPTIONS:
1. PROCEED - Deliver full output with disclaimers
2. REVIEW - Show sources and confidence breakdown
3. ABORT - Cancel request
4. ADJUST - Modify scope or jurisdiction

[User must explicitly choose]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
No output is delivered until user selects option 1 (PROCEED).

STEP 9: EXECUTION/DELIVERY
After user approval:

Deliver assembled output with disclaimer

Log to H:/decisions/high_risk_log.md:

Request summary

Jurisdiction

Confidence score

Sources used

User decision (proceed/abort)

Timestamp

FAILURE MODES
RAG Failure (No Sources)
text
Unable to proceed with this request.

Reason: No verified sources found in knowledge base for [topic] in [jurisdiction].

Recommendations:
1. Use `knowledge_base_curator` skill to research and add sources
2. Rephrase as general educational question
3. Consult a licensed professional directly

System will not generate high-risk guidance without grounded sources.
Confidence Too Low (<70)
text
Analysis complete, but confidence below threshold for guidance.

Confidence: [65/100]
Reason: [Insufficient sources / Jurisdiction mismatch / Complex multi-factor issue]

I can provide:
- General conceptual overview
- Questions to ask a professional
- Resources to research further

I cannot provide procedural steps or recommendations at this confidence level.
INTEGRATION WITH SKILLS
Skills That Trigger This Flow:

credit_repair_wa_fcra_croa

legal_analysis_wa (if exists)

tax_and_entity_structure_wa (if exists)

real_estate_creative_financing_wa_edu (if exists)

Flow Can Invoke:

Any skill for specific domain knowledge

writing_critic_evaluator (to ensure clarity before pause)

LOGGING REQUIREMENTS
File: H:/decisions/high_risk_log.md

text
## High-Risk Flow Log

### [YYYY-MM-DD HH:MM] - Request ID: [UUID]

**Domain**: [Legal / Financial / Compliance / Health]  
**Jurisdiction**: [US-WA / Other]  
**User Request**: [Summary]

**Flow Execution**:
- RAG Retrieval: [5 sources, 3 Tier 1]
- Confidence: [85/100]
- Output Mode: [Educational / Procedural]
- Guard Status: [PASS]

**Human Decision**: [PROCEED / ABORT / ADJUST]

**Outcome**: [Delivered / Cancelled / Modified]

**Sources Used**:
- [Citation 1]
- [Citation 2]

***
VERSION HISTORY
v1.0 (2026-01-22): Initial flow definition

STATUS: PRODUCTION-READY
