#!/usr/bin/env python3
import sys
import os
import subprocess
import platform
import shutil

def main():
    if len(sys.argv) < 2:
        sys.exit(0)

    hook_name = sys.argv[1]
    extra_args = sys.argv[2:]
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ext_dir = os.path.dirname(script_dir)
    hooks_dir = os.path.join(ext_dir, "hooks")
    is_windows = "windows" in platform.system().lower()

    if is_windows:
        script_path = os.path.join(hooks_dir, f"{hook_name}.ps1")
        exe = shutil.which('pwsh') or shutil.which('powershell')
        cmd = [exe, "-NoProfile", "-NoLogo", "-ExecutionPolicy", "Bypass", "-File", script_path] + extra_args
    else:
        script_path = os.path.join(hooks_dir, f"{hook_name}.sh")
        cmd = ["bash", script_path] + extra_args

    if not os.path.exists(script_path):
        print('{"decision": "allow"}')
        sys.exit(0)

    try:
        env = os.environ.copy()
        env["EXTENSION_DIR"] = ext_dir
        
        # WE SKIP STDIN READING COMPLETELY FOR NOW
        result = subprocess.run(
            cmd,
            text=True,
            capture_output=True,
            env=env,
            timeout=10
        )
        
        stdout = result.stdout.strip() if result.stdout else ""
        if stdout:
            import re
            json_match = re.search(r'\{.*"decision".*\}', stdout, re.DOTALL)
            if json_match:
                print(json_match.group(0))
            else:
                print('{"decision": "allow"}')
        else:
            print('{"decision": "allow"}')
            
    except Exception:
        print('{"decision": "allow"}')
        
    sys.exit(0)

if __name__ == "__main__":
    main()
