# EPSILON AI OPERATIONAL WORKFLOWS

## Workflow 1: Truth-Surfacing Session (Standard Interaction)

### Trigger
User presents a problem, decision, or apparent conflict

### Perplexity AI Steps
1. **Detect Externalization Pattern**
   - Identify what/who is being blamed
   - Notice future-tense language ("after I...", "when I...")
   - Recognize false dichotomies ("X or Y")

2. **Surface Actual Choice**
   - State what the real choice is
   - Cut through stated problem to underlying avoidance
   - Example: "Client work vs book work" → "Work vs Kevyn"

3. **Present Smallest Truthful Action**
   - State specific, immediate action
   - Present tense only
   - No qualifiers or conditions
   - Example: "Close the laptop."

4. **Challenge Rationalizations**
   - Reject "I will after..."
   - Reject "That makes sense, but..."
   - Reject any delay or condition
   - Repeat: "That's still externalization."

5. **Validate or Acknowledge Avoidance**
   - If user acts: Success. Session validated.
   - If user avoids: State plainly. "You chose avoidance." End session.

### Success Criteria
- User states present-tense commitment AND acts
- User demonstrates discomfort (indicates truth recognized)
- User stops responding (went to act)

### Failure Criteria
- User ends with "I'll think about it"
- User introduces new external factors
- User seeks more time
- User thanks without acting

## Workflow 2: Specialized Knowledge Query

### Trigger
User question requires domain expertise not in Epsilon philosophy

### Perplexity AI Steps
1. **Identify Knowledge Domain**
   - Legal: FCRA, CROA, state regulations
   - Business: n8n workflows, automation strategy
   - Epsilon: Specific terminology or case studies

2. **Determine Required Collection**
   - epsilon_collection: Philosophy, terminology
   - legal_collection: Statutes, compliance
   - business_collection: Technical documentation

3. **Provide Gemini CLI Command**
   ```
   "Query your Gemini CLI system:

   gemini rag query --collection [domain] --query '[specific topic]'

   Paste the results back here and I'll interpret through Epsilon lens."
   ```

4. **Wait for User to Return RAG Results**

5. **Apply Epsilon Framework to Technical Content**
   - Take RAG information
   - Apply truth-surfacing lens
   - Surface action, not just information
   - Challenge any externalization even in technical context

### Example Flow
```
User: "What are the FCRA dispute procedures?"

Perplexity: 
"Query your Gemini CLI:
gemini rag query --collection legal --query 'FCRA Section 611 dispute procedures'

Bring the results back and I'll help you apply them to your actual situation."

[User returns with RAG output]

Perplexity:
"FCRA Section 611 gives consumers the right to dispute inaccurate information 
by submitting a written request to credit bureaus [legal:1].

Now: Why are you asking this? 
- Are you stalling on sending your dispute letter?
- Or do you need this information to actually file a dispute right now?

The smallest truthful action is: [whatever the actual action is]."
```

## Workflow 3: Autonomous Knowledge Base Population

### Trigger
User needs RAG populated with new domain knowledge

### User Steps
1. **Create or Use Task File**
   - Define what knowledge to research
   - Specify domain (legal/business/epsilon)
   - Set confidence tier requirements
   - Authorize autonomous operation

2. **Execute via Gemini CLI**
   ```bash
   gemini chat --file tasks/populate_[domain]_knowledge.txt
   ```

3. **Go Do Something Else**
   - System operates autonomously
   - No approval needed (if authorized in task file)
   - Estimated 30-60 minutes for major population

### Gemini CLI Steps (Autonomous)
1. **knowledge_base_curator Invoked**
   - Researches specified topics
   - Creates markdown files with metadata
   - Saves to appropriate rag/[domain]/ directory
   - Logs every file to decisions/rag_update_log.md

2. **Special Handling for H: Drive Content**
   - Scans H: drive for matching files
   - Ingests n8n documentation
   - Extracts Epsilon Man book content
   - Converts to markdown with proper metadata

3. **rag_data_attendant Invoked**
   - Rebuilds vector indices
   - Validates index integrity
   - Tests sample queries
   - Logs results to decisions/vector_index_log.md

4. **Generate Completion Report**
   - Files created (count and list)
   - Source quality breakdown (Tier 1/2/3)
   - Documents flagged for review
   - Errors encountered
   - Next steps recommended

### User Steps (Upon Return)
1. **Review Report**
   ```bash
   cat output/autonomous_kb_population_report.md
   ```

2. **Check Logs**
   ```bash
   cat decisions/rag_update_log.md
   cat decisions/vector_index_log.md
   ```

3. **Review Flagged Content**
   - Any Tier 3 sources (low confidence)
   - All legal domain content (verify Tier 1)

4. **Validate with Sample Query**
   ```bash
   gemini rag query --collection [domain] --query "[test topic]"
   ```

## Workflow 4: Skill Training or Update

### Trigger
New skill needed OR existing skill needs knowledge update

### User Steps
1. **Identify Skill Need**
   - What domain does it cover?
   - What knowledge base will it use?
   - What should it output?

2. **Prepare Task File**
   ```
   TASK: Train New Skill

   SKILL NAME: [name]
   DOMAIN: [epsilon|legal|business]
   KNOWLEDGE SOURCE: rag/[domain]/[files]

   TRAINING REQUIREMENTS:
   - [List what skill should learn]

   OUTPUT: skills/[skill_name].md
   ```

3. **Execute Training**
   ```bash
   gemini skill invoke skill_trainer_creator      --action create      --skill_name "[name]"      --knowledge_source "rag/[domain]/"
   ```

### Gemini CLI Steps
1. **skill_trainer_creator Invoked**
   - Reads specified knowledge source
   - Extracts key concepts and patterns
   - Generates skill prompt template
   - Defines invocation patterns
   - Creates validation test cases

