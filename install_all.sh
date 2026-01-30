#!/bin/bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STABLE_SKILLS=(
  "mindmap"
  "flashcards"
  "quiz"
  "reports"
  "citation-check"
)

install_requirements() {
  local skill_dir="$1"

  if [ ! -f "$skill_dir/requirements.txt" ]; then
    echo "   No requirements.txt found."
    return 0
  fi

  if python3 -m pip install -q --disable-pip-version-check -r "$skill_dir/requirements.txt" 2>&1 | grep -q "externally-managed-environment"; then
    echo "   Using --break-system-packages flag..."
    python3 -m pip install -q --disable-pip-version-check --break-system-packages -r "$skill_dir/requirements.txt" 2>&1 | grep -v "already satisfied" || true
  else
    python3 -m pip install -q --disable-pip-version-check -r "$skill_dir/requirements.txt" 2>&1 | grep -v "already satisfied" || true
  fi
}

echo "🚀 Installing stable Open Exam Skills..."

for skill in "${STABLE_SKILLS[@]}"; do
  skill_dir="$ROOT_DIR/$skill"

  if [ ! -d "$skill_dir" ]; then
    echo "⚠️  Skipping missing skill: $skill"
    continue
  fi

  echo "\n➡️  Installing $skill..."

  if [ -x "$skill_dir/scripts/install.sh" ]; then
    bash "$skill_dir/scripts/install.sh"
  else
    install_requirements "$skill_dir"

    if [ ! -f "$skill_dir/.env" ] && [ -f "$skill_dir/.env.example" ]; then
      cp "$skill_dir/.env.example" "$skill_dir/.env"
      echo "⚠️  Please configure your API keys in $skill/.env"
    fi
  fi
done

echo "\n✅ All stable skills installed successfully!"
