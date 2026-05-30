---
description: Set up token-efficient Claude Code configuration for the current repo. Creates .claudeignore, path-scoped rules, and checks global settings. Use when starting a new project, when the user says "optimiza repo", "setup repo", "configura este repo para Claude", "economiza tokens", or after cloning a repo for the first time.
---

# Optimize Repo for Token Efficiency

## Overview

This skill configures the current repo for minimal token consumption without losing effectiveness. It creates project-level files and checks global settings.

## Workflow

### 1. Detect Project Type

Inspect the repo root to classify the project:

- **Python**: `requirements.txt`, `pyproject.toml`, `setup.py`, or `*.py` in root/src
- **Node/React**: `package.json` with `react` in deps
- **Node/Express**: `package.json` with `express` in deps
- **Generic**: none of the above

Also detect:
- Heavy data directories: `data/`, `datasets/`, `logs/`, `output/`, `reports/`
- Virtual environments: `.venv/`, `venv/`, `node_modules/`
- Build artifacts: `dist/`, `build/`, `__pycache__/`

### 2. Create `.claudeignore`

If `.claudeignore` does not exist, create it with:

**Always include:**
```
.git/
*.log
```

**Python projects — add:**
```
.venv/
venv/
__pycache__/
*.pyc
.pytest_cache/
.mypy_cache/
```

**Node projects — add:**
```
node_modules/
dist/
build/
coverage/
```

**If heavy data dirs detected — add each one:**
```
data/ohlc/
data/derived/
reports/
*.csv
*.jsonl
```

Ask the user before adding data directories — they may want some accessible.

### 3. Create Path-Scoped Rules

Scan the project structure and create `.claude/rules/` files for major modules.

For each significant directory (3+ Python/JS files), create a rule file with:
- `globs:` frontmatter matching `<dir>/**/*.py` or `<dir>/**/*.{js,jsx,ts,tsx}`
- 3-5 bullet points about that module's conventions, extracted from:
  - Existing CLAUDE.md or AGENTS.md in the repo
  - README files in that directory
  - Obvious patterns from file names and imports

Only create rules for directories where specific context would be useful. Do NOT create rules for generic utility folders.

### 4. Check Global Settings

Read `~/.claude/settings.json` and verify these are set:

| Key | Expected | What it does |
|---|---|---|
| `env.CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` | `"70"` | Compact earlier to keep context clean |
| `env.CLAUDE_CODE_SUBAGENT_MODEL` | `"haiku"` | Cheaper subagents for research tasks |
| `statusLine` | configured | Monitor context % and cost in real time |

If any are missing, inform the user and offer to add them. Do NOT modify global settings without confirmation.

### 5. Check Conventions

If the project has `package.json` with React or Express, remind the user to run `/conventions` to install the full conventions set.

### 6. Report

Print a summary:
- Files created (with paths)
- Global settings status (OK / missing)
- Estimated overhead reduction (qualitative: "heavy data dirs excluded", "N path-scoped rules created")
- Any manual steps needed

## Guardrails

- Never delete or overwrite existing files — only create new ones or append.
- Always ask before adding data directories to `.claudeignore` — the user may need them accessible.
- Do not modify global `~/.claude/settings.json` without explicit user confirmation.
- Do not create rules for directories with fewer than 3 source files.
- Keep each rule file under 10 lines — concise context only.
