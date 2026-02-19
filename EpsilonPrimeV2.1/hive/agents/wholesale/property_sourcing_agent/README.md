# Property Sourcing Agent - Autonomous Deal Finder

## Purpose
**THE MOST CRITICAL AGENT** - Automatically finds and pre-qualifies 5+ high-potential wholesale deals EVERY DAY based on buyer criteria, market data, and BuyCartel.com intelligence. This agent STARTS the workflow by sourcing properties, not analyzing ones you already found.

---

## Mission Statement

> "Wake up every morning to 5 ready-to-call deals with complete intelligence, personalized scripts, and buyer-matched criteria. No more hunting - just calling and closing."

---

## How It Works (Daily Automation)

### 6:00 AM - Property Sourcing Agent Activates

```
1. Load Buyer Criteria (from investor profiles)
   ↓
2. Scan Multiple Property Sources
   - BuyCartel.com (primary source)
   - MLS feeds
   - Zillow/Redfin APIs
   - Public records (tax delinquencies, foreclosures)
   - FSBO listings
   - Expired listings
   - Distressed signals
   ↓
3. Apply Intelligent Filters
   - Price range match
   - Property type match
   - Location/market match
   - Motivation signals (DOM, reductions, distress)
   - Equity spread potential
   ↓
4. Score Each Property (1-100)
   - Buyer match score (40%)
   - Motivation score (30%)
   - Equity potential (20%)
   - Market liquidity (10%)
   ↓
5. Select Top 5 Properties
   ↓
6. Run OSINT on Each Property (automated)
   ↓
7. Run Lead Qualifier (generate scripts)
   ↓
8. Run Deal Analyzer (calculate numbers)
   ↓
9. Run Confidence Scorer (validate quality)
   ↓
10. Generate Morning Report
    ↓
11. Send to Your Phone/Email: "Your 5 Deals Are Ready"
```

**By 8:00 AM:** You have 5 fully-researched, pre-qualified deals waiting for your first call.

---

## BuyCartel.com Integration (PRIMARY SOURCE)

### What is BuyCartel.com?

BuyCartel is a wholesale property marketplace that aggregates distressed and wholesale-ready properties from multiple sources. It's designed for investors and wholesalers.

### Why BuyCartel is Perfect for This:

✅ **Pre-filtered for wholesaling** - Properties already have wholesale characteristics  
✅ **Motivation indicators** - Sellers already motivated  
✅ **Direct access** - Contact info often included  
✅ **Multiple markets** - National coverage  
✅ **Deal flow** - Fresh properties added daily  
✅ **Investor-focused** - Properties matched to buyer criteria  

---

## BuyCartel.com Data Extraction Strategy

### What to Extract from BuyCartel:

```python
{
  "property_id": "BC12345",
  "address": "123 Oak Street, Columbus, OH 43201",
  "list_price": 180000,
  "arv": 280000,  # Often provided by BuyCartel
  "estimated_repairs": 35000,  # Often provided
  "beds": 3,
  "baths": 2,
  "sqft": 1400,
  "property_type": "SFR",
  "dom": 52,
  "motivation_flags": ["vacant", "price_reduction", "estate"],
  "seller_info": {
    "name": "John Smith",
    "phone": "614-555-1234",
    "email": "john@email.com"
  },
  "listing_agent": {
    "name": "Jane Realtor",
    "phone": "614-555-5678",
    "brokerage": "ABC Realty"
  },
  "description": "Needs cosmetic updates, vacant, motivated seller",
  "photos": ["url1", "url2"],
  "buycartel_score": 8.5,  # Their internal score if available
  "date_listed": "2026-01-10",
  "market": "Columbus, OH"
}
```

### BuyCartel.com Scraping/API Strategy

**Option 1: Official API (BEST)**
```python
import requests

buycartel_api_key = "YOUR_API_KEY"
headers = {"Authorization": f"Bearer {buycartel_api_key}"}

# Get properties matching criteria
response = requests.get(
    "https://api.buycartel.com/v1/properties",
    headers=headers,
    params={
        "market": "Columbus, OH",
        "price_min": 100000,
        "price_max": 300000,
        "property_type": "SFR",
        "motivation": "high",
        "limit": 50
    }
)

properties = response.json()["properties"]
```

