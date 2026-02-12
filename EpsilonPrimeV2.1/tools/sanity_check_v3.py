import os
import socket
import json

PROJECT_ROOT = os.getcwd()
SKILLS_DIR = os.path.join(PROJECT_ROOT, "skills")
MCP_DIR = os.path.join(PROJECT_ROOT, "mcp")

def check_path(path):
    exists = os.path.exists(path)
    return "OK" if exists else "MISSING"

def check_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return "LIVE" if s.connect_ex(('localhost', port)) == 0 else "DOWN"

print("--- EPSILON PRIME V3.0 DIAGNOSTIC ---")

print("\n[CORE PATHS]")
print(f"Hive Config:      {check_path('hive/hive_config.json')}")
print(f"Packages Dir:     {check_path('packages')}")
print(f"Soul File:        {check_path('.gemini/memory/SOUL.md')}")
print(f"Cognitive Log:    {check_path('.gemini/memory/COGNITIVE_LOG.md')}")

print("\n[TRINITY SKILLS]")
for trinity in ["EPSILON.md", "JACK.md", "PICKLE.md"]:
    p = os.path.join('skills/trinity', trinity)
    print(f"{trinity:<15} {check_path(p)}")

print("\n[SERVICES]")
print(f"API Bridge (5000): {check_port(5000)}")
print(f"n8n (5678):        {check_port(5678)}")
print(f"OpenClaw (18789):  {check_port(18789)}")

print("\n[MCP SERVERS]")
try:
    mcp_files = [f for f in os.listdir(MCP_DIR) if f.endswith(".py")]
    for mcp in mcp_files:
        p = os.path.join(MCP_DIR, mcp)
        print(f"{mcp:<25} {check_path(p)}")
except:
    print("MCP directory inaccessible.")

print("\n--- DIAGNOSTIC COMPLETE ---")
