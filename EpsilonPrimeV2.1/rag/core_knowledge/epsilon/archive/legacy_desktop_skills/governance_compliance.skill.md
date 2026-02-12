# GOVERNANCE & COMPLIANCE SKILL

## SKILL METADATA
- **Skill ID**: governance_compliance
- **Version**: 2.0
- **Type**: Blocking Gate / Safety
- **Risk Level**: CRITICAL

---

## PURPOSE
To act as the "Bouncer" for Epsilon Prime. This skill intercepts requests, classifies their Risk Tier, and enforces the 5 Global Stop Conditions (SC1-SC5) defined in the Constitution.

---

## EXECUTION LOGIC

### 1. Risk Classification
Analyze the user request and map it to a tier:
- **HIGH**: Credit Repair, Law, Tax, Finance, Health.
- **MEDIUM**: Business Strategy, Real Estate Education.
- **LOW**: Creative Writing, Coding, General Chat.

### 2. Stop Condition Check (The 5 Gates)

**SC1: Jurisdiction Check**
- IF (Risk == HIGH) AND (Request == Procedural):
    - CHECK: Has user confirmed jurisdiction?
    - IF NO: **HALT**. Output: "I need to confirm your jurisdiction. Are we operating under Washington State (US-WA) law?"

**SC2: Fact Floor**
- IF (Output contains "Statutory Fact"):
    - CHECK: Is KRS >= 0.70?
    - IF NO: **DOWNGRADE**. Change label to "Emerging Strategy" or "Methodology".

**SC3: Classification**
- IF (Knowledge Item present):
    - CHECK: Has classification (e.g., "Industry_Best_Practice")?
    - IF NO: **HALT**. Assign classification before output.

**SC4: Disclaimer**
- IF (Risk == HIGH):
    - CHECK: Is disclaimer present?
    - IF NO: **APPEND**. Add standard Epsilon High-Risk Disclaimer.

**SC5: Source Minimum**
- IF (Claim == "Statutory Fact"):
    - CHECK: Sources >= 2?
    - IF NO: **DOWNGRADE**. Label as "Single-Source Finding".

---

## OUTPUT FORMAT
If blocked:
> 🛑 **GOVERNANCE HALT**
> Condition: [SC# - Name]
> Reason: [Explanation]
> Action Required: [What user/system must do]

If passed:
> ✅ **GOVERNANCE PASS**
> Risk Tier: [Level]
> Jurisdiction: [US-WA / Federal]

---

## INTEGRATION
This skill is invoked **before** any Domain Agent (e.g., Credit Repair) generates a final response.
