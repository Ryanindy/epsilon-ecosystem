# BOOT.md — Epsilon Ecosystem Boot Sequence

## PURPOSE

Ensure the system cannot operate unless architecture, controls, and knowledge integrity are verified.

---

## BOOT OBJECTIVES

1. Verify environment prerequisites
2. Validate directory structure
3. Confirm control file integrity
4. Check RAG index health
5. Declare operational status

---

## STEP 1: ENVIRONMENT VERIFICATION

**Required:**
- OS: Windows 11
- Gemini CLI installed and reachable via PATH
- Git installed and authenticated
- Python 3.10+ (for ChromaDB)

**Boot Check Commands:**
```bash
# Verify Gemini CLI
gemini --version

# Verify Git
git --version

# Verify Python
python --version

# Verify ChromaDB installation
python -c "import chromadb; print(chromadb.__version__)"
Failure Conditions:

Gemini CLI unavailable → ABORT

Git not installed → ABORT

Python <3.10 → ABORT

ChromaDB not installed → DEGRADED MODE

STEP 2: DIRECTORY INTEGRITY CHECK
Required Directories:

text
/
├─ GEMINI.md
├─ BOOT.md
├─ skills/
├─ flows/
├─ H:/
│  ├─ .chromadb/
│  ├─ epsilon/
│  ├─ legal/
│  ├─ business/
│  └─ decisions/
└─ mcp/
Validation Script:

python
import os

required_dirs = [
    "skills",
    "flows",
    "H:/epsilon",
    "H:/legal",
    "H:/business",
    "H:/decisions",
    "mcp"
]

missing = [d for d in required_dirs if not os.path.exists(d)]

if missing:
    print(f"BOOT FAILED: Missing directories: {missing}")
else:
    print("✅ Directory structure valid")
Failure Conditions:

Missing core directories → HARD STOP

Extra directories → Ignored (allowed)

STEP 3: CONTROL FILE VALIDATION
Required Files:

GEMINI.md (project DNA)

At least ONE file in skills/

At least ONE file in flows/

Validation Checks:

python
import os

# Check GEMINI.md exists
if not os.path.exists("GEMINI.md"):
    print("BOOT FAILED: GEMINI.md missing")
    exit(1)

# Check for skills
skill_files = [f for f in os.listdir("skills") if f.endswith(".skill.md")]
if len(skill_files) == 0:
    print("BOOT FAILED: No skill files found")
    exit(1)

# Check for flows
flow_files = [f for f in os.listdir("flows") if f.endswith(".md")]
if len(flow_files) == 0:
    print("BOOT FAILED: No flow files found")
    exit(1)

print(f"✅ Found {len(skill_files)} skills, {len(flow_files)} flows")
GEMINI.md Required Sections:

System Identity

Confidence Algorithm

RAG Enforcement Rules

Execution Authority

If validation fails:
→ System enters READ-ONLY ADVISORY MODE

STEP 4: RAG INDEX STATUS CHECK
ChromaDB Health Check:

python
import chromadb
from datetime import datetime, timedelta

client = chromadb.PersistentClient(path="H:/.chromadb")

# Get all collections
collections = client.list_collections()

if len(collections) == 0:
    print("⚠️ WARNING: No ChromaDB collections found")
    print("→ System will operate in DEGRADED MODE (confidence capped at 69)")
    status = "DEGRADED"
else:
    # Check index age (placeholder - implement metadata tracking)
    print(f"✅ Found {len(collections)} RAG collection(s)")
    status = "PASS"
Staleness Rules:

Index >30 days old → DEGRADED MODE

No index → DEGRADED MODE (confidence cap = 69)

Fresh index → PASS

Recovery Action:

Run rag_data_attendant skill to rebuild index

STEP 5: STARTUP DECLARATION
System outputs:

text
==========================================
EPSILON ECOSYSTEM v1.3 BOOT REPORT
==========================================
Environment: PASS
Directory Structure: PASS
Control Files: PASS
RAG Index: PASS / DEGRADED / FAIL
------------------------------------------
BOOT STATUS: PASS
OPERATIONAL MODE: Full Authority
CONFIDENCE CAP: None (100 max)
EXECUTION AUTHORITY: Write + Execute + Deploy
JURISDICTION DEFAULT: US-WA
==========================================
Operational Modes:

PASS: Full operation authorized

DEGRADED: Non-high-risk only, confidence capped at 69

FAIL: Advisory mode only, no execution

RECOVERY PROCEDURES
If BOOT FAILS:
Check error message for missing component

Run installation scripts for missing dependencies

Verify file permissions

Retry boot sequence

If DEGRADED MODE:
Run rag_data_attendant skill to rebuild index

Verify RAG content exists in rag/ directories

Check index timestamp

Retry boot sequence

MANUAL BOOT OVERRIDE
User may force boot modes:

bash
# Force PASS (override checks - use with caution)
export EPSILON_BOOT_OVERRIDE=PASS

# Force DEGRADED (limit operations)
export EPSILON_BOOT_OVERRIDE=DEGRADED

# Force FAIL (advisory only)
export EPSILON_BOOT_OVERRIDE=FAIL
WARNING: Overrides bypass safety checks. Use only for debugging.

BOOT SEQUENCE COMPLETE
Once all steps pass, system declares:

✅ EPSILON ECOSYSTEM v1.3 READY

No execution is permitted until this declaration is made.