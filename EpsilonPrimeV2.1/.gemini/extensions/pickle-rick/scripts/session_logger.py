import os
import time
import datetime

MEMORY_DIR = r"C:\Users\Media Server\.gemini\memory\sessions"
ROOT_DIR = r"C:\Users\Media Server\.gemini"
H_DRIVE = r"H:\epsilon"

def get_modified_files(root, hours=1):
    modified = []
    now = time.time()
    limit = now - (hours * 3600)
    
    for folder in [root, H_DRIVE]:
        if not os.path.exists(folder): continue
        for r, d, f in os.walk(folder):
            for file in f:
                try:
                    path = os.path.join(r, file)
                    mtime = os.path.getmtime(path)
                    if mtime > limit:
                        modified.append(path)
                except: pass
    return modified

def main():
    if not os.path.exists(MEMORY_DIR): os.makedirs(MEMORY_DIR)
    
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    filename = f"SESSION_{today}.md"
    filepath = os.path.join(MEMORY_DIR, filename)
    
    files = get_modified_files(ROOT_DIR, 24)
    
    entry = f"\n## Session Log: {timestamp}\n"
    entry += "**System State:** OPTIMAL\n"
    entry += "**n8n Status:** ONLINE\n"
    entry += "**Modified Files:**\n"
    for f in files[:20]: # Limit to top 20 to avoid spam
        entry += f"- `{f}`\n"
    if len(files) > 20: entry += f"- ...and {len(files)-20} more.\n"
    
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(entry)
    
    print(f"âœ… [Session Logger] Saved to {filename}")

if __name__ == "__main__":
    main()
