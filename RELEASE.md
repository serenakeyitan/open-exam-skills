# Release Process

Use this checklist to cut stable releases from `main`.

## v0.1.0 Checklist

1. Confirm `main` contains only stable skills.
2. Run the packaging script:
   ```bash
   ./scripts/package_release.sh v0.1.0
   ```
3. Create a GitHub Release tagged `v0.1.0`.
4. Upload all assets from `dist/v0.1.0/`:
   - `study-skills-suite-v0.1.0-all.zip`
   - One zip per stable skill (`mindmap.zip`, `flashcards.zip`, `quiz.zip`, `reports.zip`, `infographic.zip`, `data-table.zip`, `citation-check.zip`)
5. Add release notes that highlight the stable skills, install flow, and that experimental skills live in `dev`.

Only stable skills from `main` should ship in release assets.
