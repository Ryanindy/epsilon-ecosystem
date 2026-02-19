import os
import shutil
import subprocess
import shlex
import re
import logging
from datetime import datetime
from smolagents import tool

# --- LOGGING ---
logger = logging.getLogger("SovereignTools")

# --- SHELL COMMAND SECURITY ---
# Blocked patterns that could be dangerous
BLOCKED_SHELL_PATTERNS = [
    r'rm\s+-rf\s+/',        # rm -rf /
    r'rm\s+-rf\s+~',        # rm -rf ~
    r'mkfs\.',              # filesystem formatting
    r'dd\s+if=',            # disk destroyer
    r':\(\)\{',             # fork bomb
    r'>\s*/dev/sd',         # write to raw device
    r'chmod\s+-R\s+777\s+/',  # dangerous permissions
    r'\|\s*sh\b',           # piping to shell
    r'\|\s*bash\b',         # piping to bash
    r'curl.*\|\s*sh',       # curl pipe to shell
    r'wget.*\|\s*sh',       # wget pipe to shell
    r'eval\s+',             # eval command
    r'`.*`',                # command substitution (backticks)
    r'\$\(.*\)',            # command substitution
]

def is_command_safe(command: str) -> tuple[bool, str]:
    """Validates a shell command against security patterns."""
    command_lower = command.lower()
    for pattern in BLOCKED_SHELL_PATTERNS:
        if re.search(pattern, command_lower):
            return False, f"Blocked pattern detected: {pattern}"
    return True, "OK"

# --- CORE FILE SYSTEM & SHELL TOOLS ---
@tool
def list_directory(path: str = ".") -> str:
    """
    Lists the contents of a specified directory.
    
    Args:
        path: The path of the directory to list. Defaults to the current directory.
    """
    try:
        return "\n".join(os.listdir(path))
    except Exception as e:
        return f"Error: {e}"

@tool
def read_file(path: str) -> str:
    """
    Reads and returns the text content of a file.
    
    Args:
        path: The path to the file to be read.
    """
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        return f"Error: {e}"

@tool
def write_file(path: str, content: str) -> str:
    """
    Writes content to a file at the specified path.
    
    Args:
        path: The path where the file will be written.
        content: The text content to write into the file.
    """
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Success: Written to {path}"
    except Exception as e:
        return f"Error: {e}"

@tool
def shell_command(command: str) -> str:
    """
    Executes a shell command and returns the output.
    Commands are validated against security patterns before execution.

    Args:
        command: The shell command to be executed.
    """
    # Security validation
    is_safe, reason = is_command_safe(command)
    if not is_safe:
        logger.warning(f"BLOCKED shell command: {command} - Reason: {reason}")
        return f"Security Error: Command blocked - {reason}"

    try:
        # Use shell=False with shlex.split for safer execution where possible
        # Fall back to shell=True only for complex commands with pipes/redirects
        if any(c in command for c in ['|', '>', '<', '&&', '||', ';']):
            # Complex command - must use shell, but already validated
            logger.warning(f"EXECUTING COMPLEX SHELL COMMAND: {command}")
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
        else:
            # Simple command - use safer shell=False
            args = shlex.split(command)
            result = subprocess.run(
                args,
                shell=False,
                capture_output=True,
                text=True,
                timeout=300
            )

        output = f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        if result.returncode != 0:
            output += f"\nReturn Code: {result.returncode}"
        return output
    except subprocess.TimeoutExpired:
        return "Execution Error: Command timed out after 5 minutes"
    except Exception as e:
        logger.error(f"Shell command failed: {e}")
        return f"Execution Error: {e}"

# --- GIT & VERSION CONTROL TOOLS ---
@tool
def git_sync(commit_message: str) -> str:
    """
    Stages all changes, commits them with the provided message, and pushes to the remote repository.
    
    Args:
        commit_message: The message to use for the git commit.
    """
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push"], check=True)
        return "Git Sync and Push successful."
    except Exception as e:
        return f"Git Sync failed: {e}"

# --- MODULAR TOOLSETS ---
# Import tools from other modules
from tools.browser_tools import BROWSER_TOOLSET
from tools.wholesale.wholesale_tools import WHOLESALE_TOOLSET
from tools.osint_tools import OSINT_TOOLSET

# Define role-based toolsets
FILESYSTEM_TOOLSET = [list_directory, read_file, write_file, shell_command]
VERSION_CONTROL_TOOLSET = [git_sync]
# The 'coder-rick' agent gets everything dangerous
CODER_TOOLSET = FILESYSTEM_TOOLSET + VERSION_CONTROL_TOOLSET + BROWSER_TOOLSET + WHOLESALE_TOOLSET + OSINT_TOOLSET

# The 'researcher-lyra' agent only gets read-only and web tools
RESEARCHER_TOOLSET = [list_directory, read_file] + BROWSER_TOOLSET + OSINT_TOOLSET

# The master toolset for the top-level agent if no sub-agent is selected
SOVEREIGN_TOOLSET = CODER_TOOLSET 
