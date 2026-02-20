import subprocess
import sys
import os
import time
import re

ROOT_DIR = "C:/Users/Media Server/EpsilonPrimeV2.1"
TARGET_FILE = sys.argv[1] if len(sys.argv) > 1 else "main_server.py"
BRIDGE_CMD = [sys.executable, os.path.join(ROOT_DIR, TARGET_FILE)]
LOG_FILE = os.path.join(ROOT_DIR, f"{TARGET_FILE.split('.')[0]}_healer.log")

# Known error patterns and their fixes
PATCH_RULES = [
    {
        "pattern": r"NameError: name '(\w+)' is not defined",
        "action": "inject_import"
    },
    {
        "pattern": r"ModuleNotFoundError: No module named '(\w+)'",
        "action": "pip_install"
    }
]

def log(msg):
    try:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{timestamp}] {msg}"
        print(line)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception as e:
        print(f"Logging error: {e}")

def apply_fix(error_text):
    log("Analyzing failure...")
    
    # Check for NameError (Missing Import)
    match = re.search(r"NameError: name '(\w+)' is not defined", error_text)
    if match:
        missing_name = match.group(1)
        # Try to find which file crashed
        file_match = re.findall(r'File "(.*?)", line (\d+)', error_text)
        if file_match:
            target_file, line_num = file_match[-1]
            log(f"Detected missing name '{missing_name}' in {target_file} at line {line_num}")
            
            # Simple injection: Add 'import [name]' at the top
            with open(target_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            if f"import {missing_name}" not in content:
                log(f"Injecting 'import {missing_name}' into {target_file}")
                with open(target_file, "w", encoding="utf-8") as f:
                    f.write(f"import {missing_name}\n" + content)
                return True
                
    # Check for ModuleNotFoundError
    match = re.search(r"ModuleNotFoundError: No module named '(\w+)'", error_text)
    if match:
        module_name = match.group(1)
        log(f"Detected missing module: {module_name}. Attempting pip install...")
        subprocess.run([sys.executable, "-m", "pip", "install", module_name])
        return True

    return False

def run_bridge():
    while True:
        log("Launching Epsilon Bridge...")
        try:
            process = subprocess.Popen(
                BRIDGE_CMD,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                encoding="utf-8"
            )

            error_accumulator = []
            
            # Monitor stderr for crashes
            while True:
                line = process.stderr.readline()
                if not line:
                    break
                print(f"[BRIDGE_ERR] {line.strip()}")
                error_accumulator.append(line)
                
                # If we see a traceback end, try to fix
                if "Error:" in line or "Exception:" in line:
                    full_error = "".join(error_accumulator)
                    if apply_fix(full_error):
                        log("Fix applied. Killing stale process and restarting...")
                        process.terminate()
                        time.sleep(2)
                        break # Restart loop
                    
            exit_code = process.wait()
            log(f"Bridge exited with code {exit_code}")
        except Exception as e:
            log(f"Process management error: {e}")
            
        time.sleep(5) # Cooldown before restart

if __name__ == "__main__":
    log("--- HEALER STARTUP ---")
    run_bridge()
