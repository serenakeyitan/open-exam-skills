# Ultimate Open-Source AI Exam Prep Toolkit (SKILLs)

A high-quality collection of study skills built for high school and college students, teachers, and TAs.  
Interactive mind maps, flashcards and quizzes, citation checking, and complete study workflows.  
Not just tools, but a smart study companion that learns with you.

You can upload these skills and run them directly inside Claude and GPT, or run them in Kael by simply saying things like “create a mind map for me” or “quiz me on this topic”.

This lets you turn notes into practice questions, concept cards, and even mock exams, all in one conversation.

## Who This Is For

- Students preparing for exams (high school & college)
- Teachers and TAs creating quizzes, practice exams, and study materials

## Study Workflow Packs (Angle D)

**Student Exam Prep Pack**
- Notes → mind map → flashcards → quiz → weak-area review

**Practice Exam Pack (Students + TAs)**
- Source material → practice questions → interactive quiz → explanations

**Trust Track (Citation Check)**
- Any report, notes, or slides → citation-check
- No citation, no output

## Skills Table

| Name | What it does | Best for | Output type |
| --- | --- | --- | --- |
| Mind Map | Turns notes into interactive concept maps | Student | HTML, PNG, Mermaid |
| Flashcards | Builds fast recall cards from study material | Student | HTML, CSV |
| Quiz | Generates practice quizzes with explanations | Student | HTML |
| Reports | Produces structured study reports and briefs | TA | Markdown, PDF, DOCX |
| Infographic | Summarizes key data into visuals | TA | PNG, SVG |
| Data Table | Extracts structured tables from sources | TA | CSV, JSON, XLSX |
| Citation Check | Blocks uncited or inconsistent claims | Both | Markdown report |

## Installation

### Beginner: Download a Release Zip

1. Download the latest release bundle (`study-skills-suite-<version>-all.zip`) or an individual skill zip.
2. Upload the zip into Claude or GPT (Settings → Skills → Add).
3. Invoke the skill by name (for example, “mindmap”, “flashcards”, “quiz”, “citation-check”).

### Advanced: Git Clone + Local Install

```bash
git clone https://github.com/serenakeyitan/study-skills-suite.git
cd study-skills-suite
./install_all.sh
```

`install_all.sh` installs only the stable skills listed below.

## Environment Variables

Each skill reads environment variables from its own `.env` file (created from `.env.example` when available).

| Variable | Used by | Notes |
| --- | --- | --- |
| `GEMINI_API_KEY` | reports, infographic, data-table | Required for AI generation |
| `ANTHROPIC_API_KEY` | reports, data-table | Optional fallback |
| `ELEVENLABS_API_KEY` | audio-overview, video-overview | Experimental only (dev branch) |

Skills that are pure front-end converters (mindmap, flashcards, quiz) and citation-check require no API keys.

## Supported Skills vs Experimental

**Stable (main)**
- `mindmap`
- `flashcards`
- `quiz`
- `reports`
- `infographic`
- `data-table`
- `citation-check`

**Experimental (dev branch)**
- `audio-overview`
- `video-overview`

Experimental skills are intentionally separated and are not included in installs or release bundles.

## Safety & Quality

Stable skills are designed for real classrooms: deterministic where possible, documented, and safe to run with student material. Citation-check enforces “no citation, no output” for any research-facing workflow.

## Releases

Each GitHub Release ships:

- One “all skills” zip bundle
- Individual zips per stable skill

Only stable skills from `main` are included.

## Contributing

See `CONTRIBUTING.md` for how to add a new skill, the folder structure, and the quality bar for stable releases.

## License

MIT License. See `LICENSE`.
