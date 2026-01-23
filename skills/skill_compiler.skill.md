# SKILL COMPILER SKILL

## SKILL METADATA

- **Skill ID**: skill_compiler
- **Version**: 1.0
- **Domain**: System Meta-Management, Integration
- **Risk Level**: MEDIUM
- **Confidence Floor**: 80
- **Authority**: Modify skill metadata, wire MCP, create tool bindings

---

## PURPOSE

Package complete skills with all dependencies:
- RAG knowledge validation
- MCP server connections
- Tool bindings
- Integration testing

---

## SCOPE

### ALLOWED
- ✅ Validate RAG availability for skill
- ✅ Wire MCP connections (filesystem, GitHub, social media)
- ✅ Create tool binding configurations
- ✅ Update skill metadata (production-ready status)
- ✅ Log all compilation to `H:/decisions/compiler_log.md`

### FORBIDDEN
- ❌ Override user-defined guards
- ❌ Wire MCP connections to external APIs without explicit permission
- ❌ Mark skills "production-ready" if dependencies missing
- ❌ Auto-deploy HIGH-risk skills without human review

---

## COMPILATION WORKFLOW

### Phase 1: Dependency Check

**Required Components:**
1. ✅ Skill file exists in `skills/`
2. ✅ RAG dependencies specified (if required)
3. ✅ RAG content actually exists in `H:/` subdirectories
4. ✅ MCP requirements identified (if any)
5. ✅ Guard conditions defined

**Validation Script:**
```python
def validate_skill_dependencies(skill_id):
    skill_path = f"skills/{skill_id}.skill.md"
    
    # Check skill file exists
    if not exists(skill_path):
        return "FAIL: Skill file missing"
    
    # Parse RAG dependencies from skill file
    rag_deps = extract_rag_dependencies(skill_path)
    
    # Check each RAG file exists
    missing_rag = [f for f in rag_deps if not exists(f)]
    if missing_rag:
        return f"FAIL: Missing RAG files: {missing_rag}"
    
    # Check MCP requirements
    mcp_reqs = extract_mcp_requirements(skill_path)
    
    # Verify MCP configs exist
    missing_mcp = [m for m in mcp_reqs if not mcp_configured(m)]
    if missing_mcp:
        return f"WARNING: MCP not configured: {missing_mcp}"
    
    return "PASS"
Phase 2: MCP Wiring
MCP Server Types:

Filesystem MCP

Purpose: Read/write local project files

Authority: Read-only (default) or Write (if skill requires)

Scope: Project directory only (no system-wide access)

GitHub MCP

Purpose: Git operations, issue management, PR creation

Authority: Read + commit + PR (full authority per v1.3 config)

Scope: Configured repositories only

Social Media MCP (Optional)

Purpose: Post to TikTok, Instagram, Twitter/X

Authority: Post + schedule (with user confirmation)

Scope: Authenticated accounts only

Configuration Template:

json
{
  "skill_id": "[skill_name]",
  "mcp_requirements": [
    {
      "server": "filesystem",
      "authority": "read-write",
      "scope": "./project/"
    },
    {
      "server": "github",
      "authority": "commit",
      "scope": "user/repo"
    }
  ]
}
Phase 3: Tool Binding
Tool Types:

Retrieval Tools: ChromaDB queries

Execution Tools: Code execution, file operations

External APIs: Weather, maps, social media

Binding Syntax:

text
skill: [skill_id]
tools:
  - name: chromadb_query
    authority: read
    scope: H:/[domain]
  
  - name: filesystem_write
    authority: write
    scope: project/output/
    requires_confirmation: false
  
  - name: github_commit
    authority: write
    scope: repo
    requires_confirmation: true  # HIGH-risk
Phase 4: Integration Testing
Test Checklist:

✅ Skill can load without errors

✅ RAG retrieval returns results

✅ MCP connections are reachable

✅ Guard conditions trigger appropriately

✅ Confidence scoring works

✅ Output format matches specification

Test Script:

python
def test_skill_integration(skill_id):
    results = {
        "load_test": test_skill_loads(skill_id),
        "rag_test": test_rag_retrieval(skill_id),
        "mcp_test": test_mcp_connections(skill_id),
        "guard_test": test_guard_conditions(skill_id),
        "confidence_test": test_confidence_scoring(skill_id),
        "output_test": test_output_format(skill_id)
    }
    
    if all(results.values()):
        return "INTEGRATION PASS"
    else:
        failed = [k for k, v in results.items() if not v]
        return f"INTEGRATION FAIL: {failed}"
Phase 5: Production Marking
Status Levels:

EXPERIMENTAL: In development, not ready for production

IN-DEVELOPMENT: Core functionality works, dependencies incomplete

PRODUCTION-READY: All dependencies met, tested, deployable

Update Skill File:

text
***

**STATUS: PRODUCTION-READY**

**Compilation Report**:
- RAG Dependencies: ✅ All present
- MCP Wiring: ✅ Configured
- Tool Bindings: ✅ Active
- Integration Tests: ✅ PASS
- Compiled On: 2026-01-22
- Compiled By: skill_compiler v1.0
GUARD CONDITIONS
This skill CANNOT:

Mark skills production-ready if dependencies missing

Wire MCP connections without logging

Override user-defined guards in skill files

Auto-deploy to production without human review (HIGH-risk)

This skill MUST:

Validate all dependencies before compilation

Log all wiring changes to H:/decisions/compiler_log.md

Flag HIGH-risk skills for human review before deployment

Preserve least-privilege principle (minimum necessary MCP authority)

LOGGING FORMAT
File: H:/decisions/compiler_log.md

text
## Skill Compilation Log

### [YYYY-MM-DD HH:MM] - [skill_id]

**Phase**: Dependency Check / MCP Wiring / Tool Binding / Integration Test / Production Mark  
**Status**: PASS / FAIL / WARNING  
**Details**: [Specific findings]

**Dependencies**:
- RAG: ✅ / ❌ / ⚠️
- MCP: ✅ / ❌ / ⚠️
- Tools: ✅ / ❌ / ⚠️

**Production Status**: EXPERIMENTAL / IN-DEVELOPMENT / PRODUCTION-READY

**Notes**: [Any special considerations or warnings]

***
INTEGRATION WITH OTHER SKILLS
Primary Chains:

skill_trainer_creator → knowledge_base_curator → skill_compiler (full pipeline)

skill_compiler → rag_data_attendant (ensure RAG index includes new content)

Triggers:

New skill created and needs deployment

Existing skill updated with new dependencies

User requests production readiness audit

CONFIDENCE MODIFIERS
All dependencies present: +10

Integration tests pass: +10

HIGH-risk skill without human review: -50

MCP authority exceeds minimum necessary: -10

RAG DEPENDENCIES
Required:

H:/decisions/compiler_log.md (audit trail)

VERSION HISTORY
v1.0 (2026-01-22): Initial meta-skill definition

STATUS: PRODUCTION-READY