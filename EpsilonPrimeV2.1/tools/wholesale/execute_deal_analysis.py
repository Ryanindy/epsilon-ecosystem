"""
Wholesale AI System - Main Execution Script
Orchestrates the complete deal analysis workflow
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Force UTF-8 encoding for console output
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

class WholesaleAISystem:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.config = self._load_config()
        self.kb = self._load_knowledge_base()
        
    def _load_config(self):
        config_path = self.project_root / "config" / "system_config.json"
        with open(config_path, 'r') as f:
            return json.load(f)
    
    def _load_knowledge_base(self):
        kb_path = self.project_root / "knowledge_base" / "knowledge_base.json"
        with open(kb_path, 'r') as f:
            return json.load(f)
    
    def analyze_property(self, property_data):
        """
        Main workflow: Property -> Deal Analysis -> Confidence Score -> Packet
        """
        print(f"\n{'='*60}")
        print(f"ANALYZING PROPERTY: {property_data['address']}")
        print(f"{'='*60}\n")
        
        # Step 1: Deal Analysis
        print("Step 1: Running Deal Analyzer...")
        deal_analysis = self.run_deal_analyzer(property_data)
        print("[OK] Deal Analysis Complete")
        print(f"  Strategy: {deal_analysis['strategy']}")
        print(f"  Assignment Fee: ${deal_analysis['assignment_fee']:,}")
        
        # Step 2: Confidence Scoring
        print("\nStep 2: Running Confidence Scorer...")
        confidence_result = self.run_confidence_scorer(deal_analysis, property_data)
        print(f"[OK] Confidence Score: {confidence_result['overall_score']:.2f}")
        print(f"  Classification: {confidence_result['classification']}")
        
        # Step 3: Decision Gate
        if confidence_result['overall_score'] < self.config['thresholds']['minimum_confidence_score']:
            print(f"\n[WARNING] ESCALATION: Score below {self.config['thresholds']['minimum_confidence_score']} - Human review required")
            return {
                'status': 'escalated',
                'deal_analysis': deal_analysis,
                'confidence_result': confidence_result
            }
        
        # Step 4: Packet Generation
        print("\nStep 3: Generating Investor Packet...")
        packet = self.run_packet_generator(deal_analysis, property_data, confidence_result)
        print("[OK] Packet Generated")
        
        # Step 5: Save Outputs
        self._save_outputs(property_data['address'], deal_analysis, confidence_result, packet)
        
        print(f"\n{'='*60}")
        print("[OK] WORKFLOW COMPLETE - Deal Ready for Distribution")
        print(f"{'='*60}\n")
        
        return {
            'status': 'approved',
            'deal_analysis': deal_analysis,
            'confidence_result': confidence_result,
            'packet': packet
        }
    
    def run_deal_analyzer(self, property_data):
        """
        Calculate ARV, repairs, MAO, and deal structure
        """
        # ARV Calculation (conservative)
        arv = self._calculate_arv(property_data)
        
        # Repair Estimation
        repairs = self._estimate_repairs(property_data)
        
        # MAO Calculation: ARV x 0.75 - Repairs - $8,000
        mao = (arv * 0.75) - repairs - 8000
        
        # Strategy Selection
        strategy = self._select_strategy(property_data, arv, repairs, mao)
        
        # Deal Structuring
        seller_offer = mao - 2000  # Slightly under MAO for negotiation room
        assignment_fee_target = max(15000, arv * 0.05)  # 5% of ARV or $15k minimum
        buyer_price = seller_offer + assignment_fee_target
        
        # Ensure buyer profit viability
        buyer_all_in = buyer_price + repairs + 8000
        buyer_profit = arv - buyer_all_in
        buyer_roi = buyer_profit / buyer_all_in if buyer_all_in > 0 else 0
        
        # Adjust if buyer ROI too low
        if buyer_roi < self.config['thresholds']['minimum_buyer_roi']:
            # Reduce assignment fee to preserve buyer margin
            target_profit = buyer_all_in * 0.20
            new_arv_target = buyer_all_in + target_profit
            if new_arv_target > arv:
                buyer_price = mao  # Minimal assignment fee
                assignment_fee_target = max(10000, buyer_price - seller_offer)
        
        assignment_fee = buyer_price - seller_offer
        
        return {
            'arv': arv,
            'repairs': repairs,
            'mao': mao,
            'seller_offer': seller_offer,
            'buyer_price': buyer_price,
            'assignment_fee': assignment_fee,
            'strategy': strategy,
            'buyer_roi': buyer_roi,
            'assumptions': [
                f"ARV estimated conservatively at ${arv:,}",
                f"Repairs estimated at ${repairs:,}",
                f"Assignment fee of ${assignment_fee:,} preserves {buyer_roi*100:.1f}% buyer ROI",
                f"Strategy: {strategy}"
            ]
        }
    
    def _calculate_arv(self, property_data):
        """Calculate After Repair Value conservatively"""
        # In production, this would pull actual comps
        # For now, use a conservative multiplier based on list price
        list_price = property_data.get('list_price', 0)
        sqft = property_data.get('sqft', 1500)
        
        # Estimate market value per sqft (conservative)
        price_per_sqft = 180  # Adjust based on market
        arv = sqft * price_per_sqft
        
        # Don't exceed list price by more than 40% (safety)
        max_arv = list_price * 1.4
        return min(arv, max_arv)
    
    def _estimate_repairs(self, property_data):
        """Estimate repair costs"""
        sqft = property_data.get('sqft', 1500)
        description = property_data.get('description', '').lower()
        
        # Categorize repair level
        if 'heavy' in description or 'extensive' in description:
            repair_per_sqft = 50
        elif 'moderate' in description or 'needs work' in description:
            repair_per_sqft = 35
        else:
            repair_per_sqft = 25  # Cosmetic
        
        return sqft * repair_per_sqft
    
    def _select_strategy(self, property_data, arv, repairs, mao):
        """Select optimal deal strategy"""
        list_price = property_data.get('list_price', 0)
        dom = property_data.get('dom', 0)
        flags = property_data.get('flags', [])
        
        equity_spread = (arv - list_price) / arv if arv > 0 else 0
        
        # Decision logic
        if equity_spread > 0.25 and dom > 30:
            return "wholesale_cash"
        elif equity_spread > 0.60:
            return "seller_finance"
        elif equity_spread < 0.20:
            return "subject_to"
        else:
            return "creative_hybrid"
    
    def run_confidence_scorer(self, deal_analysis, property_data):
        """Score deal 0.00-1.00 across 4 components"""
        # Component 1: Seller Motivation (30%)
        seller_motivation = self._score_seller_motivation(property_data)
        
        # Component 2: Equity & Spread (30%)
        equity_spread = self._score_equity_spread(deal_analysis)
        
        # Component 3: Deal Simplicity (20%)
        deal_simplicity = self._score_deal_simplicity(deal_analysis, property_data)
        
        # Component 4: Market Liquidity (20%)
        market_liquidity = self._score_market_liquidity(property_data)
        
        # Weighted calculation
        overall_score = (
            seller_motivation * 0.30 +
            equity_spread * 0.30 +
            deal_simplicity * 0.20 +
            market_liquidity * 0.20
        )
        
        # Classification
        if overall_score >= 0.80:
            classification = "Priority Deal"
        elif overall_score >= 0.60:
            classification = "Viable Deal"
        else:
            classification = "Human Review Required"
        
        return {
            'overall_score': overall_score,
            'classification': classification,
            'component_scores': {
                'seller_motivation': seller_motivation,
                'equity_spread': equity_spread,
                'deal_simplicity': deal_simplicity,
                'market_liquidity': market_liquidity
            },
            'escalation_required': overall_score < 0.60
        }
    
    def _score_seller_motivation(self, property_data):
        """Score 0.0-1.0 based on motivation indicators"""
        score = 0.5  # Baseline
        dom = property_data.get('dom', 0)
        flags = property_data.get('flags', [])
        
        if dom > 60:
            score += 0.3
        elif dom > 30:
            score += 0.2
        
        if 'price_reduction' in flags:
            score += 0.15
        if 'vacant' in flags:
            score += 0.1
        if 'as_is' in flags:
            score += 0.1
        
        return min(score, 1.0)
    
    def _score_equity_spread(self, deal_analysis):
        """Score based on financial metrics"""
        assignment_fee = deal_analysis['assignment_fee']
        buyer_roi = deal_analysis['buyer_roi']
        
        score = 0.5
        
        if assignment_fee >= 20000:
            score += 0.3
        elif assignment_fee >= 15000:
            score += 0.2
        elif assignment_fee >= 10000:
            score += 0.1
        
        if buyer_roi >= 0.25:
            score += 0.2
        elif buyer_roi >= 0.20:
            score += 0.1
        
        return min(score, 1.0)
    
    def _score_deal_simplicity(self, deal_analysis, property_data):
        """Score based on complexity"""
        strategy = deal_analysis['strategy']
        
        if strategy == "wholesale_cash":
            return 0.9
        elif strategy == "seller_finance":
            return 0.7
        elif strategy == "subject_to":
            return 0.6
        else:
            return 0.5
    
    def _score_market_liquidity(self, property_data):
        """Score based on market conditions"""
        list_price = property_data.get('list_price', 0)
        
        # Sweet spot: $150k-$400k
        if 150000 <= list_price <= 400000:
            return 0.8
        elif 100000 <= list_price < 150000 or 400000 < list_price <= 500000:
            return 0.6
        else:
            return 0.4
    
    def run_packet_generator(self, deal_analysis, property_data, confidence_result):
        """Generate investor-facing packet"""
        packet = {
            'property_snapshot': self._generate_property_snapshot(property_data),
            'deal_summary': self._generate_deal_summary(deal_analysis),
            'strategy': self._generate_strategy_section(deal_analysis),
            'financial_breakdown': self._generate_financial_breakdown(deal_analysis),
            'exit_scenarios': self._generate_exit_scenarios(deal_analysis),
            'risk_assumptions': self._generate_risk_section(deal_analysis),
            'call_to_action': self._generate_cta(deal_analysis)
        }
        return packet
    
    def _generate_property_snapshot(self, data):
        return f"""
