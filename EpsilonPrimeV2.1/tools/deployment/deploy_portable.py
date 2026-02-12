import os
import shutil
import re
import sys
import codecs

# Configuration
SOURCE_ROOT = r"C:/Users/Media Server"
# Default Destination
DEST_ROOT = r"C:/Users/Media Server/Desktop/Epsilon Portable v2"

# STRICT WHITELIST
# Only these files/folders in the root will be copied.
ALLOWED_ROOT_FILES = {
    "BOOT.py", "main.py", "chat.py", "gemini.bat", "requirements.txt", 
    "BOOT.md", "README.md", "GEMINI.md", "EPSILON_PRIME_MASTER_README.md",
    "agentic_bridge_workflow.json", "cleaned_workflow.json", "existing_workflows.json",
    "memory_engine.py", "rag_retrieval.py", "n8n_manager.py", "n8n_api_manager.py",
    "safety_scoring.py", "extract_and_save.py", "fix_json.py", "god_importer.py",
    "generate_rag_index.py", "update_session_rag.py", "_PROJECT_MAP.json",
    "persona_prompt.py", "sms_handler.py", "init_db.py"
}

ALLOWED_ROOT_DIRS = {
    ".gemini", "rag", "skills", "flows", "src_templates", "ui", "tools"
}

IGNORE_IN_DIRS = {
    ".git", "__pycache__", "tmp", "sessions", "node_modules", "venv", "$RECYCLE.BIN", "RECYCLE.BIN",
    "antigravity-browser-profile", "Stealth", "node_modules", "dist", "build", "archives", "SOF", ".venv"
}

# Hot-Patching Rules
REPLACEMENTS = [
    # BOOT.py specific fix
    (r'SYSTEM_ROOT = "C:/Users/Media Server/"', 'import os; SYSTEM_ROOT = os.path.dirname(os.path.abspath(__file__)).replace(chr(92), "/") + "/"'),
    # General Python Absolute Path Fix
    (r'C:\\Users\\Media Server', '.'),
    (r'C:/Users/Media Server', '.'),
    # Batch file fixes
    (r'python "C:\\Users\\Media Server\\', 'python "%~dp0'),
    (r'python "C:/Users/Media Server/', 'python "%~dp0'),
]

def on_rm_error(func, path, exc_info):
    import stat
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception as e:
        print(f"⚠️  Failed to delete {path}: {e}")

def hot_patch_content(content, filename):
    for pattern, replacement in REPLACEMENTS:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    if filename == "gemini.bat":
        content = re.sub(r'cd /d "C:\\Users\\Media Server"', 'cd /d "%~dp0"', content)
    return content

