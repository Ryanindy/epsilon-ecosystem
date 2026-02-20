# HARDENED BOOTLOADER V3.0
# "Solenya" Protocol - Fast, Aggressive, Clean.

import os
import sys
import subprocess
import time
import shutil

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCK_FILES = [".gemini/GOD_MODE_ACTIVE", ".lock"]

def clean_locks():
    print("[BOOT] Cleaning stale locks...")
    for lock in LOCK_FILES:
        path = os.path.join(PROJECT_ROOT, lock)
        if os.path.exists(path):
            try:
                os.remove(path)
                print(f"  - Removed {lock}")
            except Exception as e:
                print(f"  - Failed to remove {lock}: {e}")

def check_pnpm():
    print("[BOOT] Verifying Workspace (pnpm)...")
    if not os.path.exists(os.path.join(PROJECT_ROOT, "pnpm-lock.yaml")):
        print("  - CRITICAL: pnpm-lock.yaml missing. Workspace corrupted.")
        return False
    return True

def start_services():
    print("[BOOT] Igniting Services...")
    
    # 1. API Bridge
    print("  - Launching API Bridge (Port 5000)...")
    subprocess.Popen(["python", "main_server.py"], cwd=PROJECT_ROOT, 
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                     creationflags=subprocess.CREATE_NEW_CONSOLE)
    
    # 2. n8n (if not running)
    # Check port 5678 logic here if needed, or assume n8n auto-starts
    
    # 3. OpenClaw Gateway
    print("  - Launching OpenClaw Gateway...")
    gateway_cmd = os.path.join(os.path.expanduser("~"), ".openclaw", "gateway.cmd")
    if os.path.exists(gateway_cmd):
        subprocess.Popen([gateway_cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                         creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        print("  - WARN: OpenClaw gateway not found.")

def main():
    print("🔱 EPSILON PRIME V3.0 BOOT SEQUENCE")
    clean_locks()
    
    if not check_pnpm():
        print("  - BOOT ABORTED: Dependency failure.")
        sys.exit(1)
        
    start_services()
    print("[BOOT] SEQUENCE COMPLETE. SYSTEM IS LIVE.")

if __name__ == "__main__":
    main()