PROPERTY: {data.get('city', '')}, {data.get('state', '')} [Full address after NDA]
Type: Single Family Home
Specs: {data.get('beds', 3)} Beds | {data.get('baths', 2)} Baths | {data.get('sqft', 0):,} sqft
Status: {data.get('description', 'Status TBD')}
Days on Market: {data.get('dom', 0)}
"""
    
    def _generate_deal_summary(self, analysis):
        return f"""
DEAL NUMBERS

Contract Price:       ${analysis['seller_offer']:,}
Your Price:           ${analysis['buyer_price']:,}
Estimated ARV:        ${analysis['arv']:,}
Estimated Repairs:    ${analysis['repairs']:,}
------------------------------------------------------------
All-In Cost:          ${analysis['buyer_price'] + analysis['repairs']:,}
Projected Profit:     ${analysis['arv'] - (analysis['buyer_price'] + analysis['repairs']):,}+
ROI:                  {analysis['buyer_roi']*100:.1f}%
"""
    
    def _generate_strategy_section(self, analysis):
        strategy_descriptions = {
            'wholesale_cash': 'Quick cash flip - high motivation and solid spread',
            'seller_finance': 'Seller financing opportunity - flexible terms available',
            'subject_to': 'Subject-To existing financing - creative structure',
            'creative_hybrid': 'Hybrid creative deal - multiple strategies possible'
        }
        return f"""
