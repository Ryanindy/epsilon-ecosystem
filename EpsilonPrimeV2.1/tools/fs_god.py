import os
import platform
import subprocess
import sys
import urllib.request
from typing import List, Optional

def scan_host_drives() -> List[str]:
    """
    Scans the host system for all available storage drives and mount points.
    Returns a list of drive letters (Windows) or mount points (Linux/Mac).
    """
    system = platform.system()
    drives = []

    if system == "Windows":
        try:
            output = subprocess.check_output(['wmic', 'logicaldisk', 'get', 'caption'], text=True)        
            for line in output.split('\n'):
                if ':' in line:
                    drives.append(line.strip())
        except Exception:
            pass
    else:
        try:
            output = subprocess.check_output(['df', '-h'], text=True)
            for line in output.split('\n')[1:]:
                parts = line.split()
                if len(parts) >= 6:
                    mount = parts[-1]
                    if mount.startswith(('/mnt', '/media', '/Volumes')) or mount == '/':
                        drives.append(mount)
        except Exception:
            pass
    return drives

def force_read_file(path: str) -> str:
    """
    Reads the content of any file on the host system, bypassing project-level restrictions.
    Use this only when authorized by the Jack Protocol.
    """
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        return f"Error: Unable to read file at {path}. {str(e)}"

def force_write_file(path: str, content: str) -> str:
    """
    Writes content to any location on the host system. 
    WARNING: This is a Jack-level execution tool. It can overwrite system files.
    """
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Success: File written to {path}"
    except Exception as e:
        return f"Error: Unable to write to {path}. {str(e)}"

def list_host_directory(path: str) -> str:
    """
    Lists the contents of any directory on the host system.
    """
    try:
        items = os.listdir(path)
        return "\n".join(items)
    except Exception as e:
        return f"Error: Unable to list directory {path}. {str(e)}"

def download_to_host(url: str, dest_path: str) -> str:
    """
    Downloads a file from a URL directly to the host system at the specified path.
    """
    try:
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        urllib.request.urlretrieve(url, dest_path)
        return f"Success: Downloaded {url} to {dest_path}"
    except Exception as e:
        return f"Error: Failed to download from {url}. {str(e)}"

def inject_and_run(command: str, working_dir: Optional[str] = None) -> str:
    """
    Injects and executes a shell command on the host system. 
    WARNING: This allows remote code execution. Use with extreme caution.
    """
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=working_dir)
        return f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}\nExit Code: {result.returncode}"
    except Exception as e:
        return f"Error: Failed to execute command. {str(e)}"

def inject_python_script(script_content: str, script_name: str = "payload.py") -> str:
    """
    Writes a python script to the host and executes it using the current interpreter.
    """
    try:
        with open(script_name, 'w', encoding='utf-8') as f:
            f.write(script_content)
        result = subprocess.run([sys.executable, script_name], capture_output=True, text=True)
        os.remove(script_name) # Cleanup
        return f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    except Exception as e:
        return f"Error: Python injection failed. {str(e)}"