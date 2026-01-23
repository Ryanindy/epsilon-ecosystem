# CONTENT PRODUCTION FLOW

## FLOW METADATA

- **Flow ID**: flow_content_production
- **Version**: 1.0
- **Trigger Conditions**: Books, frameworks, long-form writing, brand doctrine
- **Human Pause**: At major milestones (outline approval, draft review)
- **Confidence Requirement**: ≥75 for published content

---

## PURPOSE

Orchestrate multi-stage content creation with quality gates, brand alignment, and iterative refinement.

---

## TRIGGER CLASSIFICATION

This flow activates for:

### Long-Form Content
- Book chapters, sections
- Workbooks, guides
- Training materials
- Brand manifestos

### Framework Development
- Business models
- Philosophical frameworks
- Leadership curricula

### Multi-Asset Projects
- Books + workbooks + mentor guides
- 90-day challenges
- Course content packages

---

## FLOW EXECUTION GRAPH

[1. Project Intake]
↓
[2. Core Thesis Validation] ← Skill: epsilon_man_core / k_and_f_identity
↓
[3. Structural Outline] ← Create skeleton
↓
[4. MILESTONE PAUSE] ← User approves outline
↓
[5. Content Generation] ← Skill chaining (core → draft → critique)
↓
[6. Quality Gate] ← Skill: writing_critic_evaluator
↓
[7. Iterative Refinement] ← Loop until quality threshold met
↓
[8. Brand Integrity Check] ← Ensure alignment with Epsilon/K&F doctrine
↓
[9. MILESTONE PAUSE] ← User approves final draft
↓
[10. Packaging & Delivery] ← Assemble final artifacts

text

---

## STEP 1: PROJECT INTAKE

**Goal**: Define scope, audience, brand, and success criteria.

