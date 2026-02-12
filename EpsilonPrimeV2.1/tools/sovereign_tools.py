import os
import shutil
import subprocess
from datetime import datetime
from smolagents import tool

@tool
def list_directory(path: str = ".") -> str:
    """
    Lists the contents of a directory in the Epsilon workspace.
    Args:
        path: The relative path to list. Defaults to root.
    """
    try:
        items = os.listdir(path)
        return "\n".join(items)
    except Exception as e:
        return f"Error: {e}"

@tool
def read_file(path: str) -> str:
    """
    Reads the content of a file in the Epsilon workspace.
    Args:
        path: The relative path to the file.
    """
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        return f"Error: {e}"

@tool
def write_file(path: str, content: str) -> str:
    """
    Writes content to a file in the Epsilon workspace.
    Args:
        path: The relative path to the file.
        content: The text content to write.
    """
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Success: Written to {path}"
    except Exception as e:
        return f"Error: {e}"

@tool
def git_sync() -> str:
    """
    Stages, commits, and pushes all changes in the current repository.
    """
    try:
        subprocess.run(["git", "add", "."], check=True)
        msg = f"Epsilon Sovereign Sync: {datetime.now().isoformat()}"
        subprocess.run(["git", "commit", "-m", msg], check=True)
        subprocess.run(["git", "push"], check=True)
        return "Git Sync and Push successful."
    except Exception as e:
        return f"Git Sync failed: {e}"

@tool
def shell_command(command: str) -> str:
    """
    Executes a raw shell command on the host system. Use with caution.
    Args:
        command: The command to execute.
    """
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
    except Exception as e:
        return f"Execution Error: {e}"

from tools.browser_tools import visit_webpage, search_web
from tools.browser_mcp import playwright_mcp

# Collection of all sovereign tools
SOVEREIGN_TOOLSET = [list_directory, read_file, write_file, git_sync, shell_command, visit_webpage, search_web, playwright_mcp]