**Option 2: Web Scraping (If no API)**
```python
from playwright import sync_api

# Use Playwright to scrape BuyCartel
with sync_api.sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    
    # Login to BuyCartel
    page.goto("https://buycartel.com/login")
    page.fill("#email", "your_email@email.com")
    page.fill("#password", "your_password")
    page.click("button[type='submit']")
    
    # Navigate to search results
    page.goto("https://buycartel.com/properties?market=Columbus")
    
    # Extract property listings
    properties = page.eval_on_selector_all(
        ".property-card",
        """(elements) => elements.map(el => ({
            address: el.querySelector('.address').textContent,
            price: el.querySelector('.price').textContent,
            arv: el.querySelector('.arv').textContent,
            repairs: el.querySelector('.repairs').textContent,
            beds: el.querySelector('.beds').textContent,
            baths: el.querySelector('.baths').textContent,
            sqft: el.querySelector('.sqft').textContent,
            link: el.querySelector('a').href
        }))"""
    )
    
    browser.close()
```

**Option 3: RSS/Email Alerts**
- Subscribe to BuyCartel email alerts
- Parse incoming emails automatically
- Extract property data from HTML

---

## Buyer Criteria Configuration

### Investor Profile Template

Create profiles for your buyers:

```json
{
  "buyer_id": "BUYER001",
  "buyer_name": "Mike Johnson - Fix & Flip Investor",
  "active": true,
  "preferred_contact": "email",
  "email": "mike@investor.com",
  "phone": "614-555-9999",
  
  "criteria": {
    "markets": ["Columbus, OH", "Cleveland, OH", "Cincinnati, OH"],
    "property_types": ["SFR", "2-4 Unit"],
    "price_range": {
      "min": 100000,
      "max": 300000
    },
    "arv_range": {
      "min": 200000,
      "max": 500000
    },
    "desired_spread": {
      "minimum_equity_spread_pct": 25,
      "minimum_profit_potential": 40000
    },
    "repair_tolerance": {
      "min": 10000,
      "max": 60000,
      "prefer": "moderate"  # light, moderate, heavy
    },
    "strategy_preference": ["fix_flip", "brrrr"],
    "must_have": {
      "min_beds": 3,
      "min_baths": 1,
      "min_sqft": 1000,
      "max_dom": 90
    },
    "motivation_required": true,
    "motivation_signals": [
      "vacant",
      "price_reduction",
      "estate",
      "foreclosure",
      "tax_delinquency",
      "divorce",
      "relocation"
    ],
    "avoid": {
      "flood_zones": true,
      "hoa_fees_over": 200,
      "major_structural_issues": true
    }
  },
  
  "financial_requirements": {
    "min_buyer_roi": 20,
    "max_assignment_fee": 20000,
    "closing_timeline": "21 days",
    "proof_of_funds": true
  },
  
  "deal_volume": {
    "current_active_deals": 2,
    "max_concurrent_deals": 5,
    "closed_last_30_days": 3
  }
}
```

### Multiple Buyer Profiles

Store multiple buyer profiles and match properties to the best fit:

```
/config/buyer_profiles/
├── buyer_001_mike_fix_flip.json
├── buyer_002_sarah_brrrr.json
├── buyer_003_david_rentals.json
├── buyer_004_lisa_wholesale.json
└── buyer_005_team_hybrid.json
```

---

## Property Scoring Algorithm

### Overall Score Formula (1-100)

```
Property Score = 
  (Buyer Match × 0.40) +
  (Motivation Score × 0.30) +
  (Equity Potential × 0.20) +
  (Market Liquidity × 0.10)
```

### Component Breakdown

#### 1. Buyer Match Score (0-100 points, weight 40%)

```python
def calculate_buyer_match(property, buyer_criteria):
    score = 0
    max_score = 100
    
    # Price range match (25 points)
    if buyer_criteria["price_range"]["min"] <= property["list_price"] <= buyer_criteria["price_range"]["max"]:
        score += 25
    
    # Property type match (15 points)
    if property["property_type"] in buyer_criteria["property_types"]:
        score += 15
    
    # Market match (15 points)
    if property["market"] in buyer_criteria["markets"]:
        score += 15
    
    # Bed/bath/sqft requirements (15 points)
    if (property["beds"] >= buyer_criteria["must_have"]["min_beds"] and
        property["baths"] >= buyer_criteria["must_have"]["min_baths"] and
        property["sqft"] >= buyer_criteria["must_have"]["min_sqft"]):
        score += 15
    
    # Repair tolerance (10 points)
    repair_range = buyer_criteria["repair_tolerance"]
    if repair_range["min"] <= property["estimated_repairs"] <= repair_range["max"]:
        score += 10
    
    # DOM requirement (10 points)
    if property["dom"] <= buyer_criteria["must_have"]["max_dom"]:
        score += 10
    
    # Strategy match (10 points)
    if property["suggested_strategy"] in buyer_criteria["strategy_preference"]:
        score += 10
    
    return score
```