2. **Creates Skill File**
   - Saves to skills/[skill_name].md
   - Includes: Purpose, Knowledge Base, Invocation Examples, Validation Tests

3. **Logs Training**
   - Records in decisions/skill_training_log.md
   - Notes knowledge source used
   - Documents test results

4. **Returns Invocation Command**
   ```
   Skill trained successfully.

   Invoke with:
   gemini skill invoke [skill_name] --task "[description]"
   ```

### User Steps (Validation)
1. **Test Skill**
   ```bash
   gemini skill invoke [skill_name] --task "[test case]"
   ```

2. **Review Output**
   - Does it meet requirements?
   - Does it surface truth (if Epsilon-aligned)?
   - Does it cite sources appropriately?

3. **Iterate if Needed**
   - Update knowledge source
   - Retrain with additional examples
   - Refine skill prompt

## Workflow 5: System Health Check

### Frequency
- Daily: Quick validation
- Weekly: Full audit
- Monthly: Deep review

### Daily Health Check (5 minutes)
```bash
# Check for errors in recent operations
grep "ERROR" decisions/*_log.md | tail -20

# Verify index is accessible
gemini rag query --collection epsilon --query "internal locus" | head -5

# Check for Tier 3 content needing review
grep -r "tier: 3" rag/**/*.md
```

### Weekly Audit (30 minutes)
```bash
# Review all logs from past week
cat decisions/rag_update_log.md | grep "$(date -d '7 days ago' +%Y-%m)"

# Count documents per collection
find rag/epsilon/ -name "*.md" | wc -l
find rag/legal/ -name "*.md" | wc -l
find rag/business/ -name "*.md" | wc -l

# Validate legal collection still Tier 1 only
grep -r "tier: [23]" rag/legal/ # Should return nothing

# Test sample queries across domains
gemini rag query --collection epsilon --query "smallest truthful action"
gemini rag query --collection legal --query "FCRA dispute"
gemini rag query --collection business --query "n8n webhook"

# Review autonomous execution results
cat decisions/autonomous_execution_log.md
```

### Monthly Deep Review (2-3 hours)
1. **Legal Collection Audit**
   - Check for statute updates on ftc.gov, wa.gov
   - Verify all sources still Tier 1
   - Update any changed regulations

2. **Epsilon Collection Review**
   - Ensure doctrine consistency
   - Add recent case studies if applicable
   - Prune any contradictory content

3. **Business Collection Maintenance**
   - Check for outdated n8n documentation
   - Update tool comparisons if needed
   - Add new workflow patterns discovered

4. **Skill Performance Review**
   - Test each skill with validation queries
   - Check for skills that need retraining
   - Deprecate unused skills

5. **Index Optimization**
   ```bash
   gemini skill invoke rag_data_attendant --action optimize
   ```

6. **Backup Verification**
   ```bash
   # Verify backups exist and are recent
   ls -lh backups/ | tail -10

   # Test restore procedure (dry run)
   gemini skill invoke rag_data_attendant --action validate_backup
   ```

## Workflow 6: Emergency Rollback

### Trigger
Bad knowledge added, index corrupted, or major error

### Immediate Steps
1. **Stop All Operations**
   ```bash
   # If Gemini CLI running autonomous task, interrupt
   # Ctrl+C in terminal
   ```

2. **Assess Damage**
   ```bash
   # Check logs for what happened
   tail -50 decisions/*_log.md

   # Identify which collection affected
   ```

3. **Restore from Backup**
   ```bash
   # List available backups
   ls -lh backups/

   # Restore most recent good backup
   rm -rf rag/.chromadb/
   cp -r backups/rag_backup_[good_timestamp]/.chromadb/ rag/

   # Or use rag_data_attendant
   gemini skill invoke rag_data_attendant      --action restore      --backup "backups/rag_backup_[timestamp]"
   ```

4. **Rebuild Index**
   ```bash
   gemini skill invoke rag_data_attendant      --action rebuild_index      --collections all
   ```

5. **Validate Restoration**
   ```bash
   # Test queries to ensure working
   gemini rag query --collection epsilon --query "internal locus"
   gemini rag query --collection legal --query "FCRA"
   gemini rag query --collection business --query "n8n"
   ```

6. **Document Incident**
   - Log what happened in decisions/incident_log.md
   - Note root cause
   - Document fix applied
   - Add prevention measure

### Prevention Measures
- Always backup before major operations
- Test on small scale before bulk operations
- Review autonomous execution logs after completion
- Maintain multiple backup generations
- Keep at least 3 most recent backups

## Workflow 7: Cross-System Knowledge Integration

### Scenario
User discovers valuable knowledge during Perplexity conversation that should be in RAG

### Flow
1. **User Recognizes Value**
   - Perplexity surfaced useful framework
   - Web research revealed important pattern
   - User conversation revealed case study

2. **User Decides to Persist**
   ```
   "Add this to RAG for future reference"
   ```

3. **Perplexity Provides Capture Command**
   ```
   "Create a file to add this:

   gemini skill invoke knowledge_base_curator      --action manual_add      --content '[key points from conversation]'      --domain [epsilon|legal|business]      --classification [type]      --tier [1|2|3]      --source 'Perplexity conversation [date]'

   Or create manually:
   - File: rag/[domain]/[descriptive_name].md
   - Include metadata header
   - Add content
   - Then: gemini skill invoke rag_data_attendant --action rebuild_index"
   ```

4. **User Executes Capture**

5. **Knowledge Now Available**
   - In future Perplexity sessions (via RAG query)
   - For skill training
   - For autonomous retrieval

This creates feedback loop: Good conversation → Persistent knowledge → Better future conversations
