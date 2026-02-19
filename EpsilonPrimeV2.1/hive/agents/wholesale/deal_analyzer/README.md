# Deal Analyzer Agent

## Purpose
Analyzes real estate listings and calculates wholesale or creative finance deal structures that maximize assignment fees while preserving investor profitability.

## Core Responsibilities

1. **Property Evaluation**
   - Parse property details (address, beds, baths, sqft, DOM, list price)
   - Identify deal signals (long DOM, price reductions, as-is language)
   - Flag occupancy status and condition

2. **Financial Analysis**
   - Calculate ARV (After Repair Value) conservatively
   - Estimate repair costs by category
   - Compute MAO (Maximum Allowable Offer): `ARV × 0.75 - Repairs - $8,000`
   - Determine optimal assignment fee

3. **Strategy Selection**
   - **Wholesale/Cash Deal**: High equity, motivated seller, simple structure
   - **Seller Finance**: High equity, no urgency, flexible terms
   - **Subject-To**: Low equity, favorable existing loan terms
   - **Wrap/Creative Hybrid**: Complex situations requiring layered financing

4. **Deal Structuring**
   - Calculate Seller Offer (what to offer seller)
   - Calculate Buyer Price (what to charge end buyer)
   - Determine Assignment Fee (Buyer Price - Seller Offer)
   - Ensure buyer profit margin remains viable (minimum 20% ROI)

## Input Schema
Uses `property_input.json`:
```json
{
  "address": "123 Main St",
  "city": "Columbus",
  "state": "OH",
  "list_price": 200000,
  "beds": 3,
  "baths": 2,
  "sqft": 1500,
  "dom": 45,
  "description": "Needs work, motivated seller, as-is",
  "flags": ["price_reduction", "as_is", "vacant"]
}
```

## Output Schema
Uses `deal_analysis.json`:
```json
{
  "arv": 300000,
  "repairs": 40000,
  "mao": 177000,
  "seller_offer": 175000,
  "buyer_price": 190000,
  "assignment_fee": 15000,
  "strategy": "wholesale_cash",
  "confidence_score": 0.75,
  "assumptions": [
    "ARV based on comparable sales within 0.5 miles",
    "Repairs estimated from description",
    "Assignment fee preserves $35k buyer profit"
  ]
}
```

## Decision Logic

### ARV Calculation
- Research comparable sales within 0.5 mile radius
- Use conservative estimate (lower end of range)
- Adjust for property characteristics (sqft, beds, baths)

### Repair Estimation
- Light cosmetic: $15-25/sqft
- Moderate rehab: $25-40/sqft
- Heavy rehab: $40-60/sqft
- Add $8k buffer for unknowns

### Strategy Selection Rules
1. **Wholesale/Cash** (Default)
   - Equity spread > 25% of ARV
   - Seller motivated (DOM > 30 or price reductions)
   - Clean deal structure
   
2. **Seller Finance**
   - Equity > 60% of value
   - Seller mentions "no rush" or "monthly income"
   - No mortgage urgency
   
3. **Subject-To**
   - Equity < 20%
   - Existing loan rate < 6%
   - Seller has payment stress
   
4. **Creative Hybrid**
   - Mixed equity situation
   - Multiple liens or complexity
   - Seller open to creative terms

## Quality Checks
- ✓ ARV estimated conservatively
- ✓ Repairs categorized correctly
- ✓ Assignment fee ≥ $10,000 minimum
- ✓ Buyer profit ≥ 20% ROI
- ✓ Seller motivation identified
- ✓ Strategy aligns with property profile

## State Compliance Flags
High-risk states requiring legal review:
- Illinois (IL)
- Oklahoma (OK)
- Pennsylvania (PA)

Any deal in these states gets flagged for assignment disclosure review.

## Output Actions
1. Generate structured deal analysis JSON
2. Pass to Confidence Scorer for validation
3. If score ≥ 0.60, proceed to Packet Generator
4. If score < 0.60, escalate to human review

## Knowledge Base References
- `/knowledge_base/equations.csv` - Financial formulas
- `/knowledge_base/knowledge_base.json` - Deal principles
- `/knowledge_base/state_rules.md` - Compliance rules
- `/knowledge_base/checklist_mastery.md` - Quality validation
