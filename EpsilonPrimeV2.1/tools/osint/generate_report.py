"""
OSINT Report Generator: Aggregates findings from multiple tools.
"""
import json
import datetime
import os

def generate_report(target, findings):
    report_dir = "C:/Users/Media Server/EpsilonPrimeV2.1/output/osint_reports"
    os.makedirs(report_dir, exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join(report_dir, f"report_{target}_{timestamp}.md")
    
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(f"# OSINT COMPREHENSIVE REPORT: {target}\n")
        f.write(f"**Date:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("## EXECUTIVE SUMMARY\n")
        f.write(findings.get("summary", "No summary provided.") + "\n\n")
        
        f.write("## TOOL FINDINGS\n")
        for tool, data in findings.get("tools", {}).items():
            f.write(f"### {tool.upper()}\n")
            f.write("```\n")
            f.write(str(data))
            f.write("\n```\n\n")
            
        f.write("## WEB RESOURCES\n")
        for resource, data in findings.get("web", {}).items():
            f.write(f"### {resource}\n")
            f.write(str(data) + "\n\n")
            
        f.write("--- \n")
        f.write("**SYSTEM OPERATIONAL: OSINT MASTER REPORT GENERATED.**\n")
        
    return report_file
