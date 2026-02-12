# N8N ARCHITECT SKILL

## SKILL METADATA
- **Skill ID**: n8n_architect
- **Version**: 1.0
- **Domain**: Automation / DevOps
- **Risk Level**: MEDIUM (Modifies Production Workflows)
- **Confidence Floor**: 80
- **Tools**: `n8n_manager.py`

---

## PURPOSE
Manage the local n8n automation server. Create, list, and activate workflows directly from the CLI.

---

## CAPABILITIES

### 1. List Workflows
**Action**: `list`
**Command**: `python n8n_manager.py list`
**Description**: Shows all workflows, their IDs, and active status.

### 2. Create Workflow
**Action**: `create`
**Command**: `python n8n_manager.py create --name "{name}" --file "{json_file_path}"`
**Description**: Uploads a JSON workflow definition to n8n.
**Pre-requisite**: You must have the JSON content saved to a file first.

### 3. Activate/Deactivate
**Action**: `activate` / `deactivate`
**Command**: `python n8n_manager.py activate --id "{id}"`
**Description**: Toggles the production state of a workflow.

---

## USAGE EXAMPLES

**User**: "Show me my n8n workflows."
**Agent**: 
1. `python n8n_manager.py list`

**User**: "Deploy this JSON as 'Email Scraper'."
**Agent**:
1. `write_file(content=json_data, file_path="temp_workflow.json")`
2. `python n8n_manager.py create --name "Email Scraper" --file "temp_workflow.json"`
3. `run_shell_command("del temp_workflow.json")`

---

## DEPENDENCIES
- `requests` python library
- n8n instance running at `http://localhost:5678` (default)
- API Key (embedded or env var)

**STATUS: ACTIVE**
