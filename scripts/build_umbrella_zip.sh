#!/bin/bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST_DIR="$ROOT_DIR/dist"
OUTPUT_ZIP="$DIST_DIR/open-exam-skills-all.zip"

EXCLUDES=(
  "**/__pycache__/*"
  "**/*.pyc"
  "**/.env"
  "**/.env.*"
  "**/.DS_Store"
  "**/*.zip"
)

mkdir -p "$DIST_DIR"

echo "📦 Building umbrella zip at $OUTPUT_ZIP"
zip -r "$OUTPUT_ZIP" "skills" -x "${EXCLUDES[@]}"
echo "✅ Umbrella zip ready: $OUTPUT_ZIP"
