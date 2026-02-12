import subprocess
import sys
import os
from datetime import datetime

# Configuration
REPO_DIR = os.path.dirname(os.path.abspath(__file__))
COMMIT_MSG = f"Auto-update: {datetime.now().strftime('%Y-%m-%d %H:%M')}"

def run_command(command):
    try:
        result = subprocess.run(
            command, 
            cwd=REPO_DIR, 
            shell=True, 
            check=True, 
            text=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        print(f"SUCCESS: {command}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {command}\n{e.stderr}")
        return False

def sync_repo():
    print("--- Starting Epsilon Prime Sync ---")
    
    # 1. Generate RAG Index
    print("Step 1: Updating RAG Index...")
    run_command("python generate_rag_index.py")
    
    # 2. Git Add
    print("Step 2: Staging files...")
    run_command("git add .")
    
    # 3. Git Commit
    print("Step 3: Committing...")
    # Check if there are changes first
    status = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    if not status.stdout.strip():
        print("No changes to commit.")
    else:
        run_command(f'git commit -m "{COMMIT_MSG}"')
    
    # 4. Git Push
    print("Step 4: Pushing to remote...")
    if run_command("git push origin main"):
        print("Sync Complete!")
    else:
        print("Push failed. Check remote configuration.")

if __name__ == "__main__":
    sync_repo()
