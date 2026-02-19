import os

target_path = 'C:/Users/Media Server/Mr.Holmes/Core/Searcher_person.py'
clean_path = 'C:/Users/Media Server/Mr.Holmes/Mr.Holmes/Core/Searcher_person.py'

with open(clean_path, 'r', encoding='utf-8') as f:
    content = f.read()

# More surgical replacement
to_replace = [
    ('choice = int(input(
            Font.Color.BLUE + "
[?]" + Font.Color.WHITE + Language.Translation.Translate_Language(filename, "Default", "choice", "None") + Font.Color.GREEN + "[#MR.HOLMES#]" + Font.Color.WHITE + "-->"))', 'choice = 0'),
    ('Recaps = int(input(Font.Color.BLUE + "
[?]" + Font.Color.WHITE + Language.Translation.Translate_Language(
            filename, "Default", "Hypo", "None") + Font.Color.GREEN + "[#MR.HOLMES#]" + Font.Color.WHITE + "-->"))', 'Recaps = 0'),
    ('choice = int(input(
            Font.Color.BLUE + "
[?]" + Font.Color.WHITE + Language.Translation.Translate_Language(filename, "Default", "Dorks", "None") + Font.Color.GREEN + "[#MR.HOLMES#]" + Font.Color.WHITE + "-->"))', 'choice = 0'),
    ('choice = int(input(
            Font.Color.BLUE + "
[?]" + Font.Color.WHITE + Language.Translation.Translate_Language(filename, "Transfer", "Question", "None") + Font.Color.GREEN + "[#MR.HOLMES#]" + Font.Color.WHITE + "-->"))', 'choice = 0'),
    ('inp = input(Language.Translation.Translate_Language(
            filename, "Default", "Continue", "None"))', 'inp = "n"')
]

for old, new in to_replace:
    content = content.replace(old, new)

with open(target_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Mr. Holmes patched successfully (Surgical).")
