"""
EPSILON PRIME: SOVEREIGN BOOTLOADER
Version: 2.3.0 (Hardened Boot Sequence)
"""

import os
import sys
import subprocess
import socket
import time
import logging

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

# Service configuration
SERVICE_STARTUP_TIMEOUT = 30  # seconds
SERVICE_CHECK_INTERVAL = 1   # seconds

# Clinical Minimalist Colors (ANSI)
C_DIM = "\033[2;37m"
C_CYAN = "\033[0;36m"
C_EMERALD = "\033[0;32m"
C_GOLD = "\033[0;33m"
C_RED = "\033[0;31m"
C_RESET = "\033[0m"

# --- LOGGING ---
logging.basicConfig(level=logging.INFO, format='[BOOT] %(message)s')
logger = logging.getLogger("EpsilonBoot")

def status_line(label, status, details=""):
    color = C_EMERALD if status in ["NOMINAL", "ONLINE", "ACTIVE", "READY"] else C_GOLD if status == "STARTING" else C_RED
    print(f"{C_DIM}├─ {C_RESET}{label:<20} {color}[{status}]{C_RESET} {C_DIM}{details}{C_RESET}")

def check_service(port: int) -> bool:
    """Check if a service is listening on a port."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            return s.connect_ex(('localhost', port)) == 0
    except Exception:
        return False

def wait_for_service(port: int, name: str, timeout: int = SERVICE_STARTUP_TIMEOUT) -> bool:
    """Wait for a service to become available."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        if check_service(port):
            return True
        time.sleep(SERVICE_CHECK_INTERVAL)
    logger.warning(f"{name} failed to start within {timeout}s")
    return False

def boot_banner():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    print(f"\n{C_CYAN}  ε  {C_RESET}EPSILON PRIME SOVEREIGN MAINFRAME {C_DIM}v2.3.0{C_RESET}")
    print(f"{C_DIM}  {'-'*50}{C_RESET}")

def main():
    boot_banner()

    # 1. CORE SYSTEM INTEGRITY
    print(f"{C_DIM}CORE SYSTEM INTEGRITY{C_RESET}")
    missing_dirs = []
    for d in REQUIRED_DIRS:
        full_path = os.path.join(PROJECT_ROOT, d)
        if not os.path.exists(full_path):
            missing_dirs.append(d)

    if not missing_dirs:
        status_line("FILESYSTEM", "NOMINAL", f"{len(REQUIRED_DIRS)} Nodes Verified")
    else:
        status_line("FILESYSTEM", "WARN", f"Missing: {', '.join(missing_dirs)}")
        logger.warning(f"Creating missing directories: {missing_dirs}")
        for d in missing_dirs:
            os.makedirs(os.path.join(PROJECT_ROOT, d), exist_ok=True)

    # 2. THE TRINITY & SKILLS
    status_line("SKILL FRAMEWORK", "SYNCING", "Re-indexing arsenal...")
    subprocess.run([sys.executable, os.path.join(PROJECT_ROOT, "tools/maintenance/skill_sync.py")], 
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    trinity_path = os.path.join(PROJECT_ROOT, "skills/trinity")
    persona_path = os.path.join(PROJECT_ROOT, "skills/personas")
    tool_path = os.path.join(PROJECT_ROOT, "skills/tools")

    trinity_count = len(os.listdir(trinity_path)) if os.path.exists(trinity_path) else 0
    persona_count = len(os.listdir(persona_path)) if os.path.exists(persona_path) else 0
    tool_count = len(os.listdir(tool_path)) if os.path.exists(tool_path) else 0

    status_line("TRINITY BRAIN", "ACTIVE", f"{trinity_count} Protocols Loaded")
    status_line("PERSONA LAYER", "ONLINE", f"{persona_count} Identities Ready")
    status_line("TOOL ARSENAL", "NOMINAL", f"{tool_count} Functional Modules")

    # 3. KNOWLEDGE & RAG
    chroma_path = os.path.join(PROJECT_ROOT, "rag", ".chromadb")
    chroma_status = "ONLINE" if os.path.exists(chroma_path) else "MISSING"
    status_line("VECTOR ENGINE", chroma_status, "ChromaDB Sovereign Node")
    
    if chroma_status == "ONLINE":
        status_line("VECTOR ENGINE", "WARMUP", "Paging to RAM...")
        subprocess.run([sys.executable, os.path.join(PROJECT_ROOT, "tools/rag/warmup.py")], 
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        status_line("VECTOR ENGINE", "READY", "Indices Cached")

    # 4. SERVICES (n8n & Bridge) - WITH PROPER WAIT
    n8n_live = check_service(5678)
    if not n8n_live:
        status_line("N8N AUTOMATION", "STARTING", "Initializing...")
        try:
            # Windows-specific: CREATE_NO_WINDOW flag and shell=True for n8n.cmd
            creation_flags = 0x08000000 if os.name == 'nt' else 0
            subprocess.Popen(
                ['n8n', 'start'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=creation_flags,
                shell=True # Required on Windows to find n8n.cmd/n8n.ps1
            )
            # Wait for n8n to actually start
            if wait_for_service(5678, "n8n", timeout=15):
                status_line("N8N AUTOMATION", "ONLINE", "Port 5678")
            else:
                status_line("N8N AUTOMATION", "TIMEOUT", "Port 5678 not responding")
        except Exception as e:
            status_line("N8N AUTOMATION", "ERR", f"{str(e)[:20]}")
    else:
        status_line("N8N AUTOMATION", "ONLINE", "Port 5678")

    bridge_live = check_service(5000)
    if not bridge_live:
        status_line("API BRIDGE", "STARTING", "Port 5000 | Background")
        try:
            creation_flags = 0x08000000 if os.name == 'nt' else 0
            subprocess.Popen(
                ['python', os.path.join(PROJECT_ROOT, 'main_server.py')],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=creation_flags
            )
            # Wait for bridge to actually start
            if wait_for_service(5000, "API Bridge", timeout=10):
                status_line("API BRIDGE", "ONLINE", "Port 5000")
            else:
                status_line("API BRIDGE", "TIMEOUT", "Port 5000 not responding")
        except Exception as e:
            status_line("API BRIDGE", "ERR", str(e)[:30])
    else:
        status_line("API BRIDGE", "ONLINE", "Port 5000")

    # 5. MCP NODES
    mcp_path = os.path.join(PROJECT_ROOT, "mcp")
    if os.path.exists(mcp_path):
        mcp_files = [f for f in os.listdir(mcp_path) if f.endswith(".py")]
        status_line("MCP NODES", "NOMINAL", f"{len(mcp_files)} Local Servers Found")
    else:
        status_line("MCP NODES", "MISSING", "No MCP directory")

    # 6. MEMORY
    memory_index = os.path.join(PROJECT_ROOT, ".gemini", "memory", "00_INDEX.md")
    try:
        if os.path.exists(memory_index):
            with open(memory_index, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                last_session = lines[-1].strip() if lines else "None"
            status_line("EPISODIC MEMORY", "READY", f"Last: {last_session[:30]}...")
        else:
            status_line("EPISODIC MEMORY", "EMPTY", "No sessions recorded")
    except Exception as e:
        status_line("EPISODIC MEMORY", "ERR", f"Index error: {str(e)[:20]}")

    print(f"{C_DIM}  {'-'*50}{C_RESET}")
    print(f"  {C_EMERALD}SYSTEM OPERATIONAL: FULL SOVEREIGN AUTHORITY ENGAGED{C_RESET}\n")

if __name__ == "__main__":
    main()
