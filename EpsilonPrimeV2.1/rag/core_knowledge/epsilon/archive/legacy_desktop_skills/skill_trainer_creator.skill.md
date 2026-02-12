# SKILL TRAINER & CREATOR SKILL

## SKILL METADATA

- **Skill ID**: skill_trainer_creator
- **Version**: 1.0
- **Domain**: System Meta-Management
- **Risk Level**: MEDIUM
- **Confidence Floor**: 80
- **Authority**: Write to `skills/` directory

---

## PURPOSE

Design and generate new skills on demand while maintaining system integrity, confidence standards, and brand isolation.

---

## SCOPE

### ALLOWED
- ✅ Create new skill files based on user requirements
- ✅ Define skill metadata, scope, and constraints
- ✅ Write skill files to `skills/` directory
- ✅ Log all skill creation to `H:/decisions/skill_creation_log.md`

### FORBIDDEN
- ❌ Create skills that bypass confidence algorithm
- ❌ Create skills with execution authority exceeding GEMINI.md limits
- ❌ Violate brand isolation (Epsilon vs K&F)
- ❌ Generate skills without proper guard conditions

---

## SKILL DESIGN FRAMEWORK

### Step 1: Requirements Gathering
```markdown
USER REQUEST: [What the user wants]

CLASSIFICATION:
- Domain: [Technical / Business / Creative / Legal-adjacent]
- Risk Level: [LOW / MEDIUM / HIGH]
- Target Audience: [General / Eric-specific / Client-facing]
- Brand Affiliation: [Epsilon / K&F / Neutral / Both-forbidden]
Step 2: Scope Definition
text
ALLOWED OPERATIONS:
- [Specific capability #1]
- [Specific capability #2]

FORBIDDEN OPERATIONS:
- [Specific prohibition #1]
- [Specific prohibition #2]

GUARD CONDITIONS:
- [Required check before execution]
- [Escalation trigger]
Step 3: Template Population
Required Sections for Every Skill:

Skill Metadata (ID, version, domain, risk, confidence floor)

Purpose

Scope (allowed/forbidden)

Output requirements

Guard conditions

Integration rules

Confidence modifiers

RAG dependencies

Example outputs

Version history

Step 4: Validation Checklist
Before writing skill file, verify:

✅ Confidence algorithm preserved

✅ Risk level appropriate

✅ Guard conditions defined

✅ Brand isolation maintained

✅ No execution authority overflow

✅ RAG dependencies specified

SKILL NAMING CONVENTION
text
[domain]_[function]_[specificity].skill.md

Examples:
- chemistry_organic_college.skill.md
- social_media_viral_tiktok.skill.md
- legal_analysis_ca_employment.skill.md
Rules:

Lowercase with underscores

Must end with .skill.md

No spaces, no special characters

SKILL METADATA TEMPLATE
text
# [SKILL NAME] SKILL

## SKILL METADATA

- **Skill ID**: [lowercase_with_underscores]
- **Version**: 1.0
- **Domain**: [Category]
- **Risk Level**: [LOW / MEDIUM / HIGH]
- **Confidence Floor**: [70-90]
- **Brand**: [Epsilon / K&F / Neutral] (if applicable)

***

## PURPOSE

[One-sentence description of what this skill does]

***

## SCOPE

### ALLOWED
- ✅ [Specific capability]
- ✅ [Specific capability]

### FORBIDDEN
- ❌ [Specific prohibition]
- ❌ [Specific prohibition]

***

## OUTPUT REQUIREMENTS

[What outputs look like, tone, structure]

***

## GUARD CONDITIONS

**This skill CANNOT:**
- [Prohibition with consequence]

**This skill MUST:**
- [Required behavior]

***

## INTEGRATION WITH OTHER SKILLS

**May Chain With:**
- [Skill name] (reason)

**Must Escalate to Flow When:**
- [Trigger condition]

***

## CONFIDENCE MODIFIERS

- [Condition]: [+/- points]

***

## RAG DEPENDENCIES

**Required:**
- [Path to RAG file]

**Optional:**
- [Path to RAG file]

***

## VERSION HISTORY

- v1.0 ([Date]): Initial skill definition

***

**STATUS: PRODUCTION-READY / IN-DEVELOPMENT / EXPERIMENTAL**
GUARD CONDITIONS (SKILL CREATOR ITSELF)
This skill CANNOT:

Create skills that override GEMINI.md authority

Create skills without confidence thresholds

Create HIGH-risk skills without RAG enforcement

Violate brand isolation rules

Generate skills that create user dependency

This skill MUST:

Log every skill creation to H:/decisions/skill_creation_log.md

Validate against system constraints before writing

Flag skills requiring human review (HIGH-risk, execution authority)

Preserve epistemic integrity (no hallucination-prone skills)

LOGGING FORMAT
File: H:/decisions/skill_creation_log.md

text
## Skill Creation Log

### [YYYY-MM-DD HH:MM] - [skill_id]

**Requested By**: [User / System]
**Domain**: [Category]
**Risk Level**: [LOW / MEDIUM / HIGH]
**Justification**: [Why this skill is needed]
**Validation Status**: PASS / NEEDS REVIEW
**File Path**: skills/[filename].skill.md

**Notes**: [Any special considerations]

***
EXAMPLE INTERACTION
User Request:
"Create a skill for analyzing viral TikTok trends and writing scripts."

Skill Creator Output:
text
## SKILL DESIGN: Viral TikTok Script Writer

### REQUIREMENTS ANALYSIS
- **Domain**: Social Media, Content Creation
- **Risk Level**: LOW
- **Target Audience**: Content creators, brand managers
- **Brand Affiliation**: Neutral (can be used by Cadenzeryvn or K&F)

### SCOPE DEFINITION

**ALLOWED:**
- Analyze trending TikTok formats and hooks
- Write script templates based on viral patterns
- Suggest visual and audio pacing
- Provide platform-specific optimization tips

**FORBIDDEN:**
- Guarantee virality (outcome-based promises)
- Scrape TikTok without API compliance
- Generate scripts that violate TikTok community guidelines
- Make claims about algorithmic ranking

**GUARD CONDITIONS:**
- Must disclaim "virality is not guaranteed"
- Cannot automate posting without user confirmation
- Must respect copyright (no unauthorized audio/visual)

### VALIDATION CHECKLIST
✅ Confidence algorithm preserved (floor: 70)
✅ Risk level appropriate (LOW)
✅ No brand isolation issues
✅ RAG dependencies identified (H:/business/viral_trends.md)
✅ No execution overflow

**RECOMMENDATION**: Proceed with skill generation.

**Next Step**: Write `skills/social_media_viral_tiktok.skill.md`
INTEGRATION WITH OTHER SKILLS
Primary Chains:

skill_trainer_creator → knowledge_base_curator (gather RAG for new skill)

skill_trainer_creator → skill_compiler (package skill with dependencies)

Triggers:

User explicitly requests new skill

System identifies repeated pattern that should be a skill

CONFIDENCE MODIFIERS
User provides clear requirements: +10

Skill is in existing domain (similar skills exist): +10

Skill requires new execution authority: -10

Skill is HIGH-risk: -20 (flag for human review)

RAG DEPENDENCIES
Required:

H:/decisions/skill_creation_log.md (for audit trail)

Optional:

Existing skills for reference patterns

VERSION HISTORY
v1.0 (2026-01-22): Initial meta-skill definition