#### 2. Motivation Score (0-100 points, weight 30%)

```python
def calculate_motivation_score(property):
    score = 50  # Baseline
    
    # DOM scoring
    if property["dom"] > 90:
        score += 25
    elif property["dom"] > 60:
        score += 20
    elif property["dom"] > 30:
        score += 15
    
    # Motivation flags (5 points each, max 25)
    motivation_flags = property.get("motivation_flags", [])
    flag_points = min(len(motivation_flags) * 5, 25)
    score += flag_points
    
    # Price reductions (if data available)
    if "price_reductions" in property:
        reductions = property["price_reductions"]
        if reductions >= 3:
            score += 15
        elif reductions >= 2:
            score += 10
        elif reductions >= 1:
            score += 5
    
    # Occupancy status
    if "vacant" in motivation_flags:
        score += 10
    
    return min(score, 100)
```

#### 3. Equity Potential Score (0-100 points, weight 20%)

```python
def calculate_equity_potential(property, buyer_criteria):
    score = 0
    
    arv = property.get("arv", 0)
    list_price = property["list_price"]
    repairs = property.get("estimated_repairs", 0)
    
    if arv == 0:
        return 50  # Can't score without ARV
    
    # Calculate spread percentage
    spread_pct = ((arv - list_price - repairs) / arv) * 100
    
    # Score based on spread
    if spread_pct >= 40:
        score = 100
    elif spread_pct >= 30:
        score = 85
    elif spread_pct >= 25:
        score = 70
    elif spread_pct >= 20:
        score = 55
    elif spread_pct >= 15:
        score = 40
    else:
        score = 20
    
    # Bonus: meets buyer's minimum spread requirement
    if spread_pct >= buyer_criteria["desired_spread"]["minimum_equity_spread_pct"]:
        score = min(score + 10, 100)
    
    # Calculate absolute profit potential
    profit_potential = arv - list_price - repairs
    if profit_potential >= buyer_criteria["desired_spread"]["minimum_profit_potential"]:
        score = min(score + 10, 100)
    
    return score
```

#### 4. Market Liquidity Score (0-100 points, weight 10%)

```python
def calculate_market_liquidity(property):
    score = 50  # Baseline
    
    list_price = property["list_price"]
    market = property["market"]
    
    # Sweet spot price range (most liquid)
    if 150000 <= list_price <= 300000:
        score += 30
    elif 100000 <= list_price < 150000 or 300000 < list_price <= 400000:
        score += 20
    elif list_price < 100000 or list_price > 400000:
        score += 10
    
    # Market activity (if data available from BuyCartel)
    if "market_data" in property:
        activity = property["market_data"]["activity_level"]
        if activity == "hot":
            score += 20
        elif activity == "warm":
            score += 10
    
    return min(score, 100)
```

---

## Daily Automation Workflow

### Morning Routine Script

