#!/usr/bin/env python3

from pathlib import Path
import re
import sys


MAX_DESCRIPTION_LENGTH = 140
REQUIRED_FIELDS = {"name", "description"}


def extract_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("Missing frontmatter header")

    try:
        end_index = lines.index("---", 1)
    except ValueError as exc:
        raise ValueError("Missing frontmatter footer") from exc

    frontmatter = {}
    for line in lines[1:end_index]:
        if not line.strip():
            continue
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.+)$", line)
        if not match:
            raise ValueError(f"Invalid frontmatter line: {line}")
        frontmatter[match.group(1)] = match.group(2).strip()
    return frontmatter


def validate_description(description: str) -> list[str]:
    issues = []
    if len(description) > MAX_DESCRIPTION_LENGTH:
        issues.append(
            f"Description too long ({len(description)} > {MAX_DESCRIPTION_LENGTH})"
        )
    lowered = description.lower()
    if "step" in lowered:
        issues.append("Description must be trigger-only (contains 'step')")
    if re.search(r"\d+\.", description):
        issues.append("Description must be trigger-only (contains numbered steps)")
    return issues


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    skills_dir = repo_root / "skills"
    meta_skill = skills_dir / "using-open-exam-skills" / "SKILL.md"

    errors = []
    if not meta_skill.exists():
        errors.append("Missing meta skill: skills/using-open-exam-skills/SKILL.md")

    for skill_md in skills_dir.rglob("SKILL.md"):
        try:
            frontmatter = extract_frontmatter(skill_md)
        except ValueError as exc:
            errors.append(f"{skill_md}: {exc}")
            continue

        missing = REQUIRED_FIELDS - frontmatter.keys()
        if missing:
            errors.append(f"{skill_md}: missing fields {sorted(missing)}")
            continue

        description = frontmatter.get("description", "")
        for issue in validate_description(description):
            errors.append(f"{skill_md}: {issue}")

    if errors:
        print("Skill frontmatter checks failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Skill frontmatter checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
