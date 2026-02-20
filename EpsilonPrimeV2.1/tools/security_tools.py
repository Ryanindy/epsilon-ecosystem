import subprocess
import json
import os
from smolagents import tool

@tool
def run_semgrep(target_path: str, rules: str = None) -> str:
    """
    Runs Semgrep static analysis on the specified target path with optional rules.
    Args:
        target_path: The file or directory path to scan (e.g., 'main_server.py', 'tools/').
        rules: Optional. A Semgrep ruleset ID or file path (e.g., 'p/python-security', 'path/to/my_rules.yml').
               If not provided, it defaults to a general security ruleset if available.
    Returns:
        A JSON string containing Semgrep findings or an error message.
    """
    command = ["semgrep", "--json", "--output", "-"]
    
    if rules:
        command.extend(["--config", rules])
    else:
        command.extend(["--config", "p/security-audit"])
        
    command.append(target_path)
    
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
            cwd=os.getcwd(),
            timeout=300
        )
        
        if result.returncode != 0 and "ERROR" in result.stderr.upper():
            return f"Semgrep Error: {result.stderr}\nSTDOUT: {result.stdout}"
        
        try:
            json_output = json.loads(result.stdout)
            return json.dumps(json_output, indent=2)
        except json.JSONDecodeError:
            return f"Semgrep Output (non-JSON):\n{result.stdout}\nSTDERR: {result.stderr}"
            
    except FileNotFoundError:
        return "Error: 'semgrep' command not found. Is it installed and in PATH?"
    except subprocess.TimeoutExpired:
        return f"Error: Semgrep scan for '{target_path}' timed out after 300 seconds."
    except Exception as e:
        return f"A general error occurred: {e}"

@tool
def direct_semgrep_scan(target_path: str, rules: str = None) -> str:
    """
    Directly executes the Semgrep command via subprocess, bypassing smolagents' tool registration.
    Use this if the standard run_semgrep tool is not being recognized.
    Args:
        target_path: The file or directory path to scan (e.g., 'main_server.py', 'tools/').
        rules: Optional. A Semgrep ruleset ID or file path (e.g., 'p/python-security', 'path/to/my_rules.yml').
               If not provided, it defaults to a 'p/security-audit' ruleset.
    Returns:
        A JSON string containing Semgrep findings or an error message.
    """
    command = ["semgrep", "--json", "--output", "-"]
    
    if rules:
        command.extend(["--config", rules])
    else:
        command.extend(["--config", "p/security-audit"])
        
    command.append(target_path)
    
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False, # Semgrep returns non-zero on findings, so don't check=True here
            cwd=os.getcwd(),
            timeout=300 # 5-minute timeout
        )
        
        if result.returncode != 0 and "ERROR" in result.stderr.upper():
            return f"Semgrep Error: {result.stderr}\nSTDOUT: {result.stdout}"
        
        try:
            json_output = json.loads(result.stdout)
            return json.dumps(json_output, indent=2)
        except json.JSONDecodeError:
            return f"Semgrep Output (non-JSON):\n{result.stdout}\nSTDERR: {result.stderr}"
            
    except FileNotFoundError:
        return "Error: 'semgrep' command not found. Is it installed and in PATH?"
    except subprocess.TimeoutExpired:
        return f"Error: Semgrep scan for '{target_path}' timed out after 300 seconds."
    except Exception as e:
        return f"A general error occurred: {e}"

SECURITY_TOOLSET = [run_semgrep, direct_semgrep_scan]
