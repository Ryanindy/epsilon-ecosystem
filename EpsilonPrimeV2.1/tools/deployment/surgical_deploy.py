import os
import shutil
import re

# Configuration
SOURCE_ROOT = r"C:/Users/Media Server"
DEST_ROOT = r"C:/Users/Media Server/Desktop/Epsilon Portable v2"

# STRICT WHITELIST OF FILES
FILES_TO_COPY = [
    "BOOT.py", "main.py", "chat.py", "gemini.bat", "requirements.txt",
    "BOOT.md", "README.md", "GEMINI.md", "EPSILON_PRIME_MASTER_README.md",
    "memory_engine.py", "rag_retrieval.py", "n8n_manager.py", "n8n_api_manager.py",
    "safety_scoring.py", "extract_and_save.py", "fix_json.py", "god_importer.py",
    "generate_rag_index.py", "update_session_rag.py", "_PROJECT_MAP.json",
    "persona_prompt.py", "sms_handler.py"
]

# STRICT WHITELIST OF DIRECTORIES (Recursive)
DIRS_TO_COPY = [
    "rag", "skills", "flows", "src_templates", "ui", ".gemini/memory"
]

# Hot-Patching Rules
REPLACEMENTS = [
    (r'SYSTEM_ROOT = "C:/Users/Media Server/"', r'import os; SYSTEM_ROOT = os.path.dirname(os.path.abspath(__file__)).replace("\\\\", "/") + "/"'),
    (r'C:\\Users\\Media Server', '.'),
    (r'C:/Users/Media Server', '.'),
]

def hot_patch_content(content):
    for pattern, replacement in REPLACEMENTS:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    return content

def surgical_copy():
    print(f"🚀 Starting Surgical Build to: {DEST_ROOT}")
    
    # 1. Copy Files
    for file in FILES_TO_COPY:
        src = os.path.join(SOURCE_ROOT, file)
        dest = os.path.join(DEST_ROOT, file)
        if os.path.exists(src):
            print(f"  📄 Copying: {file}")
            try:
                with open(src, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                content = hot_patch_content(content)
                
                with open(dest, 'w', encoding='utf-8') as f:
                    f.write(content)
            except Exception as e:
                print(f"    ⚠️ Binary/Error (Copying raw): {file} ({e})")
                shutil.copy2(src, dest)
        else:
            print(f"    ❌ Missing: {file}")

    # 2. Copy Directories
    for d in DIRS_TO_COPY:
        src = os.path.join(SOURCE_ROOT, d)
        dest = os.path.join(DEST_ROOT, d)
        print(f"  📂 Copying Directory: {d}")
        
        if os.path.exists(src):
            # shutil.copytree is cleaner than manual walking for this purpose
            # We ignore .git and __pycache__ inside these specific folders
            if os.path.exists(dest):
                shutil.rmtree(dest)
            shutil.copytree(src, dest, ignore=shutil.ignore_patterns('*.pyc', '__pycache__', '.git', '$RECYCLE.BIN', 'node_modules'))
        else:
            print(f"    ❌ Missing Directory: {d}")

    # 3. Create Empties
    os.makedirs(os.path.join(DEST_ROOT, "python_embed"), exist_ok=True)
    os.makedirs(os.path.join(DEST_ROOT, "node_embed"), exist_ok=True)
    os.makedirs(os.path.join(DEST_ROOT, "n8n_data"), exist_ok=True)

    print("✅ Surgical Build Complete.")

if __name__ == "__main__":
    surgical_copy()
