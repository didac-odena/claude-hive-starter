---
description: Install project conventions (React, Express, Vitest, CSS, Naming) into the current repo's CLAUDE.md so they load automatically for that project. Use when setting up a new project, when the user says "instala convenciones", "setup conventions", "conventions", or when starting work on a React/Express repo that doesn't have conventions yet.
---

# Install Conventions

## Workflow

1. Check if the project CLAUDE.md already contains the marker `<!-- conventions:react-express -->`.
   - If yes: tell the user conventions are already installed. Ask if they want to update (replace the block).
   - If no: proceed.

2. Detect project type by reading `package.json` (if it exists):
   - **React**: `react` in dependencies/devDependencies
   - **Express**: `express` in dependencies
   - **Vitest**: `vitest` in devDependencies
   - If no `package.json` found: ask the user what conventions they want (React, Express, both).

3. Read the template file: `~/.claude/templates/conventions-react-express.md`

4. Filter sections based on detected project type:
   - React detected: include Toolchain, Frontend Structure, Barrels, React Conventions, React Router v6, CSS, API Services, Naming
   - Express detected: include Node/Express REST API (all subsections)
   - Vitest detected: include Testing
   - Both: include all sections

5. Append the filtered conventions to the project's CLAUDE.md (create the file if it doesn't exist).

6. Also check if the project has an AGENTS.md (Codex). If it does, install the same conventions there too. If not, ask the user if they want one created.

7. Confirm to the user what was installed and where.

## Guardrails

- Never overwrite existing CLAUDE.md or AGENTS.md content — only append at the end.
- Always preserve the `<!-- conventions:react-express -->` marker so re-running is idempotent.
- If updating (marker already exists): replace only the block between the marker and the end of the conventions section.
- Do not modify the global `~/.claude/CLAUDE.md` or `~/.codex/AGENTS.md`.
