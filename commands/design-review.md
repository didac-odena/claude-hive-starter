---
description: Review software architecture and code structure to propose incremental design improvements in responsibilities, coupling, module boundaries, folder organization, and data flow. Use when the user asks to review architecture or structure, check whether responsibilities are correct, improve maintainability, or plan a structural refactor, including prompts like "revisa la arquitectura", "revisa la estructura", or "revisa que las responsabilidades sean correctas". Prefer this over perf-check or security-scan when the main goal is code organization and design quality rather than speed or vulnerabilities.
---

# Design Review

## Overview

Review code structure and architecture with a maintainability-first mindset.
Propose incremental improvements that fit the repository conventions instead of suggesting large rewrites by default.

## Workflow

1. Define the review scope and goal.
2. Read local conventions and architecture constraints first.
3. Map the current structure and responsibilities.
4. Identify design issues and classify their impact.
5. Propose incremental improvements with tradeoffs.
6. Suggest an implementation order.
7. Report findings with file references and rationale.

## Step Details

### 1. Define Scope

- Identify whether the review targets a module, feature, page, service, API layer, or whole repo.
- Identify the user's goal: maintainability, readability, ownership boundaries, scaling, onboarding, or refactor planning.
- Avoid expanding scope unless needed to explain a dependency problem.

### 2. Read Conventions First

- Read local `CLAUDE.md`, `AGENTS.md`, and relevant project docs before proposing structural changes.
- Treat repo conventions as constraints, not suggestions.
- If a convention conflicts with current code, call it out explicitly instead of silently applying your own preference.

### 3. Map Current Design

- Identify main modules and their responsibilities.
- Trace key flows (for example: UI -> hook/service -> state -> UI, or route -> controller -> service -> model).
- Note coupling points, shared utilities, and cross-layer dependencies.
- Note repeated patterns that could justify a reusable abstraction.

### 4. Identify Issues

Prioritize issues like:

- Mixed responsibilities in one file or module
- Tight coupling across layers or features
- Leaky abstractions (UI code in services, HTTP concerns in domain logic, etc.)
- Folder/module organization that hides intent
- Repetition that should be extracted
- Over-abstraction or unnecessary indirection
- Inconsistent naming that hurts navigation

Separate:

- Confirmed issues (visible in code)
- Risks/assumptions (need broader context or runtime behavior)

### 5. Propose Improvements

- Prefer small, staged refactors over broad rewrites.
- Explain why each change improves clarity, maintainability, or correctness.
- Keep proposals aligned with the repo's conventions and the user's experience level.
- Give concrete examples (move file, rename module, extract component/service, collapse unnecessary layer).

### 6. Sequence the Work

- Start with low-risk structural wins.
- Isolate risky refactors behind tests or verification steps.
- Call out what can be done now vs later.

## Guardrails

- Do not propose a rewrite when incremental changes solve the main issues.
- Do not ignore local conventions in `CLAUDE.md` / `AGENTS.md`.
- Do not mix performance/security audits into the review unless explicitly requested.
- Do not present personal style preferences as architectural problems.
- Do not recommend abstractions without repeated evidence in the codebase.

## Done Criteria

Consider the task done only when all applicable items are true:

- Scope and assumptions are explicit.
- Local conventions were reviewed and referenced when relevant.
- Findings are prioritized by impact and maintainability risk.
- Recommendations are concrete, incremental, and actionable.
- Tradeoffs and risks are explained.
- File references are included for key findings.

## Response Format

Return a concise report with these sections:

- Scope and conventions considered
- Prioritized findings
- Recommended structural changes
- Suggested implementation order
- Risks / open questions
