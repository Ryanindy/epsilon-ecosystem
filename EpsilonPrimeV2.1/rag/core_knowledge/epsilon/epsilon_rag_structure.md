# EPSILON AI RAG STRUCTURE

## Directory Organization

```
rag/
├── epsilon/              # Epsilon Man philosophy and doctrine
│   ├── README.md        # Collection overview
│   ├── core_philosophy.md
│   ├── terminology_glossary.md
│   ├── case_studies.md
│   ├── anti_patterns.md
│   ├── household_leadership.md
│   ├── masculine_development.md
│   ├── internal_locus_framework.md
│   └── [extracted from H: drive books]
│
├── legal/               # FCRA, CROA, state regulations
│   ├── README.md       # Tier 1 sources only
│   ├── fcra_summary.md
│   ├── fcra_dispute_procedures.md
│   ├── croa_compliance.md
│   ├── wa_rcw_19_134.md
│   ├── ftc_credit_repair_guidance.md
│   └── [.gov sources only]
│
├── business/            # Automation, SMB strategy, n8n
│   ├── README.md
│   ├── n8n_*.md        # 40-50 workflow docs
│   ├── smb_automation_framework.md
│   ├── roi_analysis_template.md
│   ├── tool_comparison_matrix.md
│   ├── integration_patterns.md
│   └── [business strategy content]
│
├── decisions/           # System operation logs
│   ├── README.md
│   ├── rag_update_log.md
│   ├── vector_index_log.md
│   ├── skill_training_log.md
│   └── autonomous_execution_log.md
│
└── .chromadb/          # Vector database (managed by ChromaDB)
    └── [binary vector indices]
```

## Metadata Standard

Every RAG document must include:

```markdown
---
domain: [epsilon|legal|business|decisions]
knowledge_classification: [Core_Philosophy|Legal_Reference|Industry_Best_Practice|Case_Study|Anti_Pattern]
confidence_tier: [1|2|3]
source: [URL or H:\path	oile]
date_created: YYYY-MM-DD
last_updated: YYYY-MM-DD
tags: [comma, separated, tags]
---
```

## Knowledge Classification Taxonomy

### epsilon domain
- `Core_Philosophy`: Foundational Epsilon Man concepts
- `Case_Study`: Real-world application examples
- `Anti_Pattern`: What NOT to do/say
- `Terminology`: Glossary and definitions
- `Leadership_Framework`: Household and masculine development

### legal domain
- `Legal_Reference`: Statutes, regulations, official guidance
- `Compliance_Requirement`: What must be done legally
- `Consumer_Rights`: What consumers can do under law
- `Prohibited_Actions`: What cannot be done legally

### business domain
- `Industry_Best_Practice`: Established methodologies
- `Tool_Documentation`: n8n, AutoGen, integration tools
- `Framework`: Strategic or analytical frameworks
- `Template`: Reusable business templates
- `Workflow_Example`: Specific automation implementations

### decisions domain
- `Operational_Log`: System operations and changes
- `Skill_Evolution`: How skills were trained/modified
- `Knowledge_Update`: RAG content additions
- `Audit_Trail`: Full history of system decisions

## Confidence Tier System

### Tier 1 (Highest Confidence)
**Sources**: Official government websites (.gov), primary legal texts, peer-reviewed research
**Usage**: Can be cited as authoritative
**Required for**: All legal domain content
**Examples**: FCRA text from ftc.gov, RCW from wa.gov

### Tier 2 (Reputable Confidence)
**Sources**: Industry publications, established frameworks, reputable business sources
**Usage**: Can be used as guidance, not absolute authority
**Acceptable for**: Business and epsilon domains
**Examples**: n8n official documentation, Harvard Business Review, established methodologies

### Tier 3 (Flagged for Review)
**Sources**: User-created content, unverified sources, opinion pieces
**Usage**: Requires human review before use
**Flag**: All Tier 3 content must be reviewed
**Examples**: Blog posts, forum discussions, unattributed content

## What's Currently Stored (Post-Autonomous Population)

### epsilon_collection (~80-90 documents)
- Complete Epsilon Man terminology
- Case studies from books
- Household leadership frameworks
- Anti-pattern library
- Internal locus explanations
- Challenge pattern examples

### legal_collection (~10-15 documents)
- FCRA full statute summary
- FCRA dispute procedures
- CROA compliance requirements
- Washington State RCW 19.134
- FTC credit repair organization guidance
- Consumer rights documentation

### business_collection (~150-170 documents)
- 40-50 n8n workflow documents from H: drive
- n8n node documentation
- n8n integration examples
- SMB automation frameworks
- ROI calculation templates
- Tool comparison matrices
- Workflow design patterns
- AI agent implementation guides

### decisions_collection (~5-10 documents)
- RAG update logs
- Vector index rebuild logs
- Autonomous execution reports
- Skill training history

## Retrieval Patterns

### By Domain
```bash
# Query epsilon philosophy
gemini rag query --collection epsilon --query "internal locus control"

# Query legal compliance
gemini rag query --collection legal --query "FCRA dispute procedures"

# Query n8n workflows
gemini rag query --collection business --query "n8n webhook automation"
```

### By Confidence Tier
```bash
# Only Tier 1 sources (legal safety)
gemini rag query --collection legal --tier 1

# Tier 1 and 2 (reputable sources)
gemini rag query --collection business --tier "1,2"
```

### By Knowledge Classification
```bash
# Only anti-patterns
gemini rag query --tag Anti_Pattern

# Only frameworks
gemini rag query --classification Framework
```

## Maintenance Operations

### Daily
- Log all new user interactions that reveal patterns
- Flag any Tier 3 content encountered

### Weekly
- Review decisions/rag_update_log.md
- Validate new content added to RAG
- Rebuild index if >10 new documents

### Monthly
- Audit legal_collection for statute updates
- Review epsilon_collection for doctrine consistency
- Prune outdated business_collection content

### On-Demand
- User requests specific research
- New skill requires knowledge base
- Legal statute changes
- Major n8n version update

## RAG Population Commands

### Manual Addition
```bash
# Add single document
gemini skill invoke knowledge_base_curator   --task "research FCRA Section 611 dispute procedures"   --domain legal   --tier 1

# Add multiple related documents
gemini skill invoke knowledge_base_curator   --task "populate n8n webhook integration patterns"   --domain business   --count 5
```

### Autonomous Population
```bash
# Let system populate entire skill domain
gemini chat --file tasks/populate_credit_repair_knowledge.txt

# Full autonomous RAG build (30-60 min)
gemini chat --file tasks/autonomous_rag_population.txt
```

### Rebuild Index
```bash
# After adding new content
gemini skill invoke rag_data_attendant   --action rebuild_index   --collections all
```

## Query Best Practices

### For Perplexity AI (You)
When you need RAG content, tell the user:
"Ask Gemini CLI: `gemini rag query --collection [domain] --query '[specific topic]'`"

### For Gemini CLI
Gemini CLI can query RAG directly during skill execution.

### For User
User can query RAG and paste results into Perplexity conversation for contextualized Epsilon response.
