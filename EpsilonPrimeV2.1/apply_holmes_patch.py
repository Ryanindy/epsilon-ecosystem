import os

target_path = 'C:/Users/Media Server/Mr.Holmes/Core/Searcher_person.py'
patch_path = 'Searcher_person_patch.py.part'

with open(target_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

with open(patch_path, 'r', encoding='utf-8') as f:
    patch = f.read()

# Find the start and end of the Search method
start_line = -1
end_line = -1

for i, line in enumerate(lines):
    if 'def Search(username, Mode):' in line:
        start_line = i
        break

if start_line != -1:
    # Find the next method or end of class
    # The Search method ends before 'if __name__ == "__main__":' in the original file (Wait, no, it's inside a class)
    # The next method is not there, so it goes until the end of the class.
    # Actually, in this file, Search is the last method in class 'info'.
    # So it ends when indentation changes or file ends.
    # Let's just look for the next '@staticmethod' or end of file.
    for i in range(start_line + 1, len(lines)):
        if '@staticmethod' in lines[i] or i == len(lines) - 1:
            end_line = i
            break

if start_line != -1 and end_line != -1:
    new_lines = lines[:start_line-1] + [patch] + lines[end_line:]
    with open('Searcher_person_new.py', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("Patch applied to local file.")
else:
    print(f"Could not find Search method. start: {start_line}, end: {end_line}")