```python
"""
Property Sourcing Agent - Daily Automation
Runs every morning at 6:00 AM
"""

import json
from datetime import datetime
from pathlib import Path

class PropertySourcingAgent:
    def __init__(self):
        self.project_root = Path("C:/Users/Media Server/Desktop/Wholesale_AI_Project")
        self.buyer_profiles = self.load_buyer_profiles()
        self.properties_found = []
        self.top_5_deals = []
        
    def load_buyer_profiles(self):
        """Load all active buyer profiles"""
        profiles_dir = self.project_root / "config" / "buyer_profiles"
        profiles = []
        
        for profile_file in profiles_dir.glob("*.json"):
            with open(profile_file, 'r') as f:
                profile = json.load(f)
                if profile.get("active", True):
                    profiles.append(profile)
        
        return profiles
    
    def daily_scan(self):
        """Main daily property scanning routine"""
        print(f"\n{'='*80}")
        print(f"PROPERTY SOURCING AGENT - DAILY SCAN")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}\n")
        
        # Step 1: Scan BuyCartel.com
        print("Step 1: Scanning BuyCartel.com...")
        buycartel_properties = self.scan_buycartel()
        print(f"   Found {len(buycartel_properties)} properties on BuyCartel")
        
        # Step 2: Scan MLS (if available)
        print("\nStep 2: Scanning MLS feeds...")
        mls_properties = self.scan_mls()
        print(f"   Found {len(mls_properties)} properties on MLS")
        
        # Step 3: Scan Zillow/Redfin
        print("\nStep 3: Scanning Zillow & Redfin...")
        zillow_properties = self.scan_zillow()
        print(f"   Found {len(zillow_properties)} properties on Zillow")
        
        # Step 4: Scan public distress records
        print("\nStep 4: Scanning distress signals...")
        distress_properties = self.scan_distress_signals()
        print(f"   Found {len(distress_properties)} distressed properties")
        
        # Combine all sources
        all_properties = (buycartel_properties + mls_properties + 
                         zillow_properties + distress_properties)
        print(f"\n   TOTAL PROPERTIES FOUND: {len(all_properties)}")
        
        # Step 5: Score and filter
        print("\nStep 5: Scoring properties against buyer criteria...")
        scored_properties = self.score_properties(all_properties)
        
        # Step 6: Select top 5
        print("\nStep 6: Selecting top 5 properties...")
        self.top_5_deals = sorted(scored_properties, 
                                   key=lambda x: x['total_score'], 
                                   reverse=True)[:5]
        
        for i, deal in enumerate(self.top_5_deals, 1):
            print(f"   #{i}: {deal['address']} - Score: {deal['total_score']:.1f}/100")
        
        # Step 7: Run intelligence on top 5
        print("\nStep 7: Running intelligence gathering on top 5...")
        self.enrich_properties()
        
        # Step 8: Generate morning report
        print("\nStep 8: Generating morning report...")
        self.generate_morning_report()
        
        # Step 9: Send notification
        print("\nStep 9: Sending notification...")
        self.send_notification()
        
        print(f"\n{'='*80}")
        print("DAILY SCAN COMPLETE - YOUR DEALS ARE READY!")
        print(f"{'='*80}\n")
        
        return self.top_5_deals
    
    def scan_buycartel(self):
        """Scan BuyCartel.com for properties"""
        # This would use actual BuyCartel API/scraping
        # For now, return example structure
        
        # IMPLEMENTATION NEEDED:
        # 1. Connect to BuyCartel API or scrape website
        # 2. Apply buyer criteria as search filters
        # 3. Extract property data
        # 4. Return standardized property objects
        
        properties = []
        
        for buyer_profile in self.buyer_profiles:
            # Search BuyCartel with buyer's criteria
            criteria = buyer_profile["criteria"]
            
            # Example API call (pseudocode)
            # results = buycartel_api.search(
            #     markets=criteria["markets"],
            #     price_min=criteria["price_range"]["min"],
            #     price_max=criteria["price_range"]["max"],
            #     motivation=True
            # )
            
            # For demo, using placeholder
            results = self.mock_buycartel_results(criteria)
            properties.extend(results)
        
        # Remove duplicates
        unique_properties = self.deduplicate_properties(properties)
        return unique_properties
    
    def scan_mls(self):
        """Scan MLS feeds"""
        # IMPLEMENTATION NEEDED:
        # 1. Connect to MLS API (RETS, RESO, etc.)
        # 2. Filter for wholesale-ready properties
        # 3. Return standardized format
        
        return []  # Placeholder
    
    def scan_zillow(self):
        """Scan Zillow/Redfin for FSBO and motivated sellers"""
        # IMPLEMENTATION NEEDED:
        # 1. Use Zillow API or scraping
        # 2. Filter for long DOM, price reductions
        # 3. Return standardized format
        
        return []  # Placeholder
    
    def scan_distress_signals(self):
        """Scan public records for distress signals"""
        # IMPLEMENTATION NEEDED:
        # 1. Access county tax records (delinquencies)
        # 2. Access foreclosure filings
        # 3. Access probate/estate records
        # 4. Return properties with distress signals
        
        return []  # Placeholder
    
    def score_properties(self, properties):
        """Score each property against buyer criteria"""
        scored = []
        
        for prop in properties:
            # Find best matching buyer
            best_match = None
            best_score = 0
            
            for buyer in self.buyer_profiles:
                buyer_match_score = self.calculate_buyer_match(prop, buyer)
                if buyer_match_score > best_score:
                    best_score = buyer_match_score
                    best_match = buyer
            
            if best_match:
                # Calculate all score components
                motivation_score = self.calculate_motivation_score(prop)
                equity_score = self.calculate_equity_potential(prop, best_match)
                liquidity_score = self.calculate_market_liquidity(prop)
                
                # Calculate weighted total
                total_score = (
                    (buyer_match_score * 0.40) +
                    (motivation_score * 0.30) +
                    (equity_score * 0.20) +
                    (liquidity_score * 0.10)
                )
                
                prop["buyer_match"] = best_match
                prop["scores"] = {
                    "buyer_match": buyer_match_score,
                    "motivation": motivation_score,
                    "equity_potential": equity_score,
                    "market_liquidity": liquidity_score
                }
                prop["total_score"] = total_score
                
                # Only include if score > 70
                if total_score >= 70:
                    scored.append(prop)
        
        return scored
    
    def enrich_properties(self):
        """Run OSINT, Deal Analysis, etc. on top 5"""
        for deal in self.top_5_deals:
            print(f"   Processing: {deal['address']}...")
            
            # Run OSINT Agent
            osint_report = self.run_osint(deal)
            deal["osint"] = osint_report
            
            # Run Lead Qualifier
            lead_sheet = self.run_lead_qualifier(deal)
            deal["lead_sheet"] = lead_sheet
            
            # Run Deal Analyzer
            deal_analysis = self.run_deal_analyzer(deal)
            deal["deal_analysis"] = deal_analysis
            
            # Run Confidence Scorer
            confidence = self.run_confidence_scorer(deal)
            deal["confidence"] = confidence
            
            # Generate packet if approved
            if confidence["overall_score"] >= 0.60:
                packet = self.run_packet_generator(deal)
                deal["packet"] = packet
    
    def generate_morning_report(self):
        """Generate the daily morning report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.project_root / "output" / "daily_reports" / f"{timestamp}_morning_report.txt"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("DAILY PROPERTY SOURCING REPORT\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n\n")
            
            f.write("YOUR TOP 5 DEALS TODAY:\n\n")
            
            for i, deal in enumerate(self.top_5_deals, 1):
                f.write(f"\n{'='*80}\n")
                f.write(f"DEAL #{i}\n")
                f.write(f"{'='*80}\n\n")
                
                f.write(f"PROPERTY: {deal['address']}\n")
                f.write(f"SCORE: {deal['total_score']:.1f}/100\n")
                f.write(f"BUYER MATCH: {deal['buyer_match']['buyer_name']}\n\n")
                
                f.write(f"QUICK FACTS:\n")
                f.write(f"  List Price: ${deal['list_price']:,}\n")
                f.write(f"  ARV: ${deal.get('arv', 0):,}\n")
                f.write(f"  Repairs: ${deal.get('estimated_repairs', 0):,}\n")
                f.write(f"  Beds/Baths: {deal['beds']}/{deal['baths']}\n")
                f.write(f"  Sqft: {deal['sqft']:,}\n")
                f.write(f"  DOM: {deal['dom']} days\n\n")
                
                f.write(f"MOTIVATION:\n")
                f.write(f"  Urgency: {deal['osint']['urgency_score']}/10\n")
                f.write(f"  Primary: {deal['osint']['primary_motivation']}\n\n")
                
                f.write(f"DEAL NUMBERS:\n")
                f.write(f"  Seller Offer: ${deal['deal_analysis']['seller_offer']:,}\n")
                f.write(f"  Buyer Price: ${deal['deal_analysis']['buyer_price']:,}\n")
                f.write(f"  Assignment Fee: ${deal['deal_analysis']['assignment_fee']:,}\n")
                f.write(f"  Buyer ROI: {deal['deal_analysis']['buyer_roi']*100:.1f}%\n\n")
                
                f.write(f"YOUR OPENING LINE:\n")
                f.write(f'  "{deal["lead_sheet"]["recommended_opening"]}"\n\n')
                
                f.write(f"NEXT STEPS:\n")
                for step in deal["lead_sheet"]["next_steps"]:
                    f.write(f"  - {step}\n")
        
        print(f"   Report saved: {report_path}")
        return report_path
    
    def send_notification(self):
        """Send notification that deals are ready"""
        # IMPLEMENTATION OPTIONS:
        # 1. Email
        # 2. SMS (Twilio)
        # 3. Push notification
        # 4. Slack/Discord message
        
        message = f"""
        🎯 YOUR 5 DAILY DEALS ARE READY!
        
        The Property Sourcing Agent has found and analyzed your top 5 deals.
        
        - All properties scored 70+ (high quality)
        - OSINT intelligence gathered
        - Personalized scripts ready
        - Deal numbers calculated
        - Investor packets generated
        
        Open your morning report to start calling!
        """
        
        print(message)
        # Send actual notification here
    
    # Helper methods (implementations in config.json)
    def calculate_buyer_match(self, prop, buyer): pass
    def calculate_motivation_score(self, prop): pass
    def calculate_equity_potential(self, prop, buyer): pass
    def calculate_market_liquidity(self, prop): pass
    def run_osint(self, deal): pass
    def run_lead_qualifier(self, deal): pass
    def run_deal_analyzer(self, deal): pass
    def run_confidence_scorer(self, deal): pass
    def run_packet_generator(self, deal): pass
    def deduplicate_properties(self, props): pass
    def mock_buycartel_results(self, criteria): pass


# Schedule to run daily at 6:00 AM
if __name__ == "__main__":
    agent = PropertySourcingAgent()
    agent.daily_scan()
```

