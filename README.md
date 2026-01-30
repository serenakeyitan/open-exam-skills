# Ultimate Open-Source AI Exam Prep Toolkit (SKILLs)

A high-quality collection of study skills built for high school and college students, teachers, and TAs.  
Interactive mind maps, flashcards and quizzes, citation checking, and complete study workflows.  
Not just tools, but a smart study companion that learns with you.

You can upload these skills and run them directly inside Claude and GPT, or run them in Kael by simply saying things like “create a mind map for me” or “quiz me on this topic”.

This lets you turn notes into practice questions, concept cards, and even mock exams, all in one conversation.

### [Kael.im](https://kael.im) has these skills built in for free. Just say “create a mind map”, “quiz me”, “make flashcards”, or “citation check this”.

## Demos
### flashcards skill

https://github.com/user-attachments/assets/b87cd587-74a8-4ce9-ae88-63a80e75124b

### quiz skill

https://github.com/user-attachments/assets/bf684b7f-d0fa-4ffc-b16e-b58ea4da01ac

### mindmap skill

https://github.com/user-attachments/assets/690ec675-ee48-4392-a958-f83b9c26e3e5

### citation check skill

https://github.com/user-attachments/assets/f6c92bfa-91a6-440d-8205-d84074de7dbd


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

Workflow packs are included under `skills/packs/`.

## Skills Table

| Name | What it does | Best for | Output type |
| --- | --- | --- | --- |
| Mind Map | Turns notes into interactive concept maps | Student | HTML, PNG, Mermaid |
| Flashcards | Builds fast recall cards from study material | Student | HTML, CSV |
| Quiz | Generates practice quizzes with explanations | Student | HTML |
| Citation Check | Blocks uncited or inconsistent claims | Both | Markdown report |

The umbrella zip also includes the meta skill `using-open-exam-skills` plus workflow packs under `skills/packs/`.

## Installation

### Install One Umbrella Skill (Recommended)

1. Download the umbrella bundle `open-exam-skills-all.zip` from GitHub Releases.
2. If you prefer a direct repo download, grab it from `dist/open-exam-skills-all.zip`.
3. Upload the zip into Claude or GPT (Settings → Skills → Add).
4. Use the meta skill `using-open-exam-skills` or invoke any sub-skill by name.

### Install Individual Skills (Advanced)

1. Download `mindmap.zip`, `flashcards.zip`, `quiz.zip`, or `citation-check.zip` from Releases.
2. Upload the zip into Claude or GPT (Settings → Skills → Add).
3. Use the skill name directly.

### Advanced: Git Clone + Local Install

```bash
git clone https://github.com/serenakeyitan/open-exam-skills.git
cd open-exam-skills
./install_all.sh
```

`install_all.sh` installs only the stable skills listed below.

## Environment Variables

Stable skills require no API keys. Experimental audio/video skills on `dev` use `ELEVENLABS_API_KEY`.

## Supported Skills vs Experimental

**Stable (main)**
- `skills/using-open-exam-skills`
- `skills/mindmap`
- `skills/flashcards`
- `skills/quiz`
- `skills/citation-check`
- `skills/packs/student-exam-prep`
- `skills/packs/trust-track`

**Experimental (dev branch)**
- `audio-overview`
- `video-overview`
- `infographic`
- `data-table`

Experimental skills are intentionally separated and are not included in installs or release bundles.

## Safety & Quality

Stable skills are designed for real classrooms: deterministic where possible, documented, and safe to run with student material. Citation-check enforces “no citation, no output” for any research-facing workflow.

## Releases

Each GitHub Release ships:

- `open-exam-skills-all.zip` umbrella bundle
- `open-exam-skills-v<version>-all.zip` versioned release bundle
- Individual zips per stable skill

Only stable skills from `main` are included.

## Contributing

See `CONTRIBUTING.md` for how to add a new skill, the folder structure, and the quality bar for stable releases.

## License

MIT License. See `LICENSE`.
