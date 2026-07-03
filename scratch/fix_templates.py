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

            # Use raw strings with double quotes to safely represent single quotes
            pattern = r"(==|in)\s+extracted-style-\d+\"([^']*)'"
            replacement = r"\1 '\2'"
            new_content = re.sub(pattern, replacement, content)

            if new_content != content:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                count += 1
                print(f"Fixed {filepath}")

print(f"Total files fixed: {count}")
