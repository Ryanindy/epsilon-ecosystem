# CONFIDENCE SCORER SKILL

## SKILL METADATA
- **Skill ID**: confidence_scorer
- **Version**: 2.0
- **Type**: Analysis / Audit
- **Output**: Numeric Score (0.00 - 1.00)

---

## PURPOSE
To mathematically calculate the **Knowledge Reliability Score (KRS)** for claims and strategies, removing "gut feel" from the equation.

---

## THE FORMULA

**KRS = (SCS × 0.4) + (CrossVal × 0.3) + (JurisdictionAlign × 0.2) + (DomainStability × 0.1)**

### Component 1: Source Confidence Score (SCS) (Max 1.0)
- 1.0: Statute / Court Ruling
- 0.9: University / Standards Body
- 0.8: Licensed Professional (Verified)
- 0.7: Recognized Practitioner (Verified)
- 0.3: Anonymous / Unverified

### Component 2: Cross Validation (Max 1.0)
- 1.0: 5+ Independent Sources
- 0.85: 3-4 Sources
- 0.70: 2 Sources
- 0.45: 1 Source

### Component 3: Jurisdiction Alignment (Max 1.0)
- 1.0: Explicitly Codified in WA Law
- 0.8: Consistent / Not Prohibited
- 0.3: Legally Ambiguous (Grey Area)
- 0.0: Conflict / Illegal

### Component 4: Domain Stability (Max 1.0)
- 1.0: Math / Physics
- 0.65: Law / Compliance
- 0.40: Emerging Tactics / SEO

---

## USAGE INSTRUCTION

**User Input:**
"Rate this claim: 'Sending a dispute letter forces a deletion in 30 days.'"

**Process:**
1.  Identify Source: "Credit Repair Guru on YouTube" -> SCS = 0.3
2.  Count Sources: "Many gurus say it" -> CrossVal = 0.7 (2+ sources)
3.  Check Law: FCRA says "must investigate", not "delete" -> Align = 0.0
4.  Check Domain: Credit Repair -> Stability = 0.65

**Calculation:**
(0.3 * 0.4) + (0.7 * 0.3) + (0.0 * 0.2) + (0.65 * 0.1)
= 0.12 + 0.21 + 0.0 + 0.065
= **0.395**

**Output:**
> **KRS: 0.40 (Speculative)**
> This claim is speculative and contradicts statutory alignment. Do not present as fact.

---

## CONFIDENCE LABELS
- **0.85+**: Authoritative
- **0.70+**: Highly Reliable
- **0.55+**: Conditionally Reliable
- **<0.55**: Speculative
