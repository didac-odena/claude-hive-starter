---
description: Guide for creating effective Claude custom commands. Use when the user wants to create a new command (or update an existing one) that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations. Triggered by prompts like "quiero crear una skill", "mejora esta skill", "diseña una skill nueva", or "crea un comando personalizado".
---

# Skill Creator

## About Claude Custom Commands

Custom commands live in `~/.claude/commands/<name>.md` (global) or `.claude/commands/<name>.md` (project-local).
They are invoked with `/name` in the Claude Code CLI.

Each command file is a Markdown file with optional YAML frontmatter:

```md
---
description: What this command does and when to use it (used for auto-triggering)
allowed-tools: Bash(git commit:*), Bash(npm run:*)   # optional — restrict tool access
---

# Command Name

Instructions for Claude...
```

You can inject live shell output at invocation time using `!` prefix:

```md
- Current branch: !`git branch --show-current`
- Project structure: !`find . -not -path "*/node_modules/*" | head -40`
```

## Core Principles

- **Be concise**: Only include context Claude doesn't already have. The description field is critical — it drives auto-triggering.
- **Description field**: Include what the command does AND when to use it (trigger phrases, user intents, example prompts). This is the primary triggering mechanism.
- **Body**: Loaded only after triggering. Focus on workflow steps, guardrails, and done criteria.
- **Guardrails**: Add explicit "do not" rules to prevent common failure modes.
- **Done criteria**: State clearly when the task is considered complete.

## Skill Creation Process

1. Understand the skill with concrete examples — what would a user say to trigger it?
2. Plan the workflow steps and any guardrails needed.
3. Write the `description` frontmatter (trigger-focused).
4. Write the body (workflow, steps, guardrails, response format).
5. Test it by invoking `/name` and checking behavior.
6. Iterate based on real usage.

## Command Naming

- Use lowercase letters, digits, and hyphens only (e.g., `fix-bug`, `design-review`).
- Prefer short, verb-led phrases that describe the action.
- The filename becomes the invocation name: `fix-bug.md` → `/fix-bug`.

## Response Format

When creating or updating a command:

1. Show the full content of the new/updated `.md` file.
2. State the invocation path (`~/.claude/commands/<name>.md` or `.claude/commands/<name>.md`).
3. Confirm the trigger phrases covered by the description.
