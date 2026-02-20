import os

target_path = "C:/Users/Media Server/Mr.Holmes/Core/Searcher_person.py"
clean_path = "C:/Users/Media Server/Mr.Holmes/Mr.Holmes/Core/Searcher_person.py"

with open(clean_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    stripped = line.lstrip()
    indent = line[:len(line) - len(stripped)]
    if "input(" in stripped:
        if "=" in stripped:
            parts = stripped.split("=")
            var_name = parts[0].strip()
            if "int(" in stripped:
                new_lines.append(indent + var_name + " = 0" + chr(10))
            else:
                new_lines.append(indent + var_name + " = 'n'" + chr(10))
        else:
            new_lines.append(indent + "pass # input removed" + chr(10))
    else:
        new_lines.append(line)

with open(target_path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("Mr. Holmes patched successfully (Chr10 Script).")