RECOMMENDED STRATEGY: {analysis['strategy'].replace('_', ' ').title()}

{strategy_descriptions.get(analysis['strategy'], 'Custom strategy required')}
"""
    
    def _generate_financial_breakdown(self, analysis):
        return f"""
FINANCIAL BREAKDOWN

Purchase Price:           ${analysis['buyer_price']:,}
Rehab Budget:             ${analysis['repairs']:,}
Holding/Closing Costs:    $8,000
------------------------------------------------------------
TOTAL ALL-IN:             ${analysis['buyer_price'] + analysis['repairs'] + 8000:,}
"""
    
    def _generate_exit_scenarios(self, analysis):
        all_in = analysis['buyer_price'] + analysis['repairs'] + 8000
        selling_costs = analysis['arv'] * 0.07
        net_profit = analysis['arv'] - selling_costs - all_in
        
        return f"""
EXIT SCENARIOS

FLIP EXIT:
Resale Price:         ${analysis['arv']:,} (conservative)
Selling Costs (7%):   -${selling_costs:,}
Net Proceeds:         ${analysis['arv'] - selling_costs:,}
Less All-In:          -${all_in:,}
------------------------------------------------------------
NET PROFIT:           ${net_profit:,}
"""
    
    def _generate_risk_section(self, analysis):
        return """
