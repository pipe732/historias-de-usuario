import os
import re

print('Start replacing simple styles')
# We will do simple regex replacements to move simple CSS properties into class strings.

files_changed = 0

for root, dirs, files in os.walk('.'):
    if '.git' in root or 'venv' in root or 'env' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            original = content
            
            # Simple manual replacements for very common ones:
            content = content.replace('style="text-align:center;"', 'class="text-center"')
            content = content.replace('style="text-align: center;"', 'class="text-center"')
            content = content.replace('style="display:none;"', 'class="d-none"')
            content = content.replace('style="display: none;"', 'class="d-none"')
            content = content.replace('style="display: flex; align-items: center;"', 'class="d-flex align-items-center"')
            content = content.replace('style="width:100%;"', 'class="w-100"')
            content = content.replace('style="width: 100%;"', 'class="w-100"')
            content = content.replace('style="margin:0;"', 'class="m-0"')
            
            if content != original:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                files_changed += 1
                print(f"Changed {filepath}")

print(f"Total files changed: {files_changed}")
