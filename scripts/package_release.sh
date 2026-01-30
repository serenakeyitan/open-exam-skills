#!/bin/bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VERSION="${1:-v0.1.0}"
DIST_DIR="$ROOT_DIR/dist/$VERSION"
REPO_NAME="open-exam-skills"
SKILLS_DIR="$ROOT_DIR/skills"

STABLE_SKILLS=(
  "mindmap"
  "flashcards"
  "quiz"
  "citation-check"
)

EXCLUDES=(
  "**/__pycache__/*"
  "**/*.pyc"
  "**/.env"
  "**/.env.*"
  "**/.DS_Store"
  "**/*.zip"
)

mkdir -p "$DIST_DIR"

echo "📦 Packaging release assets into $DIST_DIR"

for skill in "${STABLE_SKILLS[@]}"; do
  (cd "$SKILLS_DIR" && zip -r "$DIST_DIR/${skill}.zip" "$skill" -x "${EXCLUDES[@]}")
done

zip -r "$DIST_DIR/${REPO_NAME}-${VERSION}-all.zip" \
  "skills" \
  -x "${EXCLUDES[@]}"

echo "✅ Release assets ready in $DIST_DIR"
