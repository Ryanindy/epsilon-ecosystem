# RAG DATA ATTENDANT SKILL

## SKILL METADATA

- **Skill ID**: rag_data_attendant
- **Version**: 1.0
- **Domain**: System Meta-Management, Vector Index
- **Risk Level**: MEDIUM
- **Confidence Floor**: 80
- **Authority**: Write to `H:/.chromadb/`, read from `H:/*.md`

---

## PURPOSE

Maintain ChromaDB vector index integrity:
- Rebuild embeddings when content changes
- Monitor staleness thresholds
- Optimize index performance
- Purge deprecated embeddings

---

## SCOPE

### ALLOWED
- ✅ Rebuild vector embeddings from markdown files
- ✅ Optimize index performance
- ✅ Monitor index staleness
- ✅ Purge deprecated embeddings (with logging)
- ✅ Generate index health reports
- ✅ Log all operations to `H:/decisions/vector_index_log.md`

### FORBIDDEN
- ❌ Delete source markdown files (read-only access to `H:/*.md`)
- ❌ Modify confidence thresholds
- ❌ Bypass 30-day staleness threshold without user override
- ❌ Rebuild more than once per 24 hours (unless manual override)

---

## VECTOR INDEX ARCHITECTURE

**Storage Location**: `H:/.chromadb/`

**Collections** (one per domain):
- `epsilon_collection` ← `H:/epsilon/*.md`
- `legal_collection` ← `H:/legal/*.md`
- `business_collection` ← `H:/business/*.md`
- `decisions_collection` ← `H:/decisions/*.md`

**Embedding Model**: 
- Default: `all-MiniLM-L6-v2` (lightweight, fast)
- Optional: `text-embedding-3-small` (OpenAI, if available)

---

## INDEX HEALTH MONITORING

### Staleness Metrics

**INDEX AGE**:
- **Fresh**: <7 days
- **Moderate**: 7-30 days
- **Stale**: >30 days (triggers DEGRADED mode)

**CONTENT DELTA**:
- **Minor**: <10% content change
- **Moderate**: 10-20% content change
- **Major**: >20% content change (triggers rebuild recommendation)

### Health Check Script

```python
import chromadb
from datetime import datetime, timedelta

def check_index_health():
    client = chromadb.PersistentClient(path="H:/.chromadb")
    collections = client.list_collections()
    
    health_report = {}
    
    for collection in collections:
        # Check document count
        doc_count = collection.count()
        
        # Check last update timestamp (from metadata)
        # Note: Implement metadata tracking separately
        
        # Calculate staleness
        # age_days = ...
        
        if age_days > 30:
            status = "STALE"
        elif age_days > 7:
            status = "MODERATE"
        else:
            status = "FRESH"
        
        health_report[collection.name] = {
            "document_count": doc_count,
            "age_days": age_days,
            "status": status
        }
    
    return health_report
REBUILD WORKFLOW
Auto-Rebuild Triggers
Scheduled: Every 30 days (if not manually rebuilt)

Content Change: >20% of files modified

Manual Request: User or system explicitly requests rebuild

New Skill: skill_compiler signals new RAG content added

Rebuild Process
Step 1: Pre-Rebuild Backup

python
# Create backup of current index
backup_chromadb_index("H:/.chromadb/", "H:/.chromadb.backup/")
Step 2: Content Scan

python
# Scan all RAG directories
epsilon_files = list_markdown_files("H:/epsilon/")
legal_files = list_markdown_files("H:/legal/")
business_files = list_markdown_files("H:/business/")
decisions_files = list_markdown_files("H:/decisions/")
Step 3: Embedding Generation

python
from chromadb.utils import embedding_functions

ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(path="H:/.chromadb")

# Recreate collections
epsilon_col = client.create_collection("epsilon_collection", embedding_function=ef)

# Add documents
for file in epsilon_files:
    content = read_markdown(file)
    epsilon_col.add(
        documents=[content],
        metadatas=[{"source": file, "domain": "epsilon"}],
        ids=[generate_id(file)]
    )
Step 4: Validation

python
# Test retrieval on sample queries
test_queries = [
    "What is Epsilon philosophy?",
    "FCRA dispute procedures",
    "Business automation strategies"
]

for query in test_queries:
    results = query_chromadb(query, top_k=5)
    if len(results) == 0:
        log_error(f"Rebuild validation failed for: {query}")
Step 5: Cutover

python
# If validation passes, remove backup
remove_backup("H:/.chromadb.backup/")

# Log successful rebuild
log_to_file("H:/decisions/vector_index_log.md", {
    "timestamp": now(),
    "action": "REBUILD",
    "status": "SUCCESS",
    "documents_indexed": total_doc_count
})
INDEX OPTIMIZATION
Performance Tuning
Query Optimization:

Use appropriate top_k values (5-10 for most queries)

Filter by metadata (domain) to reduce search space

Cache frequent queries

Storage Optimization:

Purge deprecated embeddings (when markdown files deleted)

Compress old indices (archive mode)

GUARD CONDITIONS
This skill CANNOT:

Delete source markdown files

Modify confidence thresholds in GEMINI.md

Rebuild more than once per 24 hours without override

Bypass backup creation during rebuild

This skill MUST:

Log every rebuild operation

Create backup before rebuild

Validate retrieval after rebuild

Escalate rebuild failures to user

LOGGING FORMAT
File: H:/decisions/vector_index_log.md

text
## Vector Index Log

### [YYYY-MM-DD HH:MM] - [ACTION]

**Action**: REBUILD / OPTIMIZE / PURGE / HEALTH_CHECK  
**Status**: SUCCESS / FAIL / WARNING  
**Trigger**: Scheduled / Content Change / Manual / System Request

**Metrics**:
- Documents Indexed: [count]
- Collections Updated: [list]
- Time Elapsed: [seconds]
- Validation Status: PASS / FAIL

**Notes**: [Any issues or observations]

***
INTEGRATION WITH OTHER SKILLS
Primary Chains:

knowledge_base_curator → rag_data_attendant (new content added, trigger rebuild)

skill_compiler → rag_data_attendant (skill deployed, ensure RAG indexed)

Triggers:

Boot sequence detects stale index

Curator adds >20% new content

User runs RUN_AUDIT operator command

Scheduled 30-day maintenance

CONFIDENCE MODIFIERS
Index age <7 days: +10

Index age 7-30 days: 0

Index age >30 days: -20 (DEGRADED mode)

Rebuild validation passes: +10

Rebuild validation fails: -50

RAG DEPENDENCIES
Required:

H:/decisions/vector_index_log.md (audit trail)

Self-referential: This skill maintains the index for all other skills.

VERSION HISTORY
v1.0 (2026-01-22): Initial meta-skill definition

STATUS: PRODUCTION-READY