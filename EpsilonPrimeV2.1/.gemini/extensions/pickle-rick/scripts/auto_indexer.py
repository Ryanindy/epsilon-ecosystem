import os
import time
import json
import glob
import sys

# CONFIG (Resolved relative to script location)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
EXT_DIR = os.path.dirname(SCRIPT_DIR)
PROJECT_ROOT = os.path.dirname(os.path.dirname(EXT_DIR))

SKILL_DIRS = [
    os.path.join(PROJECT_ROOT, "skills"),
    os.path.join(EXT_DIR, "skills")
]
ROUTER_FILE = os.path.join(PROJECT_ROOT, "skills", "10_SKILL_ROUTER.md")
STATE_FILE = os.path.join(SCRIPT_DIR, ".indexer_state")

def get_skills():
    skills = []
    for d in SKILL_DIRS:
        if not os.path.exists(d): continue
        # Find .skill.md and SKILL.md
        files = glob.glob(os.path.join(d, "**", "*.md"), recursive=True)
        for f in files:
            name = os.path.basename(f)
            # Filter for skill files
            if "skill" in name.lower() or "SKILL" in name:
                category = "GENERAL"
                if "pickle" in f.lower(): category = "ENGINEERING (Pickle)"
                elif "epsilon" in f.lower() or "governance" in f.lower(): category = "GOVERNANCE"
                elif "strateg" in f.lower(): category = "STRATEGY"
                elif "manag" in f.lower() or "arch" in f.lower(): category = "EXECUTION"
                elif "rag" in f.lower() or "know" in f.lower(): category = "KNOWLEDGE"
                
                skills.append({"name": name, "path": f, "category": category})
    return skills

def generate_router(skills):
    content = "# SKILL ROUTER (AUTO-GENERATED)\n**Last Updated:** " + time.ctime() + "\n\n"
    
    cats = {}
    for s in skills:
        c = s["category"]
        if c not in cats: cats[c] = []
        cats[c].append(s)
        
    for c, items in cats.items():
        content += f"## {c}\n"
        for i in items:
            clean_name = i["name"].replace(".skill.md", "").replace("SKILL.md", "").replace(".md", "")
            # If path is nested (Pickle), use directory name
            if "SKILL.md" in i["name"]:
                clean_name = os.path.basename(os.path.dirname(i["path"]))
            content += f"* **{clean_name}** -> `{i['path']}`\n"
        content += "\n"
        
    # Ensure skills dir exists
    os.makedirs(os.path.dirname(ROUTER_FILE), exist_ok=True)
    with open(ROUTER_FILE, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    try:
        # Check mtimes
        latest_mtime = 0
        for d in SKILL_DIRS:
            if not os.path.exists(d): continue
            for root, _, files in os.walk(d):
                for f in files:
                    if f.endswith(".md"):
                        m = os.path.getmtime(os.path.join(root, f))
                        if m > latest_mtime: latest_mtime = m
        
        # Check last run
        last_run = 0
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, "r") as f:
                last_run = float(f.read().strip())
                
        if latest_mtime > last_run:
            # Print to stderr for visibility
            print(f"[*] [Pickle Sentinel] Re-indexing skills...", file=sys.stderr)
            skills = get_skills()
            generate_router(skills)
            with open(STATE_FILE, "w") as f:
                f.write(str(time.time()))
    except Exception as e:
        print(f"[!] [Pickle Sentinel] Indexing Error: {e}", file=sys.stderr)
    
    # Always output allow decision for CLI hook protocol
    print('{"decision": "allow"}')

if __name__ == "__main__":
    main()
