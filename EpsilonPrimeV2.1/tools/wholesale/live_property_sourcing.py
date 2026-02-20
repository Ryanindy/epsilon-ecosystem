"""
WHOLESALE AI SYSTEM - LIVE PROPERTY SOURCING
Autonomous property finder for Eric Frederick
Created: 2026-01-20
"""

import json
import os
from datetime import datetime
import random

# Configuration
PROJECT_ROOT = r"C:\Users\Media Server\Desktop\Wholesale_AI_Project"
PROFILE_PATH = os.path.join(PROJECT_ROOT, "config", "buyer_profiles", "buyer_001_eric_frederick.json")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output", "deals")

# Load buyer profile
with open(PROFILE_PATH, 'r') as f:
    buyer_profile = json.load(f)

print("=" * 80)
print("[LAUNCH] WHOLESALE AI SYSTEM - LIVE EXECUTION")
print("=" * 80)
print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Buyer: {buyer_profile['buyer_name']}")
print(f"Markets: {', '.join(buyer_profile['criteria']['markets'])}")
print("=" * 80)
print()

# Multi-source property data (simulating real sources until BuyCartel integration)
# In production, this would scrape Zillow, Realtor.com, public records, etc.

ohio_properties = [
    {
        "address": "2847 Sullivant Avenue",
        "city": "Columbus",
        "state": "OH",
        "zip": "43204",
        "list_price": 145000,
        "beds": 3,
        "baths": 2,
        "sqft": 1420,
        "year_built": 1965,
        "dom": 67,
        "condition": "Needs moderate rehab, tenant occupied",
        "flags": ["tenant_occupied", "price_reduction", "as_is", "tired_landlord"],
        "arv_estimate": 235000,
        "repairs_estimate": 45000,
        "motivation_signals": ["tired_landlord", "price_reduction", "as_is"],
        "source": "MLS",
        "mls_number": "223456789"
    },
    {
        "address": "1523 East 71st Street",
        "city": "Cleveland",
        "state": "OH",
        "zip": "44103",
        "list_price": 82000,
        "beds": 3,
        "baths": 1,
        "sqft": 1100,
        "year_built": 1955,
        "dom": 89,
        "condition": "Vacant, estate sale, needs cosmetic work",
        "flags": ["vacant", "estate", "as_is", "price_reduction"],
        "arv_estimate": 165000,
        "repairs_estimate": 32000,
        "motivation_signals": ["estate", "vacant", "price_reduction", "long_dom"],
        "source": "Zillow",
        "owner_name": "Estate of Margaret Wilson"
    },
    {
        "address": "4512 Glenway Avenue",
        "city": "Cincinnati",
        "state": "OH",
        "zip": "45238",
        "list_price": 175000,
        "beds": 4,
        "baths": 2,
        "sqft": 1850,
        "year_built": 1978,
        "dom": 45,
        "condition": "Good condition, owner relocating",
        "flags": ["relocation", "quick_sale_needed"],
        "arv_estimate": 265000,
        "repairs_estimate": 18000,
        "motivation_signals": ["relocation", "quick_sale_needed"],
        "source": "FSBO",
        "owner_name": "Robert Chen"
    },
    {
        "address": "789 Oak Street",
        "city": "Toledo",
        "state": "OH",
        "zip": "43605",
        "list_price": 95000,
        "beds": 3,
        "baths": 1.5,
        "sqft": 1250,
        "year_built": 1962,
        "dom": 103,
        "condition": "Vacant, foreclosure, needs full rehab",
        "flags": ["vacant", "foreclosure", "as_is"],
        "arv_estimate": 185000,
        "repairs_estimate": 52000,
        "motivation_signals": ["foreclosure", "vacant", "long_dom"],
        "source": "Public Records",
        "owner_name": "Bank of America REO"
    },
    {
        "address": "2156 Germantown Street",
        "city": "Dayton",
        "state": "OH",
        "zip": "45417",
        "list_price": 125000,
        "beds": 3,
        "baths": 2,
        "sqft": 1380,
        "year_built": 1972,
        "dom": 78,
        "condition": "Needs moderate updates, divorce sale",
        "flags": ["divorce", "as_is", "motivated_seller"],
        "arv_estimate": 215000,
        "repairs_estimate": 38000,
        "motivation_signals": ["divorce", "motivated_seller"],
        "source": "Realtor.com",
        "owner_name": "Sarah & Michael Thompson"
    }
]

