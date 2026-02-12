import os
import datetime
import glob
import requests
import json

# Configuration
LOG_DIR = r"H:\decisions"
OUTPUT_DIR = r"C:\Users\Media Server\Desktop\Daily_Briefings"
N8N_WEBHOOK_URL = "http://localhost:5678/webhook/daily-briefing" # Placeholder

def get_latest_log():
    files = glob.glob(os.path.join(LOG_DIR, "session_history_*.md"))
    if not files:
        return None
    return max(files, key=os.path.getctime)

def generate_report():
    log_file = get_latest_log()
    if not log_file:
        return "No session logs found.", []

    with open(log_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Simple parsing to extract highlights (Lines starting with -)
    highlights = [line.strip() for line in content.split('\n') if line.strip().startswith('- **')]
    
    # Generate Daily Report Markdown
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    report_filename = f"Daily_Briefing_{today}.md"
    report_path = os.path.join(OUTPUT_DIR, report_filename)
    
    report_content = f"""# 📅 DAILY EXECUTIVE BRIEFING
**Date**: {today}
**Status**: GENERATED

---

## 🚀 HIGHLIGHTS
{chr(10).join(highlights[:5])}

## 📋 DETAILED LOG
*(Derived from {os.path.basename(log_file)})*

{content}

---
**Priorities for Tomorrow**:
1. Review field test results of GhostPlate.
2. Check sales funnel traffic.
3. Verify RAG ingestion of new engineering data.
"""
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)
        
    print(f"Report saved to: {report_path}")
    return report_content, highlights

def send_notifications(report_body, highlights):
    # Prepare payload for n8n
    payload = {
        "date": datetime.datetime.now().strftime('%Y-%m-%d'),
        "recipient_email": "ryan.keeton00@gmail.com",
        "recipient_phone": "+12535487767",
        "email_body": report_body,
        "sms_message": "DAILY BRIEFING:\n" + "\n".join(highlights[:3]) + "\n\nCheck email for full report."
    }
    
    try:
        # We use the native n8n webhook
        # Note: You need to activate the workflow in n8n first!
        response = requests.post(N8N_WEBHOOK_URL, json=payload)
        if response.status_code == 200:
            print("✅ Notifications sent via n8n.")
        else:
            print(f"❌ Failed to send notifications: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Connection Error (n8n might be down): {e}")

if __name__ == "__main__":
    print("Generating Daily Briefing...")
    report, hits = generate_report()
    if hits:
        send_notifications(report, hits)
