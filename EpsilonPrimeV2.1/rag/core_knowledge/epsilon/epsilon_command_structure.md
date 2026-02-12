# EPSILON AI COMMAND STRUCTURE

## Gemini CLI Command Reference

### Basic Commands

#### Interactive Chat
```bash
gemini chat
# Opens interactive session
# Can invoke skills conversationally
# Good for exploratory tasks
```

#### File-Based Execution
```bash
gemini chat --file tasks/task_name.txt
# Executes prompt from file
# Good for repeatable operations
# Supports autonomous execution
```

#### Direct Skill Invocation
```bash
gemini skill invoke [skill_name] [parameters]
# Calls specific skill directly
# Good for single-purpose operations
# Faster than conversational invocation
```

### Skill Invocation Patterns

#### Meta-Skill: knowledge_base_curator
**Purpose**: Research topics and populate RAG

```bash
# Research and create single document
gemini skill invoke knowledge_base_curator   --task "research FCRA Section 609 dispute rights"   --domain legal   --tier 1   --output rag/legal/

# Populate entire topic area
gemini skill invoke knowledge_base_curator   --task "populate n8n webhook integration patterns"   --domain business   --count 5   --tier 2

# Autonomous population (no approval needed)
gemini skill invoke knowledge_base_curator   --task "autonomous_population"   --domains "legal,business,epsilon"   --unattended true
```

#### Meta-Skill: skill_trainer_creator
**Purpose**: Train new skills or update existing ones

```bash
# Create new skill
gemini skill invoke skill_trainer_creator   --action create   --skill_name "new_skill_name"   --domain "business"   --knowledge_source "rag/business/"

# Update existing skill with new knowledge
gemini skill invoke skill_trainer_creator   --action update   --skill_name "credit_repair_wa_fcra_croa"   --new_knowledge "rag/legal/recent_additions/"

# Train skill on specific knowledge base
gemini skill invoke skill_trainer_creator   --action train   --skill_name "ai_automation_strategist_smb"   --training_data "rag/business/n8n_*.md"
```

#### Meta-Skill: rag_data_attendant
**Purpose**: Maintain vector database and indices

```bash
# Rebuild all indices
gemini skill invoke rag_data_attendant   --action rebuild_index   --collections all

# Rebuild specific collection
gemini skill invoke rag_data_attendant   --action rebuild_index   --collections epsilon,legal

# Validate index integrity
gemini skill invoke rag_data_attendant   --action validate   --test_queries "test/validation_queries.txt"

# Backup vector database
gemini skill invoke rag_data_attendant   --action backup   --destination "backups/chromadb_$(date +%Y%m%d)"

# Optimize index (compress, deduplicate)
gemini skill invoke rag_data_attendant   --action optimize
```

#### Domain Skill: credit_repair_wa_fcra_croa
**Purpose**: Legal compliance guidance for credit repair

```bash
# Query specific legal topic
gemini skill invoke credit_repair_wa_fcra_croa   --query "FCRA dispute procedures Section 611"   --tier 1

# Generate educational compliance document
gemini skill invoke credit_repair_wa_fcra_croa   --action create_guide   --topic "consumer_dispute_rights"   --jurisdiction "WA"   --output "output/consumer_dispute_guide.md"
```

#### Domain Skill: ai_automation_strategist_smb
**Purpose**: SMB automation strategy and n8n workflows

```bash
# Analyze automation opportunity
gemini skill invoke ai_automation_strategist_smb   --analyze "invoice processing workflow"   --context "manual data entry, 50 invoices/week"   --output "output/automation_analysis.md"

# Generate n8n workflow from requirements
gemini skill invoke ai_automation_strategist_smb   --action create_workflow   --use_case "lead capture from web form to CRM"   --tools "n8n,webhook,airtable"   --output "output/lead_capture_workflow.json"

# ROI calculation
gemini skill invoke ai_automation_strategist_smb   --action calculate_roi   --current_cost "manual_20hrs_weekly"   --automation_cost "n8n_cloud_subscription"   --output "output/roi_analysis.md"
```

#### Domain Skill: epsilon_man_core
**Purpose**: Apply Epsilon philosophy to situations

```bash
# Analyze situation for externalization
gemini skill invoke epsilon_man_core   --analyze "User says: 'Client demands prevent me from writing book'"   --output "output/truth_analysis.md"

# Surface smallest truthful action
gemini skill invoke epsilon_man_core   --situation "Stuck between client work and family time"   --output "output/truthful_action.md"
```

