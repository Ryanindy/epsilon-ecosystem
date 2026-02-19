import os

target_path = 'C:/Users/Media Server/Mr.Holmes/Core/Searcher_person.py'
clean_path = 'C:/Users/Media Server/Mr.Holmes/Mr.Holmes/Core/Searcher_person.py'

# Restore clean
with open(clean_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Patches
# Replace input calls with hardcoded 0 (No)
# choice = int(input(...)) -> choice = 0
# Recaps = int(input(...)) -> Recaps = 0
# inp = input(...) -> inp = "n"

import re

# Patch 'choice = int(input(...))'
content = re.sub(r'choice = int\(input\(.*?\)\)', 'choice = 0', content, flags=re.DOTALL)

# Patch 'Recaps = int(input(...))'
content = re.sub(r'Recaps = int\(input\(.*?\)\)', 'Recaps = 0', content, flags=re.DOTALL)

# Patch 'inp = input(...)'
content = re.sub(r'inp = input\(.*?\)', 'inp = "n"', content, flags=re.DOTALL)

# Write back
with open(target_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Mr. Holmes patched successfully.")