---

## Integration Requirements

### 1. BuyCartel.com Account Setup

**You Need:**
- BuyCartel.com account (paid membership likely required)
- API key (if they offer API access)
- Or: Login credentials for web scraping

**Steps:**
1. Sign up at buycartel.com
2. Explore their data export options
3. Check if they have API documentation
4. If no API, prepare for web scraping (Playwright)

---

### 2. Buyer Profile Configuration

**Create profiles in:**
`/config/buyer_profiles/buyer_001.json`

**Include:**
- Contact information
- Market preferences
- Property criteria
- Financial requirements
- Deal volume capacity

---

### 3. Daily Automation Setup

**Option A: Windows Task Scheduler**
```
Task: Run Property Sourcing Agent
Schedule: Daily at 6:00 AM
Action: python property_sourcing_script.py
```

**Option B: Blackbox Scheduled Recipe**
```
Schedule wholesale-property-sourcing recipe:
  Frequency: Daily at 6:00 AM
  Notification: Email/SMS when complete
```

---

### 4. Notification Setup

**Choose method:**
- **Email:** Use SendGrid, Mailgun, or SMTP
- **SMS:** Use Twilio
- **Push:** Use Pushover, Pushbullet
- **Slack/Discord:** Webhook integration

---

## Morning Report Format

