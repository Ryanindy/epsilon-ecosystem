import subprocess
import sys
import os
from datetime import datetime

# Configuration
# The script is in tools/maintenance/ - project root is two levels up
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
COMMIT_MSG = f"Sovereign Auto-Backup: {datetime.now().strftime('%Y-%m-%d %H:%M')} [God Mode]"

def run_command(command_list, cwd=PROJECT_ROOT):
    try:
        result = subprocess.run(
            command_list, 
            cwd=cwd, 
            shell=False, 
            check=True, 
            text=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        print(f"SUCCESS: {' '.join(command_list)}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {' '.join(command_list)}\n{e.stderr}")
        return False

def sync_repo():
    print(f"--- Starting Epsilon Prime Sync [Root: {PROJECT_ROOT}] ---")
    
    # 1. Sync Skills and Update RAG
    print("Step 1: Synchronizing Skills and RAG Index...")
    skill_sync_script = os.path.join(PROJECT_ROOT, "tools", "maintenance", "skill_sync.py")
    run_command([sys.executable, skill_sync_script])
    
    # 2. Git Operations
    # Check for changes
    status = subprocess.run(["git", "status", "--porcelain"], cwd=PROJECT_ROOT, shell=False, capture_output=True, text=True)
    if not status.stdout.strip():
        print("No changes to commit. Ecosystem is static.")
        return

    print("Step 2: Staging changes...")
    run_command(["git", "add", "."])
    
    print("Step 3: Committing...")
    run_command(["git", "commit", "-m", COMMIT_MSG])
    
    print("Step 4: Pushing to remote...")
    # Using 'origin main' to match current remote config
    if run_command(["git", "push", "origin", "main"]):
        print("--- Sync Complete: Epsilon Prime is Sovereign ---")
    else:
        print("--- Push failed: Remote rejection or network failure ---")

if __name__ == "__main__":
    sync_repo()