def copy_recursive(src, dest):
    if os.path.basename(src) in IGNORE_IN_DIRS:
        return 0, 0
        
    if not os.path.exists(dest):
        os.makedirs(dest)
        
    files_copied = 0
    files_patched = 0
    
    for item in os.listdir(src):
        if item in IGNORE_IN_DIRS:
            continue
            
        if files_copied % 100 == 0 and files_copied > 0:
            print(f"   ... Copied {files_copied} files in {os.path.basename(src)}")

        s = os.path.join(src, item)
        d = os.path.join(dest, item)
        
        try:
            if os.path.isdir(s):
                c, p = copy_recursive(s, d)
                files_copied += c
                files_patched += p
            else:
                # Copy/Patch File
                if item.lower().endswith((".png", ".jpg", ".exe", ".dll", ".zip", ".db", ".pdf", ".pyc", ".bin", ".dat", ".idx", ".parquet", ".pkl", ".sqlite")):
                    shutil.copy2(s, d)
                    files_copied += 1
                else:
                    try:
                        with open(s, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        patched = hot_patch_content(content, item)
                        if content != patched:
                            files_patched += 1
                        
                        with open(d, 'w', encoding='utf-8') as f:
                            f.write(patched)
                        files_copied += 1
                    except UnicodeDecodeError:
                        shutil.copy2(s, d)
                        files_copied += 1
        except Exception as e:
            print(f"❌ Error processing {s}: {e}")
            
    return files_copied, files_patched

def deploy(dest_dir):
    print(f"🚀 Starting deployment to: {dest_dir}")
    if os.path.exists(dest_dir):
        print(f"⚠️  Cleaning existing directory...")
        shutil.rmtree(dest_dir, onerror=on_rm_error)
    os.makedirs(dest_dir, exist_ok=True)
    
    total_copied = 0
    total_patched = 0
    
    # 1. Copy Root Files (Whitelist)
    print("📦 Copying Root Files...")
    for f in ALLOWED_ROOT_FILES:
        src = os.path.join(SOURCE_ROOT, f)
        if os.path.exists(src):
            try:
                # Try reading as text to hot-patch
                with open(src, 'r', encoding='utf-8') as fin:
                    content = fin.read()
                patched = hot_patch_content(content, f)
                if content != patched:
                    total_patched += 1
                with open(os.path.join(dest_dir, f), 'w', encoding='utf-8') as fout:
                    fout.write(patched)
                total_copied += 1
            except UnicodeDecodeError:
                # Binary Fallback (Copy raw)
                shutil.copy2(src, os.path.join(dest_dir, f))
                total_copied += 1
            except Exception as e:
                print(f"❌ Failed to copy root file {f}: {e}")
    
    # 2. Copy Root Dirs (Recursive)
    print("📂 Copying Directories...")
    for d in ALLOWED_ROOT_DIRS:
        src = os.path.join(SOURCE_ROOT, d)
        if os.path.exists(src):
            c, p = copy_recursive(src, os.path.join(dest_dir, d))
            total_copied += c
            total_patched += p

    print(f"✅ Deployment Complete.")
    print(f"   Files Copied: {total_copied}")
    print(f"   Files Hot-Patched: {total_patched}")
    
    create_launchers(dest_dir)

def create_launchers(dest_dir):
    print("🛠️  Creating Launchers...")
    
    # Python Embed Setup
    embed_dir = os.path.join(dest_dir, "python_embed")
    os.makedirs(embed_dir, exist_ok=True)
    with open(os.path.join(embed_dir, "PLACE_PYTHON_HERE.txt"), 'w', encoding='utf-8') as f:
        f.write("Download Windows x86-64 embeddable package from python.org and extract contents here.")

    # Node Embed Setup
    node_dir = os.path.join(dest_dir, "node_embed")
    os.makedirs(node_dir, exist_ok=True)
    with open(os.path.join(node_dir, "PLACE_NODE_HERE.txt"), 'w', encoding='utf-8') as f:
        f.write("Download Node.js Windows Binary (.zip) -> 'node-vXX-win-x64' and extract contents here (node.exe should be in this folder).")
    
    # n8n Data Setup
    n8n_dir = os.path.join(dest_dir, "n8n_data")
    os.makedirs(n8n_dir, exist_ok=True)

    # Launch Script (Windows)
    # Using utf-8 explicitly to handle emojis
    bat_content = r"""@echo off
TITLE Epsilon Prime Portable
:: 1. Python Setup
IF EXIST "%~dp0python_embed\python.exe" (
    SET "PYTHONHOME=%~dp0python_embed"
    SET "PATH=%~dp0python_embed;%~dp0python_embed\Scripts;%PATH%"
    SET "PY_EXE=%~dp0python_embed\python.exe"
) ELSE (
    SET "PY_EXE=python"
)

:: 2. Node.js Setup (for MCP/n8n)
IF EXIST "%~dp0node_embed\node.exe" (
    SET "PATH=%~dp0node_embed;%PATH%"
)

:: 3. n8n Configuration (Portable Data)
SET "N8N_USER_FOLDER=%~dp0n8n_data"
SET "N8N_ENCRYPTION_KEY=epsilon_portable_key"

:: 4. Database Init
IF NOT EXIST "%~dp0memory.db" (
    ECHO [INFO] Initializing Memory Database...
    "%PY_EXE%" "%~dp0init_db.py"
)

:: Execute Bootloader
"%PY_EXE%" "%~dp0BOOT.py"
IF %ERRORLEVEL% NEQ 0 (
    ECHO [ERROR] Boot Sequence Failed.
    PAUSE
    EXIT /B %ERRORLEVEL%
)

:: Execute Main Interface
"%PY_EXE%" "%~dp0chat.py"
PAUSE
"""
    with open(os.path.join(dest_dir, "_LAUNCH_EPSILON.bat"), 'w', encoding='utf-8') as f:
        f.write(bat_content)
    with open(os.path.join(dest_dir, "launch_epsilon.bat"), 'w', encoding='utf-8') as f:
        f.write(bat_content)

    # Launch Script (Linux)
    sh_content = r"""#!/bin/bash
DIR=\"$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )\" 

# 1. Python Setup
if [ -f "$DIR/python_embed/python" ]; then
    export PYTHONHOME="$DIR/python_embed"
    export PATH="$DIR/python_embed:$PATH"
    PY_EXE="$DIR/python_embed/python"
else
    PY_EXE="python3"
fi

# 2. Node.js Setup
if [ -f "$DIR/node_embed/node" ]; then
    export PATH="$DIR/node_embed:$PATH"
fi

# 3. n8n Setup
export N8N_USER_FOLDER="$DIR/n8n_data"

# 4. Database Init
if [ ! -f "$DIR/memory.db" ]; then
    echo "[INFO] Initializing Memory Database..."
    "$PY_EXE" "$DIR/init_db.py"
fi

# Execute Bootloader
"$PY_EXE" "$DIR/BOOT.py"
if [ $? -eq 0 ]; then
    "$PY_EXE" "$DIR/chat.py"
else
    echo "[ERROR] Boot Sequence Failed."
fi
"""
    with open(os.path.join(dest_dir, "_LAUNCH_EPSILON.sh"), 'w', newline='\n', encoding='utf-8') as f:
        f.write(sh_content)
    with open(os.path.join(dest_dir, "launch_epsilon.sh"), 'w', newline='\n', encoding='utf-8') as f:
        f.write(sh_content)

if __name__ == "__main__":
    target = DEST_ROOT
    if len(sys.argv) > 1:
        target = sys.argv[1]
    
    deploy(target)