```
================================================================================
                      DAILY PROPERTY SOURCING REPORT
                     Generated: 2026-01-19 08:00:00 AM
================================================================================

SUMMARY:
- Properties Scanned: 247
- Properties Scored: 89
- Top 5 Selected: YES
- Average Score: 78.4/100
- All Intelligence Gathered: COMPLETE

YOUR TOP 5 DEALS TODAY:

================================================================================
DEAL #1 - SCORE: 87.5/100
================================================================================

PROPERTY: 456 Maple Avenue, Cleveland, OH 44120
BUYER MATCH: Mike Johnson - Fix & Flip Investor (BUYER001)

QUICK FACTS:
  List Price: $150,000
  ARV: $245,000
  Repairs: $42,000
  Beds/Baths/Sqft: 3/1/1,200
  DOM: 68 days
  Condition: Needs moderate rehab
  Flags: vacant, estate, price_reduction

OWNER INTELLIGENCE (OSINT):
  Name: Sarah Mitchell (Estate Executor)
  Age: 52
  Situation: Inherited property from father (deceased 4 months ago)
  Urgency: 9/10 (needs to close estate within 6 months)
  Other Properties: None (not an investor)
  Motivation: Estate settlement, out-of-state, wants quick close
  
RAPPORT POINTS:
  - Compassionate about loss
  - Acknowledges estate stress
  - Emphasizes simplicity and speed
  - Father was veteran (respect military service)

DEAL NUMBERS:
  Seller Offer: $138,000
  Buyer Price: $153,000
  Assignment Fee: $15,000
  All-In (Buyer): $195,000
  Projected Profit: $32,000
  Buyer ROI: 21.4%
  Strategy: Wholesale Cash

CONFIDENCE SCORE: 0.84 (Priority Deal)
  - Seller Motivation: 0.95 (estate urgency)
  - Equity & Spread: 0.80 (good margin)
  - Deal Simplicity: 0.75 (minor title work needed)
  - Market Liquidity: 0.85 (hot price band)

YOUR OPENING LINE:
  "Hi Sarah, this is [Your Name]. I wanted to reach out personally 
  about your father's property on Maple Avenue. First, I'm sorry for 
  your loss - I know handling an estate can be overwhelming, especially 
  from out of state. I work with investors who can close quickly and 
  handle everything as-is, which might take some stress off your plate. 
  Did I catch you at an okay time?"

SELLER CONTACT:
  Phone: (216) 555-1234
  Email: sarah.mitchell@email.com
  Best Time: Evenings (works full-time)

NEXT STEPS:
  1. Call between 6-8 PM today
  2. Use empathy-first approach (estate situation)
  3. Emphasize fast close and simplicity
  4. Mention Mike Johnson is ready to move (proof of funds available)
  5. Send packet if interested

INVESTOR PACKET: Generated (/output/packets/20260119_456_Maple_packet.pdf)

FILES:
  - OSINT Report: /output/osint/20260119_080001_456_Maple.txt
  - Lead Sheet: /output/lead_sheets/20260119_080001_456_Maple.txt
  - Deal Analysis: /output/deals/20260119_080001_456_Maple/deal_analysis.json
  - Investor Packet: /output/packets/20260119_080001_456_Maple_packet.pdf

================================================================================
DEAL #2 - SCORE: 82.3/100
================================================================================

[Deal #2 details...]

================================================================================
DEAL #3 - SCORE: 79.8/100
================================================================================

[Deal #3 details...]

================================================================================
DEAL #4 - SCORE: 76.2/100
================================================================================

[Deal #4 details...]

================================================================================
DEAL #5 - SCORE: 74.1/100
================================================================================

[Deal #5 details...]

================================================================================
                              END OF REPORT
================================================================================

ACTION REQUIRED: Call all 5 properties today. Scripts and numbers ready.

Questions? Review individual reports in /output/
Need help? Check PROPERTY_SOURCING_AGENT/README.md
```