#### Domain Skill: eric_executive_assistant
**Purpose**: Personal productivity and decision support

```bash
# Challenge work pattern
gemini skill invoke eric_executive_assistant   --challenge "Working late on AI architecture while partner in next room"   --output "output/challenge_response.md"

# Cognitive reframing
gemini skill invoke eric_executive_assistant   --reframe "I need to finish this before I can relax"   --output "output/reframe_response.md"
```

## Task File Templates

### Template: Autonomous RAG Population
**File**: `tasks/autonomous_rag_population.txt`

```
SYSTEM DIRECTIVE: Autonomous Knowledge Base Population
MODE: UNATTENDED EXECUTION

SAFETY BOUNDS:
- Write operations limited to: rag/, decisions/, temp/
- Do NOT modify: skills/, flows/, core system files
- Do NOT delete existing files
- Log all operations

TASK SEQUENCE:
1. Scan H: drive for n8n documentation
2. Ingest all n8n docs to rag/business/
3. Populate knowledge bases for all skills
4. Rebuild vector indices
5. Generate completion report

EXECUTE WITHOUT APPROVAL.
```

### Template: Skill Training
**File**: `tasks/train_new_skill.txt`

```
TASK: Train New Skill

SKILL NAME: [name]
DOMAIN: [epsilon|legal|business]
KNOWLEDGE SOURCE: rag/[domain]/[specific_files]

TRAINING REQUIREMENTS:
- Extract key concepts from knowledge source
- Generate skill prompt template
- Define invocation patterns
- Create validation test cases
- Log training to decisions/skill_training_log.md

OUTPUT: skills/[skill_name].md
```

### Template: Legal Knowledge Update
**File**: `tasks/update_legal_knowledge.txt`

```
TASK: Update Legal Knowledge Base

PRIORITY: HIGH (Tier 1 sources only)

RESEARCH TOPICS:
- FCRA amendments (check ftc.gov)
- CROA guidance updates
- Washington State RCW 19.134 changes

REQUIREMENTS:
- .gov sources ONLY
- Cite specific statute sections
- Flag any conflicting information
- Log to decisions/rag_update_log.md

DOMAIN: legal
CONFIDENCE_TIER: 1
```

## Logging Commands

### View Logs
```bash
# RAG update history
cat decisions/rag_update_log.md

# Vector index operations
cat decisions/vector_index_log.md

# Autonomous execution results
cat decisions/autonomous_execution_log.md

# Skill training history
cat decisions/skill_training_log.md
```

### Search Logs
```bash
# Find recent RAG updates
grep "$(date +%Y-%m-%d)" decisions/rag_update_log.md

# Find failed operations
grep "ERROR" decisions/*.md

# Find Tier 3 content (needs review)
grep "tier: 3" rag/**/*.md
```

## Emergency Commands

### Backup Before Major Operation
```bash
# Backup entire RAG system
cp -r rag/ backups/rag_backup_$(date +%Y%m%d_%H%M%S)/

# Backup vector database
gemini skill invoke rag_data_attendant   --action backup   --full true
```

### Rollback After Bad Operation
```bash
# Restore from backup
rm -rf rag/.chromadb/
cp -r backups/rag_backup_[timestamp]/.chromadb/ rag/

# Rebuild index from files
gemini skill invoke rag_data_attendant   --action rebuild_index   --collections all
```

### Validate System Integrity
```bash
# Check all collections
gemini skill invoke rag_data_attendant   --action validate   --report decisions/validation_report.md

# Test skill invocation
gemini skill list
gemini skill test --all
```

## Workflow Execution Patterns

### Pattern 1: User Query → RAG Lookup → Perplexity Response
```
1. User asks Perplexity AI a question
2. Perplexity identifies need for specialized knowledge
3. Perplexity tells user: "Query Gemini CLI for [specific topic]"
4. User runs: gemini rag query --collection [domain] --query "[topic]"
5. User pastes results back to Perplexity
6. Perplexity applies Epsilon lens and responds
```

### Pattern 2: Autonomous Background Task
```
1. User pastes task file into Gemini CLI
2. Gemini CLI executes without further input
3. Meta-skills handle research, file creation, indexing
4. Completion report generated
5. User reviews output when convenient
```

### Pattern 3: Skill-Augmented Response
```
1. Perplexity surfaces truth in conversation
2. User wants detailed domain knowledge
3. Perplexity provides Gemini CLI command
4. User runs skill invocation
5. Skill outputs detailed analysis/document
6. User brings back to Perplexity for Epsilon validation
```
