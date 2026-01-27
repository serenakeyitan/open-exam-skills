#!/usr/bin/env python3
"""Fix all skills to make --input optional in test mode"""

import re
import os

skills = ['mindmap', 'reports', 'flashcards', 'quiz', 'infographic', 'data-table']

for skill in skills:
    main_file = f"{skill}/main.py"
    if not os.path.exists(main_file):
        continue

    with open(main_file, 'r') as f:
        content = f.read()

    # Fix: Remove required=True from --input argument
    content = re.sub(
        r'parser\.add_argument\("--input", "-i", required=True,',
        'parser.add_argument("--input", "-i",',
        content
    )

    #Fix: Add validation in else block if not present properly
    # Find the main() function and look for the pattern:
    # else:
    #     with open(args.input)...
    # and add validation before it

    pattern = r'(    else:\s+)\n(\s+with open\(args\.input\))'
    replacement = r'\1\n        if not args.input:\n            parser.error("--input is required when not in test mode")\n\2'
    content = re.sub(pattern, replacement, content)

    # Write back
    with open(main_file, 'w') as f:
        f.write(content)

    print(f"Fixed {skill}/main.py")

print("Done!")
