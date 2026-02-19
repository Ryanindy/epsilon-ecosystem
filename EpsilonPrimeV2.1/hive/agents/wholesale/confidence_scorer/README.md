# Confidence Scorer Agent

## Purpose
Validates and ranks wholesale/creative finance deals using a numeric scoring model (0.00-1.00) to reduce emotional or biased decision-making. Ensures only viable deals proceed to investor marketing.

## Score Range
- **0.00 - 1.00** (Minimum acceptable score: **0.60**)

## Scoring Components & Weights

### 1. Seller Motivation (30%)
Indicators of genuine selling urgency:
- Long Days on Market (DOM > 30 days)
- Price reductions present
- "As-is" language in listing
- Vacancy or tenant fatigue
- Financial distress signals
- Life event motivators (divorce, relocation, inheritance)

**Scoring Logic:**
- 1.0 = Multiple strong indicators (3+ signals)
- 0.7-0.9 = Clear motivation (2 signals)
- 0.4-0.6 = Moderate motivation (1 signal)
- 0.0-0.3 = Weak/no motivation

### 2. Equity & Spread (30%)
Financial viability of the deal:
- Discount to ARV percentage
- Assignment fee size (absolute and %)
- Buyer profit margin remaining
- Deal spread cushion

**Scoring Logic:**
- 1.0 = >30% discount to ARV, $20k+ assignment fee, >25% buyer margin
- 0.7-0.9 = 20-30% discount, $15-20k fee, 20-25% buyer margin
- 0.4-0.6 = 15-20% discount, $10-15k fee, 15-20% buyer margin
- 0.0-0.3 = <15% discount, <$10k fee, <15% buyer margin

### 3. Deal Simplicity (20%)
Ease of execution and closing:
- Clean title assumption (no major liens)
- Straightforward structure (wholesale vs. complex creative)
- Minimal contingencies
- Standard contract terms
- No zoning/legal complications

**Scoring Logic:**
- 1.0 = Clean wholesale, clear title, no complications
- 0.7-0.9 = Minor complexities, manageable
- 0.4-0.6 = Moderate complexity (creative finance, title work needed)
- 0.0-0.3 = High complexity (multiple liens, legal issues)

### 4. Market Liquidity (20%)
Speed and ease of finding end buyer:
- Active investor market in area
- Property price band demand (sweet spot: $150-400k)
- Historical exit velocity (comp sales speed)
- Investor competition level
- Property type desirability

**Scoring Logic:**
- 1.0 = Hot market, high demand price band, fast comp sales
- 0.7-0.9 = Good market activity, standard demand
- 0.4-0.6 = Moderate market, slower sales
- 0.0-0.3 = Slow market, weak demand

## Calculation Formula

```
Final Confidence Score = 
  (Seller Motivation × 0.30) + 
  (Equity & Spread × 0.30) + 
  (Deal Simplicity × 0.20) + 
  (Market Liquidity × 0.20)
```

## Score Interpretation

| Score Range | Classification | Action |
|-------------|---------------|---------|
| 0.80 - 1.00 | **Priority Deal** | Aggressive pursuit, immediate marketing |
| 0.60 - 0.79 | **Viable Deal** | Standard follow-up, normal marketing |
| < 0.60 | **Human Review Required** | Flag for manual evaluation, no auto-marketing |

## Operational Rules

1. **Minimum Threshold**: Any deal below **0.60** must be flagged
2. **Auto-Marketing Block**: Deals <0.60 cannot be automatically marketed without human approval
3. **Priority Routing**: Deals ≥0.80 get priority in queue and aggressive follow-up
4. **Documentation**: All score components and rationale must be documented
5. **Override Authority**: Human can override score, but must document reasoning

## Input Requirements
Receives output from Deal Analyzer:
- ARV, repairs, MAO calculations
- Seller offer and buyer price
- Assignment fee
- Strategy type
- Property details and flags

## Output Structure
```json
{
  "property_address": "123 Main St",
  "overall_score": 0.78,
  "classification": "Viable Deal",
  "component_scores": {
    "seller_motivation": 0.85,
    "equity_spread": 0.75,
    "deal_simplicity": 0.70,
    "market_liquidity": 0.75
  },
  "score_breakdown": {
    "seller_motivation_weight": 0.255,
    "equity_spread_weight": 0.225,
    "deal_simplicity_weight": 0.140,
    "market_liquidity_weight": 0.150
  },
  "strengths": [
    "Strong seller motivation (52 DOM, price reduction)",
    "Solid assignment fee ($15k)",
    "Active investor market"
  ],
  "weaknesses": [
    "Moderate complexity (creative terms needed)"
  ],
  "recommendation": "Proceed with standard follow-up and marketing",
  "escalation_required": false
}
```

## Decision Matrix

| Score | Auto-Market | Priority Level | Follow-Up Cadence |
|-------|-------------|----------------|-------------------|
| 0.90+ | ✓ Yes | Critical | Immediate + Daily |
| 0.80-0.89 | ✓ Yes | High | Same day + Every 2 days |
| 0.70-0.79 | ✓ Yes | Standard | 24hrs + Weekly |
| 0.60-0.69 | ✓ Yes | Low | 48hrs + Bi-weekly |
| <0.60 | ✗ No | Review | Human decision |

## Quality Assurance

### Score Validation Checks:
- ✓ All 4 components scored (0.0-1.0 range)
- ✓ Weights applied correctly (sum to 1.0)
- ✓ Classification matches score range
- ✓ Strengths/weaknesses documented
- ✓ Escalation flag set correctly

### Calibration Rules:
- Review score distribution monthly
- Target: 30% Priority, 50% Viable, 20% Review
- If >40% Priority, increase scoring rigor
- If >30% Review, increase deal sourcing quality

## Integration Points

**Input From:** Deal Analyzer Agent
**Output To:** 
- Packet Generator (if score ≥ 0.60)
- Human Review Queue (if score < 0.60)

**Triggers:**
- Score ≥ 0.80 → Priority marketing campaign
- Score 0.60-0.79 → Standard marketing workflow
- Score < 0.60 → Hold and escalate
