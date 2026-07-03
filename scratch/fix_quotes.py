import os
import re

directory = "."
for root, dirs, files in os.walk(directory):
    if ".git" in root or "venv" in root or "env" in root:
        continue
    for file in files:
        if file.endswith(".html"):
            filepath = os.path.join(root, file)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            new_content = content.replace(';""', ';"')
            new_content = new_content.replace(';">"', ';">')

            if new_content != content:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
