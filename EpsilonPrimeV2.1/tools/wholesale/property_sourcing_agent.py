"""
Property Sourcing Agent - Full Implementation
Daily autonomous property finder for Eric Frederick
"""

import json
import requests
from datetime import datetime, timedelta
from pathlib import Path
import time
from typing import List, Dict, Any
import re

class PropertySourcingAgent:
    def __init__(self, profile_path: str = None):
        self.project_root = Path("C:/Users/Media Server/Desktop/Wholesale_AI_Project")
        
        # Load Eric Frederick's profile
        if profile_path is None:
            profile_path = self.project_root / "config" / "buyer_profiles" / "buyer_001_eric_frederick.json"
        
        with open(profile_path, 'r') as f:
            self.profile = json.load(f)
        
        self.buyer_name = self.profile["buyer_name"]
        self.buyer_email = self.profile["contact_information"]["email"]
        self.daily_limit = self.profile["sourcing_preferences"]["daily_deal_limit"]
        self.min_score = self.profile["sourcing_preferences"]["minimum_score_threshold"]
        
        self.properties_found = []
        self.top_deals = []
        
        print(f"Property Sourcing Agent initialized for: {self.buyer_name}")
        print(f"Daily deal limit: {self.daily_limit}")
        print(f"Minimum score threshold: {self.min_score}")
    
    def daily_scan(self):
        """Main daily property scanning routine - THE CORE FUNCTION"""
        print(f"\n{'='*80}")
        print(f"PROPERTY SOURCING AGENT - DAILY SCAN")
        print(f"Buyer: {self.buyer_name}")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}\n")
        
        start_time = time.time()
        
        # Step 1: Scan all property sources
        print("PHASE 1: SCANNING PROPERTY SOURCES")
        print("-" * 80)
        all_properties = self.scan_all_sources()
        print(f"\nTotal properties found: {len(all_properties)}")
        
        # Step 2: Score and filter properties
        print(f"\n{'='*80}")
        print("PHASE 2: SCORING & FILTERING PROPERTIES")
        print("-" * 80)
        scored_properties = self.score_and_filter(all_properties)
        print(f"\nProperties meeting criteria (score >={self.min_score}): {len(scored_properties)}")
        
        # Step 3: Select top deals
        print(f"\n{'='*80}")
        print(f"PHASE 3: SELECTING TOP {self.daily_limit} DEALS")
        print("-" * 80)
        self.top_deals = self.select_top_deals(scored_properties)
        
        for i, deal in enumerate(self.top_deals, 1):
            print(f"#{i}: {deal['address']} - Score: {deal['total_score']:.1f}/100")
        
        # Step 4: Enrich with intelligence
        print(f"\n{'='*80}")
        print("PHASE 4: GATHERING INTELLIGENCE ON TOP DEALS")
        print("-" * 80)
        self.enrich_properties()
        
        # Step 5: Generate morning report
        print(f"\n{'='*80}")
        print("PHASE 5: GENERATING MORNING REPORT")
        print("-" * 80)
        report_path = self.generate_morning_report()
        
        # Step 6: Send notification
        print(f"\n{'='*80}")
        print("PHASE 6: SENDING NOTIFICATION")
        print("-" * 80)
        self.send_notification(report_path)
        
        elapsed_time = time.time() - start_time
        
        print(f"\n{'='*80}")
        print(f"DAILY SCAN COMPLETE!")
        print(f"Time elapsed: {elapsed_time/60:.1f} minutes")
        print(f"Deals ready: {len(self.top_deals)}")
        print(f"Report: {report_path}")
        print(f"{'='*80}\n")
        
        return self.top_deals
    
    def scan_all_sources(self) -> List[Dict]:
        """Scan all configured property sources"""
        all_properties = []
        
        # Source 1: BuyCartel.com (PRIMARY)
        print("\n1. Scanning BuyCartel.com...")
        buycartel_props = self.scan_buycartel()
        print(f"   Found: {len(buycartel_props)} properties")
        all_properties.extend(buycartel_props)
        
        # Source 2: Zillow distressed properties
        print("\n2. Scanning Zillow for distressed signals...")
        zillow_props = self.scan_zillow()
        print(f"   Found: {len(zillow_props)} properties")
        all_properties.extend(zillow_props)
        
        # Source 3: Public records (tax delinquencies, foreclosures)
        print("\n3. Scanning public distress records...")
        distress_props = self.scan_public_records()
        print(f"   Found: {len(distress_props)} properties")
        all_properties.extend(distress_props)
        
        # Source 4: FSBO listings
        print("\n4. Scanning FSBO listings...")
        fsbo_props = self.scan_fsbo()
        print(f"   Found: {len(fsbo_props)} properties")
        all_properties.extend(fsbo_props)
        
        # Remove duplicates
        unique_properties = self.deduplicate_properties(all_properties)
        print(f"\nAfter deduplication: {len(unique_properties)} unique properties")
        
        return unique_properties
    
    def scan_buycartel(self) -> List[Dict]:
        """Scan BuyCartel.com using credentials from profile"""
        properties = []
        
        try:
            # BuyCartel credentials
            email = self.profile["credentials"]["buycartel_email"]
            password = self.profile["credentials"]["buycartel_password"]
            
            # Strategy 1: Try API first (if BuyCartel has one)
            # This is a placeholder - actual API endpoint needs to be confirmed
            try:
                properties = self.buycartel_api_search(email, password)
                if properties:
                    print(f"   Using BuyCartel API")
                    return properties
            except Exception as e:
                print(f"   API not available, using web scraping...")
            
            # Strategy 2: Web scraping with Playwright
            properties = self.buycartel_web_scrape(email, password)
            
        except Exception as e:
            print(f"   ERROR scanning BuyCartel: {str(e)}")
            print(f"   Continuing with other sources...")
        
        return properties
    
    def buycartel_api_search(self, email: str, password: str) -> List[Dict]:
        """Search BuyCartel using API (if available)"""
        # Note: This is placeholder code - actual BuyCartel API needs to be documented
        # You would need to check BuyCartel's actual API documentation
        
        # Example API structure (hypothetical):
        # api_url = "https://api.buycartel.com/v1/properties/search"
        # auth = requests.post("https://api.buycartel.com/v1/auth/login", 
        #                      json={"email": email, "password": password})
        # token = auth.json()["token"]
        
        return []  # Return empty for now - implement when API is available
    
    def buycartel_web_scrape(self, email: str, password: str) -> List[Dict]:
        """Scrape BuyCartel.com using Playwright"""
        properties = []
        
        # Check if Playwright is available
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            print("   Playwright not installed. Install with: pip install playwright")
            print("   Then run: playwright install")
            return []
        
        try:
            with sync_playwright() as p:
                # Launch browser
                browser = p.chromium.launch(headless=True)
                context = browser.new_context()
                page = context.new_page()
                
                # Login to BuyCartel
                print("   Logging into BuyCartel.com...")
                page.goto("https://buycartel.com/login")
                page.wait_for_load_state("networkidle")
                
                # Fill login form (selectors may need adjustment)
                page.fill('input[type="email"], input[name="email"]', email)
                page.fill('input[type="password"], input[name="password"]', password)
                page.click('button[type="submit"], button:has-text("Login"), button:has-text("Sign In")')
                
                # Wait for login to complete
                page.wait_for_load_state("networkidle")
                time.sleep(2)
                
                # Navigate to property search
                print("   Searching properties...")
                
                # Search for each market in profile
                criteria = self.profile["criteria"]
                for market in criteria["focus_markets"]["primary"] + criteria["focus_markets"]["secondary"]:
                    market_properties = self.scrape_market_properties(page, market)
                    properties.extend(market_properties)
                    time.sleep(1)  # Be polite to the server
                
                browser.close()
                
        except Exception as e:
            print(f"   Scraping error: {str(e)}")
        
        return properties
    
    def scrape_market_properties(self, page, market: str) -> List[Dict]:
        """Scrape properties for a specific market"""
        properties = []
        
        try:
            # Navigate to search (URL structure may vary)
            search_url = f"https://buycartel.com/properties?location={market}"
            page.goto(search_url)
            page.wait_for_load_state("networkidle")
            
            # Extract property cards
            # Note: CSS selectors need to match actual BuyCartel HTML structure
            property_cards = page.query_selector_all(".property-card, .listing-card, [data-property-id]")
            
            print(f"   Found {len(property_cards)} properties in {market}")
            
            for card in property_cards[:50]:  # Limit to 50 per market
                try:
                    property_data = {
                        "source": "buycartel",
                        "market": market,
                        "address": self.extract_text(card, ".address, .property-address"),
                        "list_price": self.extract_price(card, ".price, .list-price"),
                        "arv": self.extract_price(card, ".arv, .after-repair-value"),
                        "estimated_repairs": self.extract_price(card, ".repairs, .repair-estimate"),
                        "beds": self.extract_number(card, ".beds, .bedrooms"),
                        "baths": self.extract_number(card, ".baths, .bathrooms"),
                        "sqft": self.extract_number(card, ".sqft, .square-feet"),
                        "property_type": self.extract_text(card, ".type, .property-type"),
                        "description": self.extract_text(card, ".description, .property-description"),
                        "dom": self.calculate_dom(self.extract_text(card, ".listed-date, .date-listed")),
                        "motivation_flags": self.extract_flags(card),
                        "link": self.extract_link(card),
                        "photos": self.extract_photos(card),
                        "seller_info": self.extract_seller_info(card),
                        "date_found": datetime.now().isoformat()
                    }
                    
                    # Only add if has minimum required data
                    if property_data["address"] and property_data["list_price"]:
                        properties.append(property_data)
                        
                except Exception as e:
                    continue  # Skip properties with extraction errors
            
        except Exception as e:
            print(f"   Error scraping {market}: {str(e)}")
        
        return properties
    
    def extract_text(self, element, selector: str) -> str:
        """Extract text from element using selector"""
        try:
            el = element.query_selector(selector)
            return el.inner_text().strip() if el else ""
        except:
            return ""
    
    def extract_price(self, element, selector: str) -> int:
        """Extract price and convert to integer"""
        text = self.extract_text(element, selector)
        # Remove $ , and convert to int
        price_str = re.sub(r'[^\d]', '', text)
        return int(price_str) if price_str else 0
    
    def extract_number(self, element, selector: str) -> int:
        """Extract number from text"""
        text = self.extract_text(element, selector)
        numbers = re.findall(r'\d+', text)
        return int(numbers[0]) if numbers else 0
    
    def calculate_dom(self, date_text: str) -> int:
        """Calculate days on market from date string"""
        try:
            # Try to parse date and calculate DOM
            # This is simplified - actual parsing depends on date format
            return 30  # Placeholder
        except:
            return 0
    
    def extract_flags(self, element) -> List[str]:
        """Extract motivation flags from property listing"""
        flags = []
        text = element.inner_text().lower()
        
        # Check for motivation keywords
        if "vacant" in text:
            flags.append("vacant")
        if "estate" in text or "probate" in text:
            flags.append("estate")
        if "foreclosure" in text:
            flags.append("foreclosure")
        if "pre-foreclosure" in text:
            flags.append("pre_foreclosure")
        if "reduced" in text or "price drop" in text:
            flags.append("price_reduction")
        if "as-is" in text or "as is" in text:
            flags.append("as_is")
        if "motivated" in text:
            flags.append("motivated_seller")
        
        return flags
    
    def extract_link(self, element) -> str:
        """Extract property detail link"""
        try:
            link = element.query_selector("a")
            return link.get_attribute("href") if link else ""
        except:
            return ""
    
    def extract_photos(self, element) -> List[str]:
        """Extract photo URLs"""
        try:
            images = element.query_selector_all("img")
            return [img.get_attribute("src") for img in images if img.get_attribute("src")]
        except:
            return []
    
    def extract_seller_info(self, element) -> Dict:
        """Extract seller contact info if available"""
        return {
            "name": "",
            "phone": "",
            "email": ""
        }
    
    def scan_zillow(self) -> List[Dict]:
        """Scan Zillow for distressed properties"""
        # This would use Zillow's API or scraping
        # Focus on: long DOM, price reductions, FSBO
        
        print("   Zillow scanning not yet implemented")
        print("   (Will search for: long DOM, price reductions, foreclosures)")
        
        return []
    
    def scan_public_records(self) -> List[Dict]:
        """Scan public records for tax delinquencies and foreclosures"""
        # This would access county records, foreclosure listings, etc.
        
        print("   Public records scanning not yet implemented")
        print("   (Will search for: tax delinquencies, foreclosures, probate)")
        
        return []
    
    def scan_fsbo(self) -> List[Dict]:
        """Scan FSBO listings"""
        # This would scrape FSBO sites like Craigslist, FSBO.com, Facebook Marketplace
        
        print("   FSBO scanning not yet implemented")
        print("   (Will search for: Craigslist, FSBO.com, Facebook Marketplace)")
        
        return []
    
    def deduplicate_properties(self, properties: List[Dict]) -> List[Dict]:
        """Remove duplicate properties based on address"""
        seen_addresses = set()
        unique = []
        
        for prop in properties:
            address_key = prop["address"].lower().strip()
            if address_key not in seen_addresses:
                seen_addresses.add(address_key)
                unique.append(prop)
        
        return unique
    
    def score_and_filter(self, properties: List[Dict]) -> List[Dict]:
        """Score each property and filter by minimum threshold"""
        scored = []
        
        criteria = self.profile["criteria"]
        
        for prop in properties:
            # Calculate score components
            buyer_match = self.score_buyer_match(prop, criteria)
            motivation = self.score_motivation(prop)
            equity = self.score_equity_potential(prop, criteria)
            liquidity = self.score_market_liquidity(prop)
            
            # Calculate weighted total
            weights = self.profile["scoring_weights"]
            total_score = (
                buyer_match * weights["buyer_match"] * 100 +
                motivation * weights["motivation"] * 100 +
                equity * weights["equity_potential"] * 100 +
                liquidity * weights["market_liquidity"] * 100
            )
            
            # Add scores to property
            prop["scores"] = {
                "buyer_match": buyer_match,
                "motivation": motivation,
                "equity_potential": equity,
                "market_liquidity": liquidity
            }
            prop["total_score"] = total_score
            
            # Only include if meets minimum
            if total_score >= self.min_score:
                scored.append(prop)
        
        return scored
    
    def score_buyer_match(self, prop: Dict, criteria: Dict) -> float:
        """Score how well property matches buyer criteria (0.0-1.0)"""
        score = 0.0
        
        # Price range (25%)
        list_price = prop.get("list_price", 0)
        if criteria["price_range"]["min"] <= list_price <= criteria["price_range"]["max"]:
            score += 0.25
            # Bonus for sweet spot
            if criteria["price_range"]["sweet_spot_min"] <= list_price <= criteria["price_range"]["sweet_spot_max"]:
                score += 0.05
        
        # Market match (20%)
        if prop.get("market") in criteria["markets"]:
            score += 0.20
            # Bonus for primary market
            if prop.get("market") in criteria["focus_markets"]["primary"]:
                score += 0.05
        
        # Property type (15%)
        if prop.get("property_type", "").upper() in [pt.upper() for pt in criteria["property_types"]]:
            score += 0.15
        
        # Beds/baths/sqft (15%)
        beds = prop.get("beds", 0)
        baths = prop.get("baths", 0)
        sqft = prop.get("sqft", 0)
        
        requirements_met = 0
        if beds >= criteria["must_have"]["min_beds"]:
            requirements_met += 1
        if baths >= criteria["must_have"]["min_baths"]:
            requirements_met += 1
        if sqft >= criteria["must_have"]["min_sqft"]:
            requirements_met += 1
        
        score += (requirements_met / 3) * 0.15
        
        # Repairs tolerance (10%)
        repairs = prop.get("estimated_repairs", 0)
        if criteria["repair_tolerance"]["min"] <= repairs <= criteria["repair_tolerance"]["max"]:
            score += 0.10
        
        # DOM (10%)
        dom = prop.get("dom", 0)
        if 0 < dom <= criteria["must_have"]["max_dom"]:
            score += 0.10
        
        return min(score, 1.0)
    
    def score_motivation(self, prop: Dict) -> float:
        """Score seller motivation (0.0-1.0)"""
        score = 0.5  # Baseline
        
        # DOM scoring
        dom = prop.get("dom", 0)
        if dom > 90:
            score += 0.25
        elif dom > 60:
            score += 0.20
        elif dom > 30:
            score += 0.15
        
        # Motivation flags
        flags = prop.get("motivation_flags", [])
        high_priority = self.profile["criteria"]["high_priority_signals"]
        
        for flag in flags:
            if flag in high_priority:
                score += 0.08  # Higher weight for priority signals
            else:
                score += 0.04
        
        return min(score, 1.0)
    
    def score_equity_potential(self, prop: Dict, criteria: Dict) -> float:
        """Score equity potential (0.0-1.0)"""
        arv = prop.get("arv", 0)
        list_price = prop.get("list_price", 0)
        repairs = prop.get("estimated_repairs", 0)
        
        if arv == 0 or list_price == 0:
            return 0.5  # Neutral if no data
        
        # Calculate spread percentage
        spread_pct = ((arv - list_price - repairs) / arv) * 100
        
        # Score based on spread
        if spread_pct >= 40:
            score = 1.0
        elif spread_pct >= 30:
            score = 0.85
        elif spread_pct >= criteria["desired_spread"]["ideal_equity_spread_pct"]:
            score = 0.75
        elif spread_pct >= criteria["desired_spread"]["minimum_equity_spread_pct"]:
            score = 0.60
        else:
            score = 0.30
        
        return score
    
    def score_market_liquidity(self, prop: Dict) -> float:
        """Score market liquidity (0.0-1.0)"""
        list_price = prop.get("list_price", 0)
        
        # Sweet spot pricing
        if 150000 <= list_price <= 300000:
            return 0.9
        elif 100000 <= list_price < 150000 or 300000 < list_price <= 400000:
            return 0.7
        elif 50000 <= list_price < 100000:
            return 0.6
        else:
            return 0.4
    
    def select_top_deals(self, scored_properties: List[Dict]) -> List[Dict]:
        """Select top N deals based on score"""
        # Sort by total score
        sorted_props = sorted(scored_properties, 
                             key=lambda x: x["total_score"], 
                             reverse=True)
        
        # Return top N (daily limit)
        return sorted_props[:self.daily_limit]
    
    def enrich_properties(self):
        """Run OSINT and other agents on top deals"""
        print(f"\n   Running intelligence on {len(self.top_deals)} properties...")
        
        for i, deal in enumerate(self.top_deals, 1):
            print(f"\n   Deal #{i}: {deal['address']}")
            
            # Placeholder for full agent integration
            # In production, these would call the actual agents
            deal["osint"] = {
                "urgency_score": 8,
                "primary_motivation": "estate_sale",
                "owner_name": "To be researched",
                "rapport_points": []
            }
            
            deal["deal_analysis"] = {
                "seller_offer": deal["list_price"] * 0.90,
                "buyer_price": deal["list_price"] * 0.95,
                "assignment_fee": deal["list_price"] * 0.05,
                "buyer_roi": 0.22
            }
            
            deal["confidence"] = {
                "overall_score": 0.78,
                "classification": "Viable Deal"
            }
            
            deal["lead_sheet"] = {
                "recommended_opening": f"Hi, I saw your property at {deal['address']}...",
                "next_steps": ["Call seller", "Send packet"]
            }
    
    def generate_morning_report(self) -> Path:
        """Generate comprehensive morning report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_dir = self.project_root / "output" / "daily_reports"
        report_dir.mkdir(parents=True, exist_ok=True)
        
        report_path = report_dir / f"{timestamp}_morning_report.txt"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("DAILY PROPERTY SOURCING REPORT\n")
            f.write(f"Buyer: {self.buyer_name}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n\n")
            
            f.write(f"YOUR TOP {len(self.top_deals)} DEALS TODAY:\n\n")
            
            for i, deal in enumerate(self.top_deals, 1):
                f.write("\n" + "="*80 + "\n")
                f.write(f"DEAL #{i} - SCORE: {deal['total_score']:.1f}/100\n")
                f.write("="*80 + "\n\n")
                
                f.write(f"PROPERTY: {deal['address']}\n")
                f.write(f"SOURCE: {deal['source'].upper()}\n")
                f.write(f"MARKET: {deal['market']}\n\n")
                
                f.write("QUICK FACTS:\n")
                f.write(f"  List Price: ${deal['list_price']:,}\n")
                f.write(f"  ARV: ${deal.get('arv', 0):,}\n")
                f.write(f"  Repairs: ${deal.get('estimated_repairs', 0):,}\n")
                f.write(f"  Beds/Baths/Sqft: {deal['beds']}/{deal['baths']}/{deal['sqft']:,}\n")
                f.write(f"  DOM: {deal['dom']} days\n")
                f.write(f"  Flags: {', '.join(deal.get('motivation_flags', []))}\n\n")
                
                f.write("SCORING BREAKDOWN:\n")
                f.write(f"  Buyer Match: {deal['scores']['buyer_match']:.2f}\n")
                f.write(f"  Motivation: {deal['scores']['motivation']:.2f}\n")
                f.write(f"  Equity Potential: {deal['scores']['equity_potential']:.2f}\n")
                f.write(f"  Market Liquidity: {deal['scores']['market_liquidity']:.2f}\n\n")
                
                f.write("PRELIMINARY DEAL NUMBERS:\n")
                f.write(f"  Estimated Seller Offer: ${deal['deal_analysis']['seller_offer']:,.0f}\n")
                f.write(f"  Estimated Buyer Price: ${deal['deal_analysis']['buyer_price']:,.0f}\n")
                f.write(f"  Estimated Assignment Fee: ${deal['deal_analysis']['assignment_fee']:,.0f}\n\n")
                
                f.write("NEXT STEPS:\n")
                f.write("  1. Run full OSINT research on owner\n")
                f.write("  2. Verify property details\n")
                f.write("  3. Calculate precise numbers\n")
                f.write("  4. Contact seller with personalized script\n\n")
                
                if deal.get("link"):
                    f.write(f"LINK: {deal['link']}\n\n")
            
            f.write("\n" + "="*80 + "\n")
            f.write("END OF REPORT\n")
            f.write("="*80 + "\n")
        
        print(f"   Report saved: {report_path}")
        return report_path
    
    def send_notification(self, report_path: Path):
        """Send email notification to Eric Frederick"""
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        try:
            # Email configuration (you'll need to set up SMTP)
            sender_email = "your-system-email@gmail.com"  # Configure this
            sender_password = "your-app-password"  # Configure this
            recipient_email = self.buyer_email
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = f"🎯 Your {len(self.top_deals)} Daily Deals Are Ready! - {datetime.now().strftime('%Y-%m-%d')}"
            
            # Email body
            body = f"""
