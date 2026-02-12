import os
import sys
import subprocess
import socket
import time
from datetime import datetime

# System Configuration (Updated for Epsilon Prime v2.1)
RAG_PATH = "rag"
CHROMA_PATH = "rag/.chromadb"
REQUIRED_DIRS = [
    "skills",
    "rag/core_knowledge/epsilon",
    "tools/rag",
    "boot"
]
REQUIRED_FILES = ["GEMINI.md", "BOOT.md", "main_server.py", "sms_handler.py"]

def check_env():
    print("STEP 1: ENVIRONMENT VERIFICATION")
    results = {}
    
    # Epsilon CLI (Check for the batch wrapper or main script)
    if os.path.exists("epsilon.bat") or os.path.exists("main_server.py"):
        print("✅ Epsilon CLI: FOUND")
        results['gemini'] = True
    else:
        print("❌ Epsilon CLI: NOT FOUND (ABORT)")
        results['gemini'] = False

    # Git
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
        print("✅ Git: FOUND")
        results['git'] = True
    except:
        print("❌ Git: NOT FOUND (ABORT)")
        results['git'] = False

    # Python & ChromaDB
    try:
        import chromadb
        print(f"✅ Python & ChromaDB: FOUND ({chromadb.__version__})")
        results['chroma'] = True
    except ImportError:
        print("⚠️ ChromaDB: NOT INSTALLED (DEGRADED MODE)")
        results['chroma'] = False
        
    return results

def check_structure():
    print("\nSTEP 2: DIRECTORY INTEGRITY CHECK")
    missing = [d for d in REQUIRED_DIRS if not os.path.exists(d)]
    if not missing:
        print("✅ Directory structure valid")
        return True
    else:
        print(f"❌ Missing directories: {missing}")
        return False

def check_controls():
    print("\nSTEP 3: CONTROL FILE VALIDATION")
    missing = [f for f in REQUIRED_FILES if not os.path.exists(f)]
    
    # Check skills
    if os.path.exists("skills"):
        skill_files = [f for f in os.listdir("skills") if f.endswith(".skill.md") or f.endswith(".md")]
    else:
        skill_files = []
    
    if not missing and len(skill_files) > 0:
        print(f"✅ Found {len(skill_files)} skills/protocols")
        return True
    else:
        if missing: print(f"❌ Missing files: {missing}")
        if len(skill_files) == 0: print("❌ No skill files found in skills/")
        return False

def check_rag():
    print("\nSTEP 4: RAG INDEX STATUS CHECK")
    if not os.path.exists(CHROMA_PATH):
        print("⚠️ ChromaDB index directory not found (DEGRADED)")
        return "DEGRADED"
        
    try:
        import chromadb
        client = chromadb.PersistentClient(path=CHROMA_PATH)
        collections = client.list_collections()
        if len(collections) > 0:
            print(f"✅ Found {len(collections)} RAG collection(s)")
            return "PASS"
        else:
            print("⚠️ No ChromaDB collections found (DEGRADED)")
            return "DEGRADED"
    except Exception as e:
        print(f"⚠️ RAG check failed: {str(e)} (DEGRADED)")
        return "DEGRADED"

def check_n8n():
    print("\nSTEP 5: AUTOMATION SERVICE (n8n) CHECK")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # n8n might be on 5678 or 5000 (Flask)
    result = sock.connect_ex(('localhost', 5678))
    sock.close()
    
    if result == 0:
        print("✅ n8n Service: ONLINE (Port 5678)")
        return "ONLINE"
    else:
        print("⚠️ n8n Service: OFFLINE (Skipping startup in validator)")
        return "OFFLINE"

def main():
    print("==========================================")
    print("EPSILON PRIME v2.1 BOOT SEQUENCE")
    print("==========================================\n")
    
    env = check_env()
    struct = check_structure()
    ctrl = check_controls()
    rag_status = check_rag()
    n8n_status = check_n8n()
    
    boot_pass = all([env['gemini'], env['git'], struct, ctrl])
    
    print("\n==========================================")
    print("EPSILON PRIME v2.1 BOOT REPORT")
    print("==========================================")
    print(f"Environment: {'PASS' if env['gemini'] and env['git'] else 'FAIL'}")
    print(f"Directory Structure: {'PASS' if struct else 'FAIL'}")
    print(f"Control Files: {'PASS' if ctrl else 'FAIL'}")
    print(f"RAG Index: {rag_status}")
    print(f"n8n Service: {n8n_status}")
    print("------------------------------------------")
    
    if boot_pass:
        status = "PASS" if rag_status == "PASS" else "DEGRADED"
        print(f"BOOT STATUS: {status}")
        print(f"OPERATIONAL MODE: {'Full Authority' if status == 'PASS' else 'Non-High-Risk Only'}")
        print(f"CONFIDENCE CAP: {'None' if status == 'PASS' else '69'}")
    else:
        print("BOOT STATUS: FAIL")
        print("OPERATIONAL MODE: Advisory Only")
    
    print("==========================================")
    
    if not boot_pass:
        sys.exit(1)

if __name__ == "__main__":
    main()