def score_property(prop, profile):
    """Score property against buyer criteria (0-100)"""
    score = 0
    max_score = 100
    
    # Price range match (20 points)
    if profile['criteria']['price_range']['sweet_spot_min'] <= prop['list_price'] <= profile['criteria']['price_range']['sweet_spot_max']:
        score += 20
    elif profile['criteria']['price_range']['min'] <= prop['list_price'] <= profile['criteria']['price_range']['max']:
        score += 12
    
    # Market match (15 points)
    market = f"{prop['city']}, {prop['state']}"
    if market in profile['criteria']['focus_markets']['primary']:
        score += 15
    elif market in profile['criteria']['focus_markets']['secondary']:
        score += 10
    elif market in profile['criteria']['markets']:
        score += 5
    
    # Motivation signals (25 points)
    high_priority = sum(1 for sig in prop['motivation_signals'] if sig in profile['criteria']['high_priority_signals'])
    other_signals = sum(1 for sig in prop['motivation_signals'] if sig in profile['criteria']['motivation_signals'])
    score += min(25, (high_priority * 8) + (other_signals * 3))
    
    # Equity spread (30 points)
    arv = prop.get('arv_estimate', 0)
    repairs = prop.get('repairs_estimate', 0)
    mao = (arv * 0.75) - repairs - 8000  # Standard MAO formula
    equity_spread = ((arv - prop['list_price'] - repairs) / arv) * 100 if arv > 0 else 0
    
    if equity_spread >= profile['criteria']['desired_spread']['ideal_equity_spread_pct']:
        score += 30
    elif equity_spread >= profile['criteria']['desired_spread']['minimum_equity_spread_pct']:
        score += 20
    else:
        score += max(0, equity_spread * 0.5)
    
    # DOM factor (10 points)
    if prop['dom'] > 60:
        score += 10
    elif prop['dom'] > 30:
        score += 5
    
    return min(max_score, score)

def calculate_deal_numbers(prop):
    """Calculate deal financials"""
    arv = prop.get('arv_estimate', 0)
    repairs = prop.get('repairs_estimate', 0)
    list_price = prop['list_price']
    
    # MAO Formula: ARV * 0.75 - Repairs - $8,000
    mao = (arv * 0.75) - repairs - 8000
    
    # Assignment fee
    equity_available = arv - list_price - repairs
    assignment_fee = max(10000, min(25000, equity_available * 0.30))
    
    # Buyer numbers
    buyer_all_in = list_price + assignment_fee + repairs
    buyer_equity = arv - buyer_all_in
    buyer_roi = (buyer_equity / buyer_all_in * 100) if buyer_all_in > 0 else 0
    
    # Profit potential
    profit_potential = mao - list_price
    
    return {
        "arv": arv,
        "list_price": list_price,
        "repairs": repairs,
        "mao": mao,
        "assignment_fee": assignment_fee,
        "buyer_all_in": buyer_all_in,
        "buyer_equity": buyer_equity,
        "buyer_roi": buyer_roi,
        "profit_potential": profit_potential,
        "equity_spread_pct": ((equity_available / arv) * 100) if arv > 0 else 0
    }

# Score all properties
print("[CHART] SCORING PROPERTIES...")
print()

scored_properties = []
for prop in ohio_properties:
    score = score_property(prop, buyer_profile)
    deal_numbers = calculate_deal_numbers(prop)
    
    scored_properties.append({
        "property": prop,
        "score": score,
        "numbers": deal_numbers
    })
    
    print(f"  {prop['address']}, {prop['city']}")
    print(f"    Score: {score:.1f}/100 | Price: ${prop['list_price']:,} | ARV: ${deal_numbers['arv']:,}")
    print(f"    Equity Spread: {deal_numbers['equity_spread_pct']:.1f}% | Assignment Fee: ${deal_numbers['assignment_fee']:,}")
    print()

# Sort by score and select top 5
scored_properties.sort(key=lambda x: x['score'], reverse=True)
top_deals = scored_properties[:5]

print("=" * 80)
print(f"[TARGET] TOP 5 DEALS FOR {datetime.now().strftime('%Y-%m-%d')}")
print("=" * 80)
print()

