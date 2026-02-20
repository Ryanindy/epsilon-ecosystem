import base64

code = """
import os
import re

target_path = "C:/Users/Media Server/Mr.Holmes/Core/Searcher_person.py"
clean_path = "C:/Users/Media Server/Mr.Holmes/Mr.Holmes/Core/Searcher_person.py"

if not os.path.exists(clean_path):
    print(f"Error: Clean path {clean_path} not found.")
    exit(1)

with open(clean_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace all int(input(...)) blocks with 0
content = re.sub(r"int\(input\(.*?\)\)", "0", content, flags=re.DOTALL)
# Replace all input(...) blocks with "n"
content = re.sub(r"input\(.*?\)", '"n"', content, flags=re.DOTALL)

with open(target_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Mr. Holmes patched successfully (Regex Final).")
"""

encoded = base64.b64encode(code.encode()).decode()
print(encoded)
