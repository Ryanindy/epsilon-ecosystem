import os

target_path = 'C:/Users/Media Server/Mr.Holmes/Core/Searcher_person.py'
clean_path = 'C:/Users/Media Server/Mr.Holmes/Mr.Holmes/Core/Searcher_person.py'

with open(clean_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Using block strings to avoid escaping issues
choice_input_1 = """choice = int(input(
            Font.Color.BLUE + "
[?]" + Font.Color.WHITE + Language.Translation.Translate_Language(filename, "Default", "choice", "None") + Font.Color.GREEN + "[#MR.HOLMES#]" + Font.Color.WHITE + "-->"))"""

recap_input = """Recaps = int(input(Font.Color.BLUE + "
[?]" + Font.Color.WHITE + Language.Translation.Translate_Language(
            filename, "Default", "Hypo", "None") + Font.Color.GREEN + "[#MR.HOLMES#]" + Font.Color.WHITE + "-->"))"""

choice_input_2 = """choice = int(input(
            Font.Color.BLUE + "
[?]" + Font.Color.WHITE + Language.Translation.Translate_Language(filename, "Default", "Dorks", "None") + Font.Color.GREEN + "[#MR.HOLMES#]" + Font.Color.WHITE + "-->"))"""

choice_input_3 = """choice = int(input(
            Font.Color.BLUE + "
[?]" + Font.Color.WHITE + Language.Translation.Translate_Language(filename, "Transfer", "Question", "None") + Font.Color.GREEN + "[#MR.HOLMES#]" + Font.Color.WHITE + "-->"))"""

inp_input = """inp = input(Language.Translation.Translate_Language(
            filename, "Default", "Continue", "None"))"""

to_replace = [
    (choice_input_1, 'choice = 0'),
    (recap_input, 'Recaps = 0'),
    (choice_input_2, 'choice = 0'),
    (choice_input_3, 'choice = 0'),
    (inp_input, 'inp = "n"')
]

for old, new in to_replace:
    # Normalize newlines for cross-platform matching if needed
    old_norm = old.replace('
', '
')
    content = content.replace(old_norm, new)

with open(target_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Mr. Holmes patched successfully (Block Surgical).")