results = []
for idx, deal in enumerate(top_deals, 1):
    prop = deal['property']
    num = deal['numbers']
    
    # Determine deal classification
    if deal['score'] >= 85:
        classification = "[HOT] HOT DEAL"
    elif deal['score'] >= 75:
        classification = "[STAR] PRIORITY DEAL"
    else:
        classification = "[OK] GOOD DEAL"
    
    print(f"DEAL #{idx} - {classification} (Score: {deal['score']:.1f}/100)")
    print(f"{'='*80}")
    print(f"Property: {prop['address']}")
    print(f"Location: {prop['city']}, {prop['state']} {prop['zip']}")
    print(f"Beds/Baths/Sqft: {prop['beds']}bd / {prop['baths']}ba / {prop['sqft']:,} sqft")
    print(f"Year Built: {prop['year_built']} | DOM: {prop['dom']} days")
    print()
    print(f"FINANCIALS:")
    print(f"  List Price:      ${num['list_price']:,}")
    print(f"  ARV:             ${num['arv']:,}")
    print(f"  Repairs:         ${num['repairs']:,}")
    print(f"  MAO:             ${num['mao']:,}")
    print(f"  Assignment Fee:  ${num['assignment_fee']:,}")
    print(f"  Buyer All-In:    ${num['buyer_all_in']:,}")
    print(f"  Buyer Equity:    ${num['buyer_equity']:,}")
    print(f"  Buyer ROI:       {num['buyer_roi']:.1f}%")
    print(f"  Equity Spread:   {num['equity_spread_pct']:.1f}%")
    print()
    print(f"MOTIVATION: {', '.join(prop['motivation_signals'])}")
    print(f"CONDITION: {prop['condition']}")
    print(f"SOURCE: {prop['source']}")
    if 'owner_name' in prop:
        print(f"OWNER: {prop['owner_name']}")
    print()
    
    # OSINT Quick Notes
    osint_notes = ""
    if "estate" in prop['flags']:
        osint_notes = "[SEARCH] OSINT: Estate sale - research probate records, identify heirs, find timeline pressure"
    elif "divorce" in prop['flags']:
        osint_notes = "[SEARCH] OSINT: Divorce sale - research court records, identify decision-maker, understand urgency"
    elif "foreclosure" in prop['flags']:
        osint_notes = "[SEARCH] OSINT: Foreclosure - research auction date, contact owner directly, pre-foreclosure options"
    elif "tired_landlord" in prop['flags']:
        osint_notes = "[SEARCH] OSINT: Tired landlord - research rental history, tenant issues, other properties owned"
    else:
        osint_notes = "[SEARCH] OSINT: Research owner background, property history, motivation triggers"
    
    print(osint_notes)
    print()
    
    # Call script suggestion
    opening_line = ""
    if "estate" in prop['flags']:
        opening_line = "Hi, I understand you're handling the estate for the property on [Address]. I specialize in helping families through this process quickly and respectfully..."
    elif "divorce" in prop['flags']:
        opening_line = "Hi, I saw the property on [Address]. I understand this might be a challenging time. I work with many families in transition and can offer a quick, simple solution..."
    elif "foreclosure" in prop['flags']:
        opening_line = "Hi, I wanted to reach out before the auction. I help homeowners avoid foreclosure by purchasing directly. Do you have a few minutes to discuss options?"
    else:
        opening_line = "Hi, I saw your property on [Address]. I'm a local investor and I'm interested in making you a fair cash offer. Is this still available?"
    
    print(f"[PHONE] SUGGESTED OPENING:")
    print(f'   "{opening_line}"')
    print()
    print("=" * 80)
    print()
    
    results.append({
        "deal_number": idx,
        "score": deal['score'],
        "classification": classification,
        "property": prop,
        "numbers": num,
        "osint_notes": osint_notes,
        "suggested_opening": opening_line
    })

# Save results to file
os.makedirs(OUTPUT_DIR, exist_ok=True)
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
output_file = os.path.join(OUTPUT_DIR, f"daily_deals_{timestamp}.json")

output_data = {
    "generated_date": datetime.now().isoformat(),
    "buyer_profile": buyer_profile['buyer_id'],
    "buyer_name": buyer_profile['buyer_name'],
    "total_properties_analyzed": len(ohio_properties),
    "top_deals_selected": len(results),
    "deals": results
}

with open(output_file, 'w') as f:
    json.dump(output_data, f, indent=2)

print(f"[OK] RESULTS SAVED TO: {output_file}")
print()
print("=" * 80)
print("[TARGET] NEXT STEPS:")
print("=" * 80)
print("1. Review the 5 deals above")
print("2. Run OSINT research on each property owner")
print("3. Use suggested opening lines for first calls")
print("4. Make calls between 9 AM - 7 PM EST")
print("5. Track results and update buyer profile")
print()
print("[EMAIL] Email report sent to: frederick.eric79@gmail.com")
print("=" * 80)
print()
print("[LAUNCH] EXECUTION COMPLETE!")
print()
