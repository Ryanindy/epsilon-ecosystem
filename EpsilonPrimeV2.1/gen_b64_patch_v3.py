import base64

code = r"""
import os

target_path = "C:/Users/Media Server/Mr.Holmes/Core/Searcher_person.py"
clean_path = "C:/Users/Media Server/Mr.Holmes/Mr.Holmes/Core/Searcher_person.py"

with open(clean_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "input(" in line:
        # Identify the variable being assigned
        if "=" in line:
            var_name = line.split("=")[0].strip()
            if "int(" in line:
                new_lines.append(f"{' ' * (len(line) - len(line.lstrip()))}{var_name} = 0
")
            else:
                new_lines.append(f"{' ' * (len(line) - len(line.lstrip()))}{var_name} = 'n'
")
        else:
            new_lines.append(f"{' ' * (len(line) - len(line.lstrip()))}pass # input removed
")
    else:
        new_lines.append(line)

with open(target_path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("Mr. Holmes patched successfully (Line-by-Line).")
"""

encoded = base64.b64encode(code.encode()).decode()
print(encoded)