---

## Expected Daily Routine (YOUR PERSPECTIVE)

### 7:45 AM - Wake Up
Phone notification: "🎯 Your 5 Daily Deals Are Ready!"

### 8:00 AM - Review Morning Report
- Read property summaries
- Review OSINT intelligence
- Check deal numbers
- Read personalized scripts

### 8:30 AM - Start Calling
**Deal #1:** Use personalized opening, build rapport, discuss terms
**Deal #2:** ...
**Deal #3:** ...
**Deal #4:** ...
**Deal #5:** ...

### 10:30 AM - Follow Up
- Send packets to interested sellers
- Schedule property viewings
- Loop in buyers on hot deals

### 12:00 PM - Done!
All outreach complete, deals in motion, rest of day free.

---

## Implementation Checklist

### Phase 1: Setup (Week 1)
- [ ] Create BuyCartel.com account
- [ ] Get API access or scraping credentials
- [ ] Create buyer profiles (at least 1-2 to start)
- [ ] Set up notification method (email/SMS)
- [ ] Test data extraction from BuyCartel

### Phase 2: Agent Development (Week 2)
- [ ] Build BuyCartel scraper/API integration
- [ ] Implement property scoring algorithm
- [ ] Connect to OSINT Agent
- [ ] Connect to other 4 agents
- [ ] Build morning report generator

### Phase 3: Automation (Week 3)
- [ ] Schedule daily execution (6 AM)
- [ ] Test full workflow end-to-end
- [ ] Verify all outputs generated correctly
- [ ] Confirm notifications working

### Phase 4: Optimization (Week 4)
- [ ] Refine buyer criteria based on results
- [ ] Adjust scoring weights
- [ ] Add additional data sources
- [ ] Improve OSINT accuracy
- [ ] Track conversion rates

---

## Success Metrics

**Track These Weekly:**
- Properties scanned per day
- Properties scored >70 per day
- Top 5 quality (average score)
- Call-to-appointment rate
- Appointment-to-contract rate
- Deals closed from sourced properties
- Time saved vs. manual searching

**Goal:**
- 5 high-quality deals delivered daily
- 80%+ score accuracy (properties meet criteria)
- 50%+ first-call success rate
- 2-3 contracts per week from sourced deals

---

This is THE GAME CHANGER. Wake up to pre-researched, pre-qualified deals every single day!

Want me to create the full implementation files for the Property Sourcing Agent?
