import argparse
import requests
import json
import os
import sys

# Load Configuration
def get_config():
    # Fallback to hardcoded for local Epsilon setup
    return {
        "api_key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI5NTRhM2RhMS1mNjczLTQyODQtYjY3Zi1mNmVlMjAyM2MzMmMiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzU2NjI1MDI1fQ.4XXobU5XSH6jLa12A_s_SJnfp_2QxJ8esAfwxZ2B2sM",
        "base_url": "http://localhost:5678/api/v1"
    }

def get_headers():
    config = get_config()
    return {
        "X-N8N-API-KEY": config.get("api_key"),
        "Content-Type": "application/json"
    }

def get_base_url():
    return get_config().get("base_url", "http://localhost:5678/api/v1")

def list_workflows():
    base_url = get_base_url()
    try:
        url = f"{base_url}/workflows"
        response = requests.get(url, headers=get_headers())
        response.raise_for_status()
        workflows = response.json().get("data", [])
        print(f"Found {len(workflows)} workflows:")
        for w in workflows:
            status = "ACTIVE" if w['active'] else "inactive"
            print(f"- [{w['id']}] {w['name']} ({status})")
    except Exception as e:
        print(f"Error listing workflows: {e}")
        sys.exit(1)

def get_workflow(wf_id):
    base_url = get_base_url()
    try:
        url = f"{base_url}/workflows/{wf_id}"
        response = requests.get(url, headers=get_headers())
        response.raise_for_status()
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error getting workflow: {e}")
        sys.exit(1)

def create_workflow(name, json_file):
    base_url = get_base_url()
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            workflow_data = json.load(f)
        workflow_data['name'] = name
        url = f"{base_url}/workflows"
        response = requests.post(url, headers=get_headers(), json=workflow_data)
        response.raise_for_status()
        new_wf = response.json().get("data", {})
        print(f"Successfully created: {new_wf.get('name')} (ID: {new_wf.get('id')})")
    except Exception as e:
        if 'response' in locals() and hasattr(response, 'text'):
            print(f"Error creating workflow: {e} | Response: {response.text}")
        else:
            print(f"Error creating workflow: {e}")
        sys.exit(1)

def update_workflow(wf_id, json_file):
    base_url = get_base_url()
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            workflow_data = json.load(f)
        url = f"{base_url}/workflows/{wf_id}"
        response = requests.put(url, headers=get_headers(), json=workflow_data)
        response.raise_for_status()
        print(f"Successfully updated workflow: {wf_id}")
    except Exception as e:
        print(f"Error updating workflow: {e}")
        sys.exit(1)

def activate_workflow(wf_id):
    base_url = get_base_url()
    try:
        url = f"{base_url}/workflows/{wf_id}/activate"
        response = requests.post(url, headers=get_headers())
        response.raise_for_status()
        print(f"Success: Workflow {wf_id} activated.")
    except Exception as e:
        print(f"Error activating: {e}")
        sys.exit(1)

def deactivate_workflow(wf_id):
    base_url = get_base_url()
    try:
        url = f"{base_url}/workflows/{wf_id}/deactivate"
        response = requests.post(url, headers=get_headers())
        response.raise_for_status()
        print(f"Success: Workflow {wf_id} deactivated.")
    except Exception as e:
        print(f"Error deactivating: {e}")
        sys.exit(1)

def delete_workflow(wf_id):
    base_url = get_base_url()
    try:
        url = f"{base_url}/workflows/{wf_id}"
        response = requests.delete(url, headers=get_headers())
        response.raise_for_status()
        print(f"Success: Workflow {wf_id} deleted.")
    except Exception as e:
        print(f"Error deleting: {e}")
        sys.exit(1)

def trigger_webhook(path):
    try:
        url = f"http://localhost:5678/webhook/{path}"
        print(f"Triggering Webhook: {url}")
        response = requests.post(url, json={})
        response.raise_for_status()
        print(f"✅ Webhook triggered! Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="n8n Sovereign Manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_list = subparsers.add_parser("list")
    parser_get = subparsers.add_parser("get")
    parser_get.add_argument("--id", required=True)
    parser_create = subparsers.add_parser("create")
    parser_create.add_argument("--name", required=True)
    parser_create.add_argument("--file", required=True)
    parser_update = subparsers.add_parser("update")
    parser_update.add_argument("--id", required=True)
    parser_update.add_argument("--file", required=True)
    parser_activate = subparsers.add_parser("activate")
    parser_activate.add_argument("--id", required=True)
    parser_deactivate = subparsers.add_parser("deactivate")
    parser_deactivate.add_argument("--id", required=True)
    parser_delete = subparsers.add_parser("delete")
    parser_delete.add_argument("--id", required=True)
    parser_trigger = subparsers.add_parser("trigger")
    parser_trigger.add_argument("--path", required=True)

    args = parser.parse_args()

    if args.command == "list":
        list_workflows()
    elif args.command == "get":
        get_workflow(args.id)
    elif args.command == "create":
        create_workflow(args.name, args.file)
    elif args.command == "update":
        update_workflow(args.id, args.file)
    elif args.command == "activate":
        activate_workflow(args.id)
    elif args.command == "deactivate":
        deactivate_workflow(args.id)
    elif args.command == "delete":
        delete_workflow(args.id)
    elif args.command == "trigger":
        trigger_webhook(args.path)

if __name__ == "__main__":
    main()