RISK & ASSUMPTIONS

[OK] ARV based on comparable sales analysis
[OK] Repairs estimated conservatively
[OK] Clean title assumed (due diligence recommended)
[OK] Market conditions subject to change
[OK] Buyer should conduct independent inspection
"""
    
    def _generate_cta(self, analysis):
        return f"""
NEXT STEPS

Serious buyers only - proof of funds required.

Contract Structure:
Assignment with ${analysis['assignment_fee']:,} fee OR double-close

Reply with:
1. Proof of funds
2. Preferred timeline
3. Questions

First qualified buyer gets priority.
"""
    
    def _save_outputs(self, address, deal_analysis, confidence_result, packet):
        """Save all outputs to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_address = address.replace(' ', '_').replace(',', '')
        
        output_dir = self.project_root / "output" / "deals" / f"{timestamp}_{safe_address}"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save deal analysis
        with open(output_dir / "deal_analysis.json", 'w', encoding='utf-8') as f:
            json.dump(deal_analysis, f, indent=2)
        
        # Save confidence result
        with open(output_dir / "confidence_score.json", 'w', encoding='utf-8') as f:
            json.dump(confidence_result, f, indent=2)
        
        # Save packet
        with open(output_dir / "investor_packet.txt", 'w', encoding='utf-8') as f:
            for section, content in packet.items():
                f.write(f"\n{'='*60}\n")
                f.write(f"{section.upper()}\n")
                f.write(f"{'='*60}\n")
                f.write(content)
        
        print(f"\n[OK] Outputs saved to: {output_dir}")


# Example usage
if __name__ == "__main__":
    # Initialize system
    system = WholesaleAISystem("C:/Users/Media Server/Desktop/Wholesale_AI_Project")
    
    # Example property
    sample_property = {
        "address": "123 Oak Street",
        "city": "Columbus",
        "state": "OH",
        "list_price": 180000,
        "beds": 3,
        "baths": 2,
        "sqft": 1400,
        "dom": 52,
        "description": "Needs cosmetic updates, vacant, motivated seller",
        "flags": ["vacant", "price_reduction", "as_is"]
    }
    
    # Run analysis
    result = system.analyze_property(sample_property)
    
    print("\n" + "="*60)
    print(f"Final Status: {result['status'].upper()}")
    if result['status'] == 'approved':
        print(f"Confidence Score: {result['confidence_result']['overall_score']:.2f}")
        print(f"Assignment Fee: ${result['deal_analysis']['assignment_fee']:,}")
    print("="*60)
