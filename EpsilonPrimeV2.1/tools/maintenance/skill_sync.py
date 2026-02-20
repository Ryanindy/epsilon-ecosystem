import os
import shutil
import subprocess
import sys
import hashlib

# Configuration
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SOURCE_DIR = os.path.join(PROJECT_ROOT, "skills")
DEST_DIR = os.path.join(PROJECT_ROOT, ".gemini", "skills")
RAG_INGEST_SCRIPT = os.path.join(PROJECT_ROOT, "tools", "rag", "ingest.py")

def get_file_hash(path):
    with open(path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def sync_skills():
    print("🔄 [SKILL_SYNC] Synchronizing Global Skill Framework...")
    
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)

    synced_count = 0
    
    # 1. Crawl and Sync
    for root, dirs, files in os.walk(SOURCE_DIR):
        for file in files:
            if file.endswith(".md"):
                source_path = os.path.join(root, file)
                dest_path = os.path.join(DEST_DIR, file)
                
                # Copy if missing or changed
                if not os.path.exists(dest_path) or get_file_hash(source_path) != get_file_hash(dest_path):
                    shutil.copy2(source_path, dest_path)
                    synced_count += 1
                    print(f"  [+] Synced: {file}")

    print(f"✅ [SKILL_SYNC] Synced {synced_count} new/updated modules.")

    # 2. Trigger RAG Ingestion
    print("🧠 [SKILL_SYNC] Re-indexing RAG Context...")
    try:
        subprocess.run([
            sys.executable, 
            RAG_INGEST_SCRIPT, 
            "--source", SOURCE_DIR, 
            "--collection", "epsilon"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ [SKILL_SYNC] RAG Index Updated.")
    except Exception as e:
        print(f"❌ [SKILL_SYNC] RAG Ingestion failed: {e}")

if __name__ == "__main__":
    sync_skills()
