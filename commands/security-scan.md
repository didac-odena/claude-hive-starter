---
description: Perform a basic application security review focused on input validation, sanitization, authentication and authorization, token handling, secrets exposure, and error leakage. Use when the user asks to check whether a repo, API, or feature is secure, requests hardening or a security audit, or says "comprueba que esta API es segura", "comprueba que esta parte es segura", or "que no nos expongan cosas". Prefer this over design-review when the main goal is vulnerabilities and defensive checks.
---

# Security Scan

## Overview

Perform a practical, code-first security review and return a prioritized list of findings.
Separate confirmed issues from potential risks and explain evidence for each item.

## Workflow

1. Define the scope and stack (frontend, API, database, auth, third-party services).
2. Identify security-sensitive entry points and trust boundaries.
3. Review the required categories and collect evidence.
4. Classify findings by severity and confidence.
5. Suggest concrete fixes or mitigations.
6. Report prioritized findings with file references and residual risks.

## Review Categories

Review these categories at minimum:

- Input validation and schema enforcement
- Output encoding and sanitization (XSS and injection vectors)
- Authentication, authorization, and token/session handling
- Secrets management (hardcoded keys, logs, config exposure)
- Error handling and information leakage

## Review Method

### 1. Map Entry Points

- Inspect routes, controllers, request handlers, forms, and public endpoints.
- Inspect file upload paths, query builders, templating, and HTML rendering.
- Inspect auth middleware, session/token parsing, and permission checks.

### 2. Follow Untrusted Data

- Trace user-controlled input from entry point to storage, rendering, logging, and external calls.
- Check for validation, normalization, and escaping at the right layer.
- Check for unsafe sinks (raw HTML rendering, string-built queries, shell commands, eval-like behavior).

### 3. Check Secrets and Errors

- Search for secrets in code, config defaults, and example files.
- Check whether error responses expose stack traces, SQL details, or internal paths.
- Check logging for tokens, passwords, personal data, or raw request bodies.

## Severity and Confidence

Classify each item with:

- Severity: critical, high, medium, low
- Confidence: confirmed, likely, possible

State when a finding is a hypothesis that needs runtime validation.

## Guardrails

- Do not claim exploitable vulnerabilities without evidence.
- Do not flood the report with generic best practices unrelated to the code reviewed.
- Do not mix style issues with security findings.
- Do not hide uncertainty; mark assumptions explicitly.

## Done Criteria

Consider the task done only when all applicable items are true:

- All required categories are reviewed.
- Findings are prioritized by severity.
- Each finding includes evidence and a concrete fix or mitigation.
- Non-findings and assumptions are stated when scope is partial.

## Response Format

Return a concise report with these sections:

- Scope and assumptions
- Prioritized findings
- Quick wins
- Follow-up validation needed
