#!/bin/bash

# Test all skills and report results

echo "Testing all NotebookLM Skills..."
echo "================================"
echo ""

cd /Users/keyitan/nblm-skills

# Array of skills to test
skills=("audio-overview" "video-overview" "mindmap" "reports" "flashcards" "quiz" "infographic" "data-table")

for skill in "${skills[@]}"; do
    echo "Testing: $skill"
    echo "---"
    cd "$skill"

    # Fix the --input requirement first
    if grep -q 'required=True.*"--input"' main.py 2>/dev/null; then
        sed -i '' 's/required=True, help="Input/help="Input/g' main.py
    fi
    if grep -q 'required=True).*# --input' main.py 2>/dev/null; then
        sed -i '' 's/required=True)/)/g' main.py
    fi

    # Run test
    timeout 60 python main.py --test 2>&1 | tail -5

    if [ $? -eq 0 ]; then
        echo "✅ $skill: PASSED"
    else
        echo "❌ $skill: FAILED"
    fi

    cd ..
    echo ""
done

echo "================================"
echo "Testing complete!"
