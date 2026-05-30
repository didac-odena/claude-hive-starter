---
description: List or install Claude custom commands from the official plugin marketplace or from a GitHub path. Use when the user asks what skills/commands are available to install, wants to install a command from the marketplace, or provides a GitHub repo/path with a command to copy. Triggered by prompts like "instala una skill", "qué skills hay disponibles", "instala skill desde repo", or "lista los comandos disponibles".
---

# Skill Installer

## About Claude Commands

Global commands live in `~/.claude/commands/`.
Project-local commands live in `.claude/commands/` at the repo root.

## Listing Available Commands

To list currently installed global commands:

```bash
ls ~/.claude/commands/
```

To list project-local commands (if in a repo):

```bash
ls .claude/commands/ 2>/dev/null || echo "No project-local commands"
```

The official Claude plugin marketplace is at: `~/.claude/plugins/marketplaces/claude-plugins-official/`

To list available official plugins and their commands:

```bash
ls ~/.claude/plugins/marketplaces/claude-plugins-official/plugins/
```

## Installing from the Marketplace

To install a command from an official plugin, copy its `.md` file to `~/.claude/commands/`:

```bash
cp ~/.claude/plugins/marketplaces/claude-plugins-official/plugins/<plugin-name>/commands/<command>.md ~/.claude/commands/
```

## Installing from a GitHub Repo

If the user provides a GitHub URL or repo path pointing to a command `.md` file, fetch it and save to `~/.claude/commands/`:

```bash
curl -L "<raw-github-url>" -o ~/.claude/commands/<name>.md
```

Or clone the repo and copy the relevant file manually.

## After Installing

New commands are available immediately — no restart required.
Verify with `/name` in the CLI or check the command list.

## Notes

- If a command already exists at the destination, ask the user before overwriting.
- Project-local commands (`.claude/commands/`) take precedence over global ones with the same name.
- The description field in the frontmatter controls when the command auto-triggers — review it after installing.
