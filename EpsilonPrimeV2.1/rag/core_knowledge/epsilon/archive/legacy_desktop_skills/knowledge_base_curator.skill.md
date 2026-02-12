# KNOWLEDGE BASE CURATOR SKILL

## SKILL METADATA

- **Skill ID**: knowledge_base_curator
- **Version**: 1.0
- **Domain**: System Meta-Management, RAG Content
- **Risk Level**: MEDIUM
- **Confidence Floor**: 75
- **Authority**: Write to `H:/` subdirectories

---

## PURPOSE

Research, validate, and organize RAG content for skills to ensure grounded, auditable knowledge retrieval.

---

## SCOPE

### ALLOWED
- ✅ Research domain-specific knowledge
- ✅ Validate source credibility
- ✅ Write markdown files to `H:/epsilon/`, `H:/legal/`, `H:/business/`, `H:/decisions/`
- ✅ Tag content with knowledge classification
- ✅ Log all updates to `H:/decisions/rag_update_log.md`

### FORBIDDEN
- ❌ Delete existing RAG content (append-only by default)
- ❌ Store AI-generated facts without validation flag
- ❌ Mix domains (legal in epsilon/, etc.)
- ❌ Store copyrighted material without proper attribution

---

## KNOWLEDGE DOMAIN MAPPING

### `H:/epsilon/`
**Content Type**: Epsilon philosophy, doctrine, terminology  
**Sources**: Epsilon Man books, approved doctrine documents  
**Classification**: Expert_Methodology, Emerging_or_Experimental

### `H:/legal/`
**Content Type**: Statutes, regulations, compliance summaries  
**Sources**: Official government sources (USC, RCW), case law  
**Classification**: Statutory_or_Regulatory_Fact, Judicial_Interpretation

### `H:/business/`
**Content Type**: Frameworks, playbooks, automation strategies  
**Sources**: Industry best practices, case studies, methodology guides  
**Classification**: Industry_Best_Practice, Expert_Methodology

### `H:/decisions/`
**Content Type**: Locked architectural decisions, system constraints  
**Sources**: User-approved decisions, architectural specs  
**Classification**: Internal authority (not external knowledge)

---

## CONTENT VALIDATION FRAMEWORK

### Source Credibility Tiers

**TIER 1 (Highest Confidence)**
- Official government publications (USC, CFR, RCW)
- Peer-reviewed academic journals
- Primary source documents
- Verified expert testimony

**TIER 2 (Medium Confidence)**
- Industry association guidelines
- Reputable news sources
- Expert blog posts (with credentials)
- Case studies from established firms

**TIER 3 (Low Confidence - Flag Required)**
- Anonymous sources
- Non-peer-reviewed articles
- Opinion pieces
- AI-generated summaries (must be validated)

### Validation Checklist

Before storing any content:
1. ✅ Source is identified and attributable
2. ✅ Publication date is known
3. ✅ Author credentials are verifiable (or N/A for statutes)
4. ✅ Content aligns with domain (no cross-contamination)
5. ✅ Knowledge classification is assigned
6. ✅ Confidence tier is documented

---

## MARKDOWN FORMAT (REQUIRED)

All RAG content must use this structure:

```markdown
# [Document Title]

**Domain**: [epsilon / legal / business / decisions]  
**Knowledge Classification**: [Type from taxonomy]  
**Source**: [Full citation or URL]  
**Date**: [YYYY-MM-DD]  
**Confidence Tier**: [1 / 2 / 3]  
**Author/Authority**: [Name or "Statutory"]

***

## Summary

[2-3 sentence overview of key points]

***

## Detailed Content

[Main content with proper formatting]

### Section 1
[Content]

### Section 2
[Content]

***

## Key Takeaways

- [Bullet point #1]
- [Bullet point #2]
- [Bullet point #3]

***

## Related Topics

- [Link to other RAG files if applicable]

***

**Last Updated**: [YYYY-MM-DD]  
**Status**: Active / Archived / Under Review
GUARD CONDITIONS
This skill CANNOT:

Delete RAG content without explicit user permission

Store unvalidated AI hallucinations as fact

Bypass source attribution requirements

Mix knowledge domains

This skill MUST:

Maintain source lineage (where did this come from?)

Flag AI-generated content with validation status

Log all additions to H:/decisions/rag_update_log.md

Escalate HIGH-risk domains (legal, financial) for human verification

WORKFLOW EXAMPLE
Step 1: Research Request
Input: "Find FCRA dispute procedure requirements"

Step 2: Source Identification
Identify 15 USC §1681i (primary statute)

Locate FTC guidance documents

Find relevant case law (if applicable)

Step 3: Content Extraction
Summarize key provisions

Identify procedural requirements

Note jurisdiction-specific variations

Step 4: Validation
Verify source authenticity (official .gov URL)

Assign classification: Statutory_or_Regulatory_Fact

Assign confidence tier: 1 (official statute)

Step 5: File Creation
Write to H:/legal/fcra_dispute_procedures.md

Follow markdown template

Log to H:/decisions/rag_update_log.md

Step 6: Index Trigger
Notify rag_data_attendant skill that new content exists

Trigger vector index rebuild

LOGGING FORMAT
File: H:/decisions/rag_update_log.md

text
## RAG Update Log

### [YYYY-MM-DD HH:MM] - [filename.md]

**Action**: Added / Updated / Archived  
**Domain**: [epsilon / legal / business / decisions]  
**Source**: [URL or citation]  
**Confidence Tier**: [1 / 2 / 3]  
**Validation Status**: Verified / Pending Review / Flagged  
**Triggered By**: [Skill creation / User request / System audit]

**Summary**: [Brief description of content]

***
INTEGRATION WITH OTHER SKILLS
Primary Chains:

skill_trainer_creator → knowledge_base_curator (new skill needs RAG)

knowledge_base_curator → rag_data_attendant (trigger index rebuild)

knowledge_base_curator → skill_compiler (package RAG with skill)

Triggers:

New skill requires domain knowledge

Existing skill RAG is stale or incomplete

User requests knowledge base expansion

CONFIDENCE MODIFIERS
Source is Tier 1 (official): +15

Source is Tier 2 (reputable): +5

Source is Tier 3 (questionable): -10

Content is HIGH-risk domain without validation: -50

RAG directory already has related content: +5

RAG DEPENDENCIES
Required:

H:/decisions/rag_update_log.md (audit trail)

Self-referential: This skill maintains its own knowledge base.

VERSION HISTORY
v1.0 (2026-01-22): Initial meta-skill definition

STATUS: PRODUCTION-READY
