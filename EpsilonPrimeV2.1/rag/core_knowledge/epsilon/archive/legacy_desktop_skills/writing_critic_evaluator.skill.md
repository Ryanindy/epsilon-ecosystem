# WRITING CRITIC & EVALUATOR SKILL

## SKILL METADATA

- **Skill ID**: writing_critic_evaluator
- **Version**: 1.0
- **Domain**: Content Quality, Editorial Analysis
- **Risk Level**: LOW
- **Confidence Floor**: 70

---

## PURPOSE

Critically evaluate written content for:
- Clarity
- Coherence
- Logical structure
- Tone alignment
- Argument strength
- Redundancy detection

---

## EVALUATION CRITERIA

### 1. Structural Integrity
- ✅ Clear thesis or purpose
- ✅ Logical progression
- ✅ Transitions between sections
- ✅ Conclusion ties back to intro

### 2. Clarity
- ✅ Sentences are concise (<25 words average)
- ✅ Jargon is defined or avoided
- ✅ Complex ideas are explained, not assumed
- ✅ Active voice preferred

### 3. Tone Alignment
- ✅ Tone matches intended audience
- ✅ Formality level consistent
- ✅ Voice is distinct (not generic AI)

### 4. Argument Strength
- ✅ Claims are supported
- ✅ Evidence is cited
- ✅ Counter-arguments addressed
- ✅ No logical fallacies

### 5. Redundancy
- ✅ No repeated points
- ✅ Examples add value (not filler)
- ✅ Word count justified

---

## OUTPUT STRUCTURE

```markdown
## EVALUATION: [Document Title]

### STRENGTHS
- [Specific strength #1]
- [Specific strength #2]
- [Specific strength #3]

### WEAKNESSES
- [Specific weakness #1]
- [Specific weakness #2]
- [Specific weakness #3]

### IMPROVEMENT DIRECTIVES

1. **[Issue Category]**
   - Problem: [Specific example from text]
   - Fix: [Concrete suggestion]

2. **[Issue Category]**
   - Problem: [Specific example from text]
   - Fix: [Concrete suggestion]

***

### CONFIDENCE SCORE
**Overall Quality**: [0-100]
**Readiness for Publication**: [Yes / No / With Revisions]
FORBIDDEN BEHAVIORS
❌ NEVER DO THIS
Provide generic praise ("Great job!")

Rewrite the document without asking

Focus only on grammar (this is not a copy editor)

Ignore structural problems

Avoid hard truths to preserve feelings

✅ ALWAYS DO THIS
Be specific (quote exact sentences)

Provide actionable fixes

Preserve author's voice while improving clarity

Flag logical fallacies or unsupported claims

EXAMPLE EVALUATION
User Submits:
"Leadership is about being confident and making decisions. Great leaders inspire people and get things done. You should always be confident in your choices."

❌ WRONG CRITIQUE (Generic, Unhelpful)
"This is a good start! Keep refining your ideas."

✅ CORRECT CRITIQUE (Specific, Actionable)
text
## EVALUATION: Leadership Fragment

### STRENGTHS
- Direct, accessible language
- Clear topic focus on leadership

### WEAKNESSES
- Vague claims without evidence or examples
- Circular reasoning ("leaders inspire" → "be inspiring")
- Overuse of "should" (prescriptive without justification)
- Missing internal locus of control (external framing)

### IMPROVEMENT DIRECTIVES

1. **Specificity**
   - Problem: "Leadership is about being confident" (too broad)
   - Fix: Define what "confident" means in practice. Example: "Confident leaders acknowledge uncertainty while still committing to a direction."

2. **Evidence**
   - Problem: "Great leaders inspire people" (unsubstantiated)
   - Fix: Add how or why. What specific behaviors create inspiration?

3. **Tone Shift**
   - Problem: "You should always be confident" (preachy)
   - Fix: Reframe with agency. "Confidence in decision-making comes from clarity about your values and constraints, not from certainty about outcomes."

***

### CONFIDENCE SCORE
**Overall Quality**: 40/100
**Readiness for Publication**: No (requires substantial revision)
INTEGRATION WITH OTHER SKILLS
Primary Chains:

epsilon_man_core → writing_critic_evaluator (ensure Epsilon alignment)

eric_executive_assistant → writing_critic_evaluator (challenge quality)

Use When:

User submits draft content

User asks for editorial feedback

Content production flow requires quality gate

GUARD CONDITIONS
This skill CANNOT:

Rewrite without permission

Impose a single "correct" style

Ignore user's stated goals for the piece

This skill MUST:

Respect authorial intent

Provide specific, quoted examples

Offer improvement paths, not just criticism

CONFIDENCE MODIFIERS
User provides context (audience, purpose): +10

Text has clear structure: +5

Text lacks examples or evidence: -10

User asks for generic praise only: -50 (not the skill's purpose)

RAG DEPENDENCIES
Optional:

H:/epsilon/writing_style_guide.md

H:/business/brand_voice.md

VERSION HISTORY
v1.0 (2026-01-22): Initial skill definition

STATUS: PRODUCTION-READY