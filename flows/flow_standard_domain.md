# STANDARD DOMAIN FLOW

## FLOW METADATA

- **Flow ID**: flow_standard_domain
- **Version**: 1.0
- **Trigger Conditions**: Low-to-medium risk informational requests
- **Human Pause**: Not required (unless confidence <70)
- **Confidence Requirement**: ≥70 for directives

---

## PURPOSE

Handle general informational requests efficiently while maintaining epistemic integrity.

---

## TRIGGER CLASSIFICATION

This flow activates for:

### Low-Risk Domains
- Creative writing
- Content strategy
- Business education (non-legal)
- Technical tutorials (non-security)
- General philosophy/metaphysics

### Medium-Risk Domains
- Business automation (non-financial)
- Marketing strategies
- Technical implementations (non-destructive)
- Educational content creation

---

## FLOW EXECUTION GRAPH

[1. Intent Classification]
↓
[2. Skill Selection] ← Identify relevant skills
↓
[3. RAG Retrieval] ← OPTIONAL but recommended
↓
[4. Inline Skill Chaining] ← Chain skills if needed
↓
[5. Confidence Check] ← ≥70 for directives
↓
[6. Guard Application] ← Light guards (no jurisdiction)
↓
[7. Output Assembly] ← Direct response
↓
[8. Delivery] ← No pause required

text

---

## STEP 1: INTENT CLASSIFICATION

**Goal**: Route to appropriate skills.

