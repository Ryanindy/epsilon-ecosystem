#!/usr/bin/env python3
import sys
import os
import subprocess
import platform
import shutil
import json

def log_error(message):
    """Logs error to stderr and optionally to a file."""
    print(f"Dispatcher Error: {message}", file=sys.stderr)
    try:
        # Attempt to log to the extension's debug.log
        ext_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        log_path = os.path.join(ext_dir, "debug.log")
        with open(log_path, "a") as f:
            from datetime import datetime
            f.write(f"[{datetime.now().isoformat()}] [dispatch_hook] {message}\n")
    except:
        pass

def main():
    if len(sys.argv) < 2:
        print("Usage: dispatch_hook.py <hook_name> [args...]", file=sys.stderr)
        sys.exit(1)

    hook_name = sys.argv[1]
    extra_args = sys.argv[2:]
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ext_dir = os.path.dirname(script_dir)
    hooks_dir = os.path.join(ext_dir, "hooks")
    is_windows = "windows" in platform.system().lower()

    # Determine script path and command
    if is_windows:
        script_path = os.path.join(hooks_dir, f"{hook_name}.ps1")
        exe = shutil.which('pwsh') or shutil.which('powershell')
        if not exe:
            log_error("PowerShell not found.")
            print('{"decision": "allow"}')
            sys.exit(0)
        cmd = [exe, "-NoProfile", "-NoLogo", "-ExecutionPolicy", "Bypass", "-File", script_path] + extra_args
    else:
        script_path = os.path.join(hooks_dir, f"{hook_name}.sh")
        cmd = ["bash", script_path] + extra_args

    if not os.path.exists(script_path):
        log_error(f"Hook script not found: {script_path}")
        print('{"decision": "allow"}')
        sys.exit(0)

    # Read stdin safely
    input_data = ""
    if not sys.stdin.isatty():
        try:
            input_data = sys.stdin.read()
        except Exception as e:
            log_error(f"Failed to read stdin: {e}")

    try:
        # Execute the hook script
        env = os.environ.copy()
        env["EXTENSION_DIR"] = ext_dir
        
        result = subprocess.run(
            cmd,
            input=input_data,
            text=True,
            capture_output=True,
            env=env,
            encoding="utf-8",
            errors="replace"
        )
        
        # Output handling - CLI ONLY WANTS THE JSON IN STDOUT
        stdout = result.stdout.strip() if result.stdout else ""
        
        # Log any stderr from the script to our own stderr for the user/CLI to capture if needed
        if result.stderr:
            print(result.stderr, file=sys.stderr)

        if stdout:
            # Try to find a JSON-like string in the output (in case of banners)
            import re
            json_match = re.search(r'\{.*"decision".*\}', stdout, re.DOTALL)
            if json_match:
                print(json_match.group(0))
            else:
                log_error(f"Hook {hook_name} output non-JSON: {stdout}")
                print('{"decision": "allow"}')
        else:
            if result.returncode != 0:
                log_error(f"Hook {hook_name} failed with code {result.returncode} and no output.")
            print('{"decision": "allow"}')
            
        sys.exit(0) 
        
    except Exception as e:
        log_error(f"Unexpected execution error: {e}")
        print('{"decision": "allow"}')
        sys.exit(0)

if __name__ == "__main__":
    main()