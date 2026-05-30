---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git commit:*)
description: Prepare git commits with a canonical docs/DEVLOG.md entry and a concise Conventional Commit message based on pending code changes. Use when the user asks to "hacer commit", "preparar commit", "actualizar DEVLOG y commit", or similar requests to review current changes, summarize what was implemented, and stage/commit safely.
---

# Commit Devlog

## Overview

Use this command to convert pending git changes into:

1. A human-written `docs/DEVLOG.md` entry (canonical location)
2. A short Conventional Commit message (`feat: ...`, `fix: ...`, etc.)
3. A commit execution step — only after user confirmation

Summarize intent and behavior changes. Do not paste raw diffs into `docs/DEVLOG.md`.

## Workflow

### 1. Inspect Pending Changes

Run git inspection commands first:

- `git status --short`
- `git diff --name-only`
- `git diff --staged --name-only` (if needed)

Read the changed files that matter to understand what was implemented.

If there are unrelated changes, call them out and ask whether to include them before writing the log/commit.

### 2. Understand Before Writing

Write the `DEVLOG.md` entry from code understanding, not from raw patch text.

Focus on:

- User-visible behavior changes
- Bug fixes and root cause (if visible)
- Refactors that change structure/responsibilities
- Docs/config/test changes and why they matter

Avoid:

- Copy-pasting code blocks or diffs
- Vague summaries like "updated files"
- Guessing intent when the code is unclear (ask if needed)

### 3. Update Canonical `docs/DEVLOG.md`

Use `docs/DEVLOG.md` as the canonical file.

Location rules:

- If `docs/DEVLOG.md` exists, append there.
- If `DEVLOG.md` exists in the repo root and `docs/DEVLOG.md` does not exist, move it to `docs/DEVLOG.md` and preserve existing content.
- If neither exists, create `docs/` (if needed) and create `docs/DEVLOG.md`.
- `docs/DEVLOG.md` may be intentionally listed in `.gitignore` as a private local log. This is valid and should not block updating the file.

Append a new entry (do not overwrite previous entries) using this format:

```md
## YYYY-MM-DD

- `type: short commit-style summary`
- Clear bullet explaining what changed in behavior/implementation
- Clear bullet explaining secondary changes (tests/docs/config) if relevant
```

Rules:

- `type` should usually be one of: `feat`, `fix`, `refactor`, `docs`, `chore`, `test`
- First bullet is the "reference line" (very short, commit-style)
- Following bullets explain the work in plain language
- Keep entries concise and useful for future review

If multiple independent changes are pending, either write one grouped entry with a broad summary, or ask the user whether to split into multiple commits (preferred when changes are unrelated).

### 4. Propose Commit Message

Create a single commit message matching the main change:

- `feat: ...` for new functionality
- `fix: ...` for bug fixes
- `refactor: ...` for internal restructuring
- `docs: ...` for documentation-only changes
- `chore: ...` for maintenance/config/tooling
- `test: ...` for tests

Guidelines:

- One line only unless the user asks for a longer message
- Lowercase type
- Short, specific summary
- Prefer behavior/result wording over file names

### 5. Stage and Commit — Only With Confirmation

Default behavior:

- Prepare `docs/DEVLOG.md`
- Propose commit message
- If `docs/DEVLOG.md` is ignored, do not include it in the commit by default
- **Ask for confirmation before running `git add` / `git commit`**

If the user explicitly asks to execute the commit, proceed and report:

- What was staged
- The final commit message
- Whether the commit succeeded

If `docs/DEVLOG.md` is ignored and the user still wants it in the commit, use `git add -f docs/DEVLOG.md` explicitly and mention it is being force-added despite `.gitignore`.

## Practical Heuristics

- If `docs/DEVLOG.md` is the only changed file after your update, re-check whether there were unstaged/staged code changes before assuming the task is complete.
- Distinguish "private DEVLOG update" from "commit contents": updating `docs/DEVLOG.md` is part of the workflow even when it remains uncommitted.
- Prefer one coherent commit over a mixed commit, but do not split automatically unless the user asks.
- If the repo already uses a different commit convention, follow the repo convention and keep the `DEVLOG.md` reference line aligned with it.