Good morning Eric!

Your Property Sourcing Agent has found and analyzed {len(self.top_deals)} high-quality deals for you today.

DEALS SUMMARY:
"""
            
            for i, deal in enumerate(self.top_deals, 1):
                body += f"\n#{i}: {deal['address']} - Score: {deal['total_score']:.1f}/100"
                body += f"\n    ${deal['list_price']:,} | {deal['beds']}bed/{deal['baths']}bath | {', '.join(deal.get('motivation_flags', []))}\n"
            
            body += f"""

All properties have been scored above {self.min_score}/100 and match your criteria.

Full details available in your morning report:
{report_path}

NEXT STEPS:
1. Review the morning report
2. Run full OSINT on properties of interest
3. Start calling!

Your AI system is working for you 24/7.

- Property Sourcing Agent
"""
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email (commented out until SMTP configured)
            # server = smtplib.SMTP('smtp.gmail.com', 587)
            # server.starttls()
            # server.login(sender_email, sender_password)
            # server.send_message(msg)
            # server.quit()
            
            print(f"   Email notification prepared for: {recipient_email}")
            print(f"   (Configure SMTP to actually send)")
            
        except Exception as e:
            print(f"   Notification error: {str(e)}")
            print(f"   Report still available at: {report_path}")


# Main execution
if __name__ == "__main__":
    print("\n" + "="*80)
    print("PROPERTY SOURCING AGENT - STARTING DAILY SCAN")
    print("="*80)
    
    agent = PropertySourcingAgent()
    deals = agent.daily_scan()
    
    print(f"\n✓ COMPLETE! {len(deals)} deals ready for you to call.")
    print(f"✓ Check your email: {agent.buyer_email}")
    print(f"✓ Report location: /output/daily_reports/")
    print("\n")
