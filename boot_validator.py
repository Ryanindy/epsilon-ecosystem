import os
import sys
import subprocess
from datetime import datetime

# System Configuration
RAG_PATH = "H:/"
CHROMA_PATH = "H:/.chromadb"
REQUIRED_DIRS = [
    "skills",
    "flows",
    "mcp",
    "H:/epsilon",
    "H:/legal",
    "H:/business",
    "H:/decisions"
]
REQUIRED_FILES = ["GEMINI.md", "BOOT.md"]

def check_env():
    print("STEP 1: ENVIRONMENT VERIFICATION")
    results = {}
    
    # Gemini CLI
    try:
        # Just checking if 'gemini' command exists in path
        subprocess.run(["gemini", "--version"], capture_output=True, check=True)
        print("✅ Gemini CLI: FOUND")
        results['gemini'] = True
    except:
        print("❌ Gemini CLI: NOT FOUND (ABORT)")
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
        skill_files = [f for f in os.listdir("skills") if f.endswith(".skill.md")]
    else:
        skill_files = []
        
    # Check flows
    if os.path.exists("flows"):
        flow_files = [f for f in os.listdir("flows") if f.endswith(".md")]
    else:
        flow_files = []
    
    if not missing and len(skill_files) > 0 and len(flow_files) > 0:
        print(f"✅ Found {len(skill_files)} skills, {len(flow_files)} flows")
        return True
    else:
        if missing: print(f"❌ Missing files: {missing}")
        if len(skill_files) == 0: print("❌ No .skill.md files found in skills/")
        if len(flow_files) == 0: print("❌ No .md files found in flows/")
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

def main():
    print("==========================================")
    print("EPSILON ECOSYSTEM v1.3 BOOT SEQUENCE")
    print("==========================================\n")
    
    env = check_env()
    struct = check_structure()
    ctrl = check_controls()
    rag_status = check_rag()
    
    boot_pass = all([env['gemini'], env['git'], struct, ctrl])
    
    print("\n==========================================")
    print("EPSILON ECOSYSTEM v1.3 BOOT REPORT")
    print("==========================================")
    print(f"Environment: {'PASS' if env['gemini'] and env['git'] else 'FAIL'}")
    print(f"Directory Structure: {'PASS' if struct else 'FAIL'}")
    print(f"Control Files: {'PASS' if ctrl else 'FAIL'}")
    print(f"RAG Index: {rag_status}")
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
