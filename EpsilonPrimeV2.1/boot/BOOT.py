"""
🔱 EPSILON PRIME: SOVEREIGN BOOTLOADER
Version: 2.2.1 (Sovereign Spec)
Aesthetic: Chic / Minimalist
"""

import os
import sys
import subprocess
import socket
import time
import json

# --- CONFIGURATION ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQUIRED_DIRS = [
    "skills/trinity",
    "skills/personas",
    "skills/governance",
    "skills/tools",
    "rag/core_knowledge",
    "mcp"
]

# Clinical Minimalist Colors (ANSI)
C_DIM = "\033[2;37m"
C_CYAN = "\033[0;36m"
C_EMERALD = "\033[0;32m"
C_GOLD = "\033[0;33m"
C_RED = "\033[0;31m"
C_RESET = "\033[0m"

def status_line(label, status, details=""):
    print(f"{C_DIM}├─ {C_RESET}{label:<20} {C_CYAN}[{status}]{C_RESET} {C_DIM}{details}{C_RESET}")

def check_service(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex(('localhost', port)) == 0

def boot_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"\n{C_CYAN}  ε  {C_RESET}EPSILON PRIME SOVEREIGN MAINFRAME {C_DIM}v2.2.1{C_RESET}")
    print(f"{C_DIM}  {'-'*50}{C_RESET}")

def main():
    boot_banner()
    
    # 1. CORE SYSTEM
    print(f"{C_DIM}CORE SYSTEM INTEGRITY{C_RESET}")
    missing_dirs = [d for d in REQUIRED_DIRS if not os.path.exists(os.path.join(PROJECT_ROOT, d))]
    if not missing_dirs:
        status_line("FILESYSTEM", "NOMINAL", f"{len(REQUIRED_DIRS)} Nodes Verified")
    else:
        status_line("FILESYSTEM", "CRITICAL", f"Missing: {', '.join(missing_dirs)}")
        sys.exit(1)

    # 2. THE TRINITY & SKILLS
    trinity_count = len(os.listdir(os.path.join(PROJECT_ROOT, "skills/trinity")))
    persona_count = len(os.listdir(os.path.join(PROJECT_ROOT, "skills/personas")))
    tool_count = len(os.listdir(os.path.join(PROJECT_ROOT, "skills/tools")))
    status_line("TRINITY BRAIN", "ACTIVE", f"{trinity_count} Protocols Loaded")
    status_line("PERSONA LAYER", "ONLINE", f"{persona_count} Identities Ready")
    status_line("TOOL ARSENAL", "NOMINAL", f"{tool_count} Functional Modules")

    # 3. KNOWLEDGE & RAG
    chroma_status = "ONLINE" if os.path.exists(os.path.join(PROJECT_ROOT, "rag/.chromadb")) else "MISSING"
    status_line("VECTOR ENGINE", chroma_status, "ChromaDB Sovereign Node")

    # 4. SERVICES (n8n & Bridge)
    n8n_live = check_service(5678)
    if not n8n_live:
        status_line("N8N AUTOMATION", "STARTING", "Initializing Silent Instance...")
        subprocess.Popen(['n8n', 'start'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=0x08000000)
    else:
        status_line("N8N AUTOMATION", "ONLINE", "Port 5678")

    bridge_live = check_service(5000)
    if not bridge_live:
        status_line("API BRIDGE", "STARTING", "Port 5000 | Background")
        subprocess.Popen(['python', os.path.join(PROJECT_ROOT, 'main_server.py')], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=0x08000000)
    else:
        status_line("API BRIDGE", "ONLINE", "Port 5000")

    # 5. MCP NODES
    mcp_files = [f for f in os.listdir(os.path.join(PROJECT_ROOT, "mcp")) if f.endswith(".py")]
    status_line("MCP NODES", "NOMINAL", f"{len(mcp_files)} Local Servers Found")

    # 6. MEMORY
    try:
        with open(os.path.join(PROJECT_ROOT, ".gemini/memory/00_INDEX.md"), 'r') as f:
            lines = f.readlines()
            last_session = lines[-1].strip() if lines else "None"
        status_line("EPISODIC MEMORY", "READY", f"Last: {last_session[:30]}...")
    except:
        status_line("EPISODIC MEMORY", "ERR", "Index Unreadable")

    print(f"{C_DIM}  {'-'*50}{C_RESET}")
    print(f"  {C_EMERALD}SYSTEM OPERATIONAL: FULL SOVEREIGN AUTHORITY ENGAGED{C_RESET}\n")

if __name__ == "__main__":
    main()
