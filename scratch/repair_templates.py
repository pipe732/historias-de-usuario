import os
import re

directory = "."

count = 0
for root, dirs, files in os.walk(directory):
    if ".git" in root or "venv" in root or "env" in root:
        continue
    for file in files:
        if file.endswith(".html"):
            filepath = os.path.join(root, file)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            new_content = content
            
            # Fix 1: <spanAdministrador ... >
            new_content = re.sub(
                r'<(span|div)(Administrador|vencido|devuelto)\s+class="extracted-style-\d+"\'\s*%}[^>]+>',
                r'<\1 class="badge state-\2">',
                new_content
            )

            # Fix 2: class="... extracted-style-XXX"error' %}...;" role="alert">
            # This targets the alert in lista_usuarios and similar truncated Django template tags inside the class attribute.
            new_content = re.sub(
                r'class="([^"]*?extracted-style-\d+)"[a-zA-Z]+\'\s*%}.*?;"',
                r'class="\1"',
                new_content,
                flags=re.DOTALL
            )
            
            # If there are still hanging ' %}.*?"> (without the ;)
            new_content = re.sub(
                r'class="([^"]*?extracted-style-\d+)"[a-zA-Z]+\'\s*%}.*?">',
                r'class="\1">',
                new_content,
                flags=re.DOTALL
            )

            # Fix 3: class="text-center"padding:3rem 1rem;"> missing style="
            new_content = re.sub(
                r'class="([^"]+)"(padding:[^"]+";?)',
                r'class="\1" style="\2"',
                new_content
            )
            new_content = re.sub(
                r'class="([^"]+)"(display:[^"]+";?)',
                r'class="\1" style="\2"',
                new_content
            )

            if new_content != content:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                count += 1
                print(f"Fixed syntax errors in {filepath}")

print(f"Total files fixed: {count}")
