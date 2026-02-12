import sys
import json
import logging
import subprocess
import os
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, stream=sys.stderr, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("epsilon_git_mcp")

def run_sync():
    """Runs the daily sync process for Epsilon Prime V2.1."""
    try:
        # Note: We are in /mcp, so project root is ..
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        os.chdir(root_dir)

        # 1. Update Index (Placeholder for V2.1 Indexer)
        # subprocess.run([sys.executable, "tools/reindex.py"], check=True)

        # 2. Git operations
        subprocess.run(["git", "add", "."], check=True)

        status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        if status.stdout.strip():
            msg = f"Epsilon V2.1 Auto-sync: {datetime.now().isoformat()}"
            subprocess.run(["git", "commit", "-m", msg], check=True)

            res = subprocess.run(["git", "push"], capture_output=True)
            if res.returncode == 0:
                return "Sync and Push successful."
            else:
                return "Committed locally. Push failed."
        else:
            return "No changes to sync."

    except Exception as e:
        return f"Sync failed: {str(e)}"

def mcp_loop():
    """Standard IO MCP Loop for Gemini CLI"""
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break

            request = json.loads(line)
            response = None

            if request.get("method") == "initialize":
                response = {
                    "jsonrpc": "2.0",
                    "id": request["id"],
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "serverInfo": {"name": "epsilon-git-sync", "version": "2.1"},
                        "capabilities": {
                            "tools": {
                                "sync_epsilon_v2": {
                                    "description": "Commits and Pushes the Epsilon Prime V2.1 state to GitHub",
                                    "inputSchema": {"type": "object", "properties": {}}
                                }
                            }
                        }
                    }
                }

            elif request.get("method") == "tools/call":
                if request["params"]["name"] == "sync_epsilon_v2":
                    result = run_sync()
                    response = {
                        "jsonrpc": "2.0",
                        "id": request["id"],
                        "result": {
                            "content": [{"type": "text", "text": result}]
                        }
                    }

            if response:
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()

        except Exception as e:
            logger.error(f"Error: {e}")

if __name__ == "__main__":
    mcp_loop()
