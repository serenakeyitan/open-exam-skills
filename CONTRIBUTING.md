# Contributing

Thanks for helping improve Open Exam Skills. This repo is the stable, student-facing baseline for the Kael skill marketplace.

## Adding a New Skill

1. Create a top-level folder named after the skill (kebab-case).
2. Include the standard files:
   - `SKILL.md` (required user-facing instructions)
   - `skill.yaml` (skill metadata)
   - `requirements.txt` (even if minimal)
   - `scripts/install.sh` (auto-install script)
   - `.env.example` when API keys are required
3. Keep each skill fully isolated (no shared imports across skills).
4. Update these repo files:
   - `README.md` (skills table + stable/experimental lists)
   - `install_all.sh` (stable installs only)
   - `scripts/package_release.sh` (release bundling)

## Folder Structure

```
open-exam-skills/
├── skill-name/
│   ├── SKILL.md
│   ├── skill.yaml
│   ├── requirements.txt
│   ├── main.py (if applicable)
│   ├── scripts/install.sh
│   └── .env.example (if needed)
```

## Quality Bar

- **Installable:** `scripts/install.sh` runs without manual steps beyond API keys.
- **Deterministic where possible:** avoid randomness unless explicitly required.
- **Documented:** clear instructions in `SKILL.md` and minimal usage examples.
- **Safe for real users:** defaults should avoid data loss, hallucinated citations, or ambiguous outputs.

## Stable vs Experimental

- Stable skills live on `main` and ship in releases.
- Experimental skills live on the `dev` branch and are not packaged.

If you are adding experimental work, open a PR to `dev` and keep it out of release scripts.