**Intake Questions**:
```markdown
PROJECT INTAKE FORM

1. **Content Type**: [Book chapter / Workbook / Framework / Guide]
2. **Brand**: [Epsilon Man / K&F Consulting / Neutral]
3. **Target Audience**: [Men seeking leadership / SMB owners / General]
4. **Core Message**: [One-sentence thesis]
5. **Success Criteria**: [What makes this "good enough"?]
6. **Constraints**: [Word count / Tone / Format]
Output: Project parameters (logged to H:/decisions/content_projects.md)

STEP 2: CORE THESIS VALIDATION
Goal: Ensure philosophical alignment before writing.

Skill Invocation:

python
if brand == "Epsilon Man":
    thesis_check = invoke_skill("epsilon_man_core", {
        "request": f"Validate thesis: {core_message}",
        "mode": "doctrine_alignment"
    })
    
    if thesis_check.confidence < 75:
        return "THESIS MISALIGNMENT: Refine before proceeding."

elif brand == "K&F Consulting":
    thesis_check = invoke_skill("k_and_f_identity", {
        "request": f"Validate thesis: {core_message}",
        "mode": "brand_alignment"
    })
Output: Validated thesis + confidence score

STEP 3: STRUCTURAL OUTLINE
Goal: Create content skeleton before detailed writing.

Outline Template:

text
# [Content Title]

## Core Thesis
[One-sentence summary]

## Target Audience
[Who this is for]

## Structure

### Section 1: [Title]
**Purpose**: [What this section achieves]
**Key Points**:
- [Point 1]
- [Point 2]
**Tone**: [Direct / Reflective / Technical]

### Section 2: [Title]
**Purpose**: [What this section achieves]
**Key Points**:
- [Point 1]
- [Point 2]
**Tone**: [Direct / Reflective / Technical]

### Section 3: [Title]
[...]

## Success Criteria
- [ ] Thesis is clear and defensible
- [ ] Structure is logical
- [ ] Tone aligns with brand
- [ ] Word count: [Target]
Output: Structural outline (saved to project folder)

STEP 4: MILESTONE PAUSE (Outline Approval)
System Output:

text
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 CONTENT PRODUCTION - OUTLINE REVIEW

Project: [Title]
Brand: [Epsilon / K&F]
Sections: [Count]

OUTLINE PREVIEW:
[Show section titles and purposes]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OPTIONS:
1. APPROVE - Proceed to content generation
2. REVISE - Modify structure
3. ABORT - Cancel project

[User must choose]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 5: CONTENT GENERATION (SKILL CHAINING)
Goal: Generate first draft using skill chain.

Chain Pattern:

text
epsilon_man_core (philosophical framing)
   ↓
creative_writing (draft generation)
   ↓
writing_critic_evaluator (quality check)
   ↓
eric_executive_assistant (challenge weak points)
   ↓
REFINED DRAFT
Section-by-Section Generation:

python
for section in outline.sections:
    # Generate draft
    draft = invoke_skill("creative_writing", {
        "section": section,
        "brand_context": brand,
        "tone": section.tone
    })
    
    # Critique
    critique = invoke_skill("writing_critic_evaluator", {
        "content": draft,
        "criteria": ["clarity", "logic", "tone_alignment"]
    })
    
    # Refine if needed
    if critique.confidence < 75:
        draft = refine_based_on_critique(draft, critique)
    
    save_section(draft, section.id)
STEP 6: QUALITY GATE
Goal: Ensure content meets minimum standards.

Evaluation Criteria:

Clarity: Average sentence length <25 words

Logic: No unsupported claims or fallacies

Tone: Aligns with brand voice

Structure: Transitions are smooth

Value: No filler, every paragraph serves the thesis

Pass Threshold: Quality score ≥75/100

Failure Mode:
If quality <75 → return to Step 5 (refinement loop, max 3 iterations)

STEP 7: ITERATIVE REFINEMENT
Refinement Loop (max 3 cycles):

python
iteration = 0
while quality_score < 75 and iteration < 3:
    # Get specific critiques
    issues = writing_critic_evaluator.identify_weaknesses(draft)
    
    # Address each issue
    for issue in issues:
        draft = fix_issue(draft, issue)
    
    # Re-evaluate
    quality_score = writing_critic_evaluator.evaluate(draft)
    iteration += 1

if quality_score < 75:
    flag_for_human_review("Quality threshold not met after 3 iterations")
STEP 8: BRAND INTEGRITY CHECK
Goal: Verify philosophical alignment.

Epsilon Brand Check:

No motivational clichés

No alpha/beta language

Internal locus of control framing

No dependency-forming language

K&F Brand Check:

Professional, not overly formal

Client-value focused

Expertise without arrogance

Automated Scan:

python
forbidden_patterns = {
    "Epsilon": ["you're a king", "alpha male", "winners win"],
    "K&F": ["we're the best", "guaranteed results"]
}

for pattern in forbidden_patterns[brand]:
    if pattern in draft.lower():
        flag_violation(pattern, draft_section)
STEP 9: MILESTONE PAUSE (Draft Approval)
System Output:

text
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 CONTENT PRODUCTION - DRAFT REVIEW

Project: [Title]
Word Count: [Count]
Quality Score: [85/100]
Brand Alignment: PASS

PREVIEW (First 500 words):
[Show beginning of content]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OPTIONS:
1. APPROVE - Finalize and package
2. REVISE - Make specific edits
3. REJECT - Return to outline phase

[User must choose]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 10: PACKAGING & DELIVERY
Goal: Assemble final artifacts in correct formats.

Output Formats:

Markdown (master copy)

PDF (print-ready)

EPUB (if book)

Notion-ready (if workbook)

Packaging Script:

python
def package_content(project):
    # Combine all sections
    full_draft = assemble_sections(project.sections)
    
    # Add front matter
    full_draft = add_frontmatter(full_draft, project.metadata)
    
    # Generate formats
    markdown_file = save_as_markdown(full_draft, f"output/{project.title}.md")
    pdf_file = convert_to_pdf(full_draft, f"output/{project.title}.pdf")
    
    # Log completion
    log_project_completion(project, {
        "markdown": markdown_file,
        "pdf": pdf_file,
        "quality_score": project.final_quality_score
    })
    
    return {
        "status": "COMPLETE",
        "files": [markdown_file, pdf_file]
    }
INTEGRATION WITH SKILLS
Primary Skills:

epsilon_man_core (philosophy/brand alignment)

creative_writing (draft generation)

writing_critic_evaluator (quality gates)

eric_executive_assistant (challenge mode for depth)

Optional Skills:

metaphysics_analysis (if philosophical content)

ai_automation_strategist_smb (if technical/business content)

LOGGING REQUIREMENTS
File: H:/decisions/content_projects.md

text
## Content Production Log

### [YYYY-MM-DD] - [Project Title]

**Type**: [Book Chapter / Workbook / Framework]  
**Brand**: [Epsilon / K&F]  
**Word Count**: [Target / Actual]  
**Quality Score**: [Final]

**Timeline**:
- Intake: [Date]
- Outline Approved: [Date]
- Draft 1 Complete: [Date]
- Final Approval: [Date]

**Iterations**: [Count]  
**Status**: [IN PROGRESS / COMPLETE / ON HOLD]

**Outputs**:
- [Path to markdown]
- [Path to PDF]

***
VERSION HISTORY
v1.0 (2026-01-22): Initial flow definition

STATUS: PRODUCTION-READY
