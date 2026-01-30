---
name: using-open-exam-skills
description: Route requests to the right Open Exam Skills before responding.
---

# Using Open Exam Skills

This is the meta skill that governs how to use the other skills in this bundle.

## Core Rule

If there is even a small chance a skill applies, invoke the skill before responding in your own words. Always check the skills first.

## Priority Order

1. **citation-check**: trust, claims, numbers, slide bullets, summaries with facts
2. **mindmap**: structure, outline, relationships, concept maps
3. **flashcards**: memorization, drilling, spaced repetition
4. **quiz**: testing, exam simulation, grading

## Orchestration Rules

- If the user asks for multiple outputs, orchestrate the skills in order.
- For factual or citation-heavy work, always run **citation-check** first.
- For study flow: **mindmap → flashcards → quiz**.
- For cramming: **flashcards → quiz**.

## Output Behavior

Always end outputs with a short “Next actions” menu that suggests the other skills:

Next actions: mindmap · flashcards · quiz · citation-check
