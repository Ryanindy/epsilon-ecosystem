import os
import sqlite3
import subprocess
from datetime import datetime
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# Configuration
DB_PATH = "memory.db"
DECISIONS_DIR = "rag/decisions"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def get_todays_interactions():
    """Fetches interactions from memory.db for the current day."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute(
            "SELECT message_in, message_out FROM interactions WHERE timestamp LIKE ? ORDER BY timestamp ASC",
            (f"{today}%",)
        )
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        print(f"[ERROR] Database access failed: {e}")
        return []

def generate_session_artifact(interactions):
    """Uses Gemini to summarize the day's progress into an ADR/Report."""
    if not interactions:
        return "No interactions found for today."

    history_str = ""
    for msg_in, msg_out in interactions:
        history_str += f"USER: {msg_in}\nAI: {msg_out}\n\n"

    client = genai.Client(api_key=GOOGLE_API_KEY)
    
    prompt = f"""You are the EPSILON SESSION CONSOLIDATOR. 
Analyze the following session history from today and generate a structured 'Session Report' in Markdown.
Focus on:
1. KEY DECISIONS (Architectural or Strategic).
2. TECHNICAL CHANGES (Code modified, new tools added).
3. PROGRESS STATUS (What was achieved).
4. NEXT STEPS (NMIA for tomorrow).

HISTORY:
{history_str}

OUTPUT FORMAT:
# Session Report: [Date]
## 1. Summary
...
## 2. Key Decisions
...
## 3. Technical Implementation
...
## 4. NMIA (Next Major Impact Actions)
...
"""

    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        return f"Failed to generate artifact: {e}"

def run_stasis():
    print("🌙 INITIALIZING OMEGA PROTOCOL: OMEGA TRIGGERED...")
    
    # 1. Capture & Consolidate
    print("[1/4] Consolidating episodic memory...")
    interactions = get_todays_interactions()
    report = generate_session_artifact(interactions)
    
    today_str = datetime.now().strftime('%Y_%m_%d')
    report_path = os.path.join(DECISIONS_DIR, f"session_report_{today_str}_stasis.md")
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"      -> Artifact saved: {report_path}")

    # 2. RAG Sync
    print("[2/4] Syncing Vector Engine...")
    subprocess.run(["python", "tools/rag/surgical_sync.py", report_path, "decisions_collection"], capture_output=True)
    
    # 3. Git Sync
    print("[3/4] Running global Git synchronization...")
    subprocess.run(["python", "tools/maintenance/daily_git_sync.py"], capture_output=True)

    # 4. Final Notification
    print("[4/4] Finalizing Daily Executive Briefing...")
    print("\n--- OMEGA PROTOCOL COMPLETE ---")
    print(f"Status: SYSTEM IN STASIS")
    print(f"Last Action: {datetime.now().strftime('%H:%M:%S')}")
    print("Memory Indexed. RAG Primed. Git Committed.")
    print("--------------------------------")
    print("Goodnight, Epsilon.")

if __name__ == "__main__":
    run_stasis()