**Classification Logic**:
```python
def classify_standard_intent(user_request):
    intent_map = {
        "epsilon philosophy": "epsilon_man_core",
        "executive challenge": "eric_executive_assistant",
        "writing feedback": "writing_critic_evaluator",
        "automation strategy": "ai_automation_strategist_smb",
        "metaphysics": "metaphysics_analysis",
        "content creation": ["creative_writing", "viral_content_strategist"]
    }
    
    for signal, skill in intent_map.items():
        if signal in user_request.lower():
            return skill
    
    return "general_reasoning"  # Default
Output: Primary skill(s) to invoke

STEP 2: SKILL SELECTION & CHAINING
Single Skill Invocation:

python
if single_skill_sufficient:
    result = invoke_skill(primary_skill, user_request)
    return result
Multi-Skill Chain:

python
# Example: Epsilon philosophy → Executive challenge → Writing critique
result_1 = invoke_skill("epsilon_man_core", user_request)
result_2 = invoke_skill("eric_executive_assistant", result_1)
result_3 = invoke_skill("writing_critic_evaluator", result_2)

return result_3  # Final output
Chain Escalation Rule:
If ANY skill in chain is HIGH-risk → escalate entire chain to flow_high_risk_domain

STEP 3: RAG RETRIEVAL (OPTIONAL)
When to Use RAG:

User asks about Epsilon doctrine → retrieve from H:/epsilon/

User asks about business frameworks → retrieve from H:/business/

User asks for factual claims → retrieve evidence

When to Skip RAG:

Creative writing requests (no factual grounding needed)

Reflection/challenge mode (persona-driven, not knowledge-driven)

Brainstorming (generative, not retrieval)

Retrieval Logic:

python
if requires_factual_grounding(user_request):
    rag_results = chromadb_query(
        query=user_request,
        collection=["epsilon_collection", "business_collection"],
        top_k=5
    )
    
    if len(rag_results) > 0:
        confidence_boost = +10
    else:
        confidence_penalty = -10
Output: Retrieved sources (if applicable) + confidence modifier

STEP 4: CONFIDENCE CHECK
Threshold:

≥70: Full response with directives allowed

55-69: Analysis-only, no action recommendations

<55: Insufficient confidence, request clarification or RAG expansion

Scoring (simplified for standard flow):

python
base_confidence = 70  # Standard starts higher than HIGH-risk

if rag_retrieval_successful:
    base_confidence += 10

if user_provides_clear_context:
    base_confidence += 10

if request_is_creative_not_factual:
    base_confidence += 10  # Less precision required

final_confidence = min(base_confidence, 100)
STEP 5: GUARD APPLICATION (LIGHT)
Active Guards (subset of full guards):

Confidence Guard:

Block directives if confidence <70

Downgrade to analysis-only

Brand Isolation Guard:

Ensure Epsilon and K&F content don't mix

Flag if request crosses brands

Dependency Guard:

If Eric Assistant is invoked, ensure challenge mode active (no comfort-only)

Output: PASS / DEGRADE

STEP 6: OUTPUT ASSEMBLY
Standard Output Format:

text
## [Response Title]

[Direct answer to user's question - 1-3 sentences]

### [Section 1 Heading]
[Content - 2-3 sentences]

### [Section 2 Heading]
[Content - 2-3 sentences]

### [Section 3 Heading] (if needed)
[Content - 2-3 sentences]

***

**Confidence**: [70-100] (if user requests via SHOW_CONFIDENCE)
**Sources**: [If RAG used]
Tone:

Direct, not performative

Clear, not academic

Helpful, not pandering

STEP 7: DELIVERY (NO PAUSE)
Standard flow delivers immediately (no human confirmation required).

Exception: If confidence drops below 70 during execution, auto-pause and present:

text
Confidence dropped below threshold during analysis.

Current confidence: [65/100]
Reason: [Insufficient context / Conflicting sources / Assumption required]

OPTIONS:
1. PROCEED with analysis-only (no recommendations)
2. CLARIFY request for higher confidence
3. ABORT

[User choice required]
EXAMPLE EXECUTION
User Request:
"Explain the Epsilon concept of internal locus of control and how it applies to business decisions."

Flow Execution:
Step 1: Intent Classification
→ Primary skill: epsilon_man_core
→ Secondary skill: eric_executive_assistant (optional for challenge)

Step 2: RAG Retrieval
→ Query: "internal locus of control Epsilon"
→ Results: 5 sources from H:/epsilon/
→ Confidence boost: +10

Step 3: Skill Invocation
→ epsilon_man_core generates philosophical explanation
→ Confidence: 85/100

Step 4: Guard Check
→ Confidence: PASS (≥70)
→ Brand: PASS (Epsilon-only)

Step 5: Output Assembly

text
## Internal Locus of Control in Business Decisions

Internal locus of control means you view yourself as the primary variable in your outcomes. In business, this translates to focusing on what you control—your decisions, systems, and actions—rather than externalizing blame to market conditions, competitors, or circumstances.

### Application in Decision-Making

When facing a business decision, ask: "What can I control here?" Not what you wish you could control, but what you actually can. This might be your outreach strategy, your pricing model, or how you allocate time—not whether clients respond or whether the economy cooperates.

### Common Traps

Entrepreneurs often externalize: "Clients won't pay for this" or "The market's too competitive." These framings remove your agency. Reframe: "What pricing model makes this viable?" or "What specific niche removes me from direct competition?" The outcome may still be challenging, but the locus of control remains with you.

### Epsilon Principle

The smallest truthful action (epsilon) you can take is to identify one thing within your control and act on it. Not the biggest thing, not the perfect thing—the truthful thing you can actually do.

***

**Confidence**: 85/100  
**Source**: H:/epsilon/locus_of_control.md
Step 6: Delivery
→ Output delivered immediately (no pause required)

INTEGRATION WITH SKILLS
Skills Commonly Used:

epsilon_man_core

eric_executive_assistant

ai_automation_strategist_smb

writing_critic_evaluator

metaphysics_analysis

Flow Can Chain To:

flow_high_risk_domain (if HIGH-risk detected mid-execution)

flow_content_production (if request is about creating long-form content)

LOGGING REQUIREMENTS
Logging is OPTIONAL for standard flow (to reduce overhead).

Log only if:

Confidence drops below 70

User invokes RUN_AUDIT

Error occurs during execution

File: H:/decisions/standard_flow_log.md

text
## Standard Flow Log

### [YYYY-MM-DD HH:MM] - Request ID: [UUID]

**Intent**: [Classified intent]  
**Skills Invoked**: [List]  
**RAG Used**: Yes / No  
**Confidence**: [Score]  
**Outcome**: [Success / Degraded / Error]

**Notes**: [Any issues]

***
VERSION HISTORY
v1.0 (2026-01-22): Initial flow definition

STATUS: PRODUCTION-READY