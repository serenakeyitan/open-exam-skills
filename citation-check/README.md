# Citation Check v2

> No citation → no output.

Citation Check is a small, opinionated module for **detecting and blocking hallucinated or missing citations** in LLM outputs.

Built for research, slides, and agent pipelines where correctness matters.

Part of the Study Skills Suite release collection.

---
## Demo - Identified Issues

### TRY [Kael.im](https://kael.im/home)(NotebookLM slides alternative) and register at this link for 100 pages free daily quota (nbp)!
https://github.com/user-attachments/assets/99d427cf-992f-455c-897b-a8f8a132271c


<img width="1219" height="713" alt="Screenshot 2026-01-25 at 13 56 07" src="https://github.com/user-attachments/assets/660592cd-ca53-46ae-8064-28fad9e90b44" />

## How to Use
1. Download `citation-check.zip` from this suite's Releases
2. Upload it to Claude or GPT (Settings → Skills → Add)
3. Use it by telling your assistant: "run citation check" or "verify citations"
4. In Kael, simply say: "citation check this report"

**Note:** Always download from Releases so the folder name stays clean.

**API Keys:** None required for this skill.
## What it does

- ✅ Checks that every factual claim has a citation  
- ✅ Verifies that cited sources actually exist  
- ✅ Validates claim–citation consistency (exact numbers, not rounded)
- ✅ Supports vision: reads slides, PDFs, charts, tables
- ✅ Two modes: web search verification OR doc-only verification

If a check fails, the output should be blocked or regenerated.

---

## Why

Most tools add citations *after* generation.  
This enforces citations as a **generation constraint**.

If your agent can't cite a claim, it shouldn't make it.

---

## v2.0 — Consistency Update

Same input → Same output. Key changes:

| Feature                        | What it does                                                 |
| ------------------------------ | ------------------------------------------------------------ |
| **Two-Pass Architecture**      | Extract all claims first, then verify. No more inconsistent results. |
| **Claim Extraction Rules**     | Explicit taxonomy — statistics, comparatives, attributions, etc. |
| **Status Decision Tree**       | Deterministic classification: Verified → Numerical Error → Hallucination |
| **Academic Precision Mode**    | 96.555% ≠ 97%. Exact numbers only.                           |
| **Mandatory Search Templates** | Runs ALL query patterns, not ad-hoc searches                 |
| **Tie-Breaker Rules**          | No judgment calls on edge cases                              |

---

## Typical flow

```text
LLM output (slides / report / PDF)
↓
Pass 1: Extract all claims
↓
Pass 2: Verify each claim
↓
pass → ship
fail → regenerate / fix
```

---

## Two Modes

### Mode 1: Search Verification (default)

- Searches web for authoritative sources
- Validates citations actually exist
- Checks if cited sources say what's claimed

### Mode 2: Doc-Only Verification

- User provides source document(s)
- EVERYTHING must trace to those docs
- Flags any external knowledge as hallucination

Trigger doc-only mode with: *"only use this document"* / *"verify against the PDF only"*

---

## Status Classifications

| Status               | Meaning                                               |
| -------------------- | ----------------------------------------------------- |
| ✅ Verified           | Exact match with source                               |
| ⚠️ Numerical Error    | Values don't match (e.g., 97% vs 96.555%)             |
| ⚠️ Unverified         | No authoritative source found                         |
| ❌ Hallucination      | Contradicts source or fabricated                      |
| ❌ Misleading         | Cherry-picked or missing context                      |
| ❌ Citation Not Found | Referenced paper/report doesn't exist                 |
| ❌ Not in Source      | Claim can't be traced to provided doc (doc-only mode) |

---

## Installation

It's a Claude / ChatGPT skill. 

- **Claude:** [Agent Skills Documentation](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview)
- **ChatGPT:** [Codex Skills](https://developers.openai.com/codex/skills)

---

## License

MIT
