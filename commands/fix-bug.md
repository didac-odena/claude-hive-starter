---
description: Systematic debugging and minimal bug fixing for failing tests, runtime errors, crashes, stacktraces, and regressions. Use when the user asks to debug or fix broken behavior, reproduce a failure, isolate root cause, or says phrases like "arregla este bug", "creo que hay un bug por aqui", "esto me da error", or "algo esta fallando". Prefer this over generate-tests when the main goal is fixing behavior rather than only adding tests.
---

# Fix Bug

## Overview

Use a strict debugging workflow to avoid speculative fixes and regressions.
Prefer the smallest behavior change that makes the failing case pass.

## Workflow

1. Define the target bug and success condition.
2. Reproduce the failure with an existing test, command, or minimal repro.
3. Isolate the failure point and identify the root cause.
4. Add or update a failing regression test before changing code whenever possible.
5. Implement the minimum fix that resolves the root cause.
6. Validate with targeted tests first, then broader tests/lint when available.
7. Summarize root cause, fix, test coverage, and validation results.

## Step Details

### 1. Define the Target

- Extract the exact error, broken behavior, or acceptance criteria from the user request.
- Ask for a missing repro only when the failure cannot be reproduced from local context.
- Preserve public API and external behavior unless the user explicitly approves a change.

### 2. Reproduce the Failure

- Run the smallest command that reproduces the issue first (single test, filtered test file, specific script).
- Capture the failing assertion, stacktrace, and inputs.
- Avoid changing code before reproducing unless the project is currently broken and needs setup fixes.

### 3. Isolate the Root Cause

- Trace from the failing output back to the exact code path.
- Inspect recent changes, assumptions, and branch conditions.
- Confirm the hypothesis with a focused check instead of guessing.

### 4. Add Regression Coverage

- Add a test that fails before the fix and passes after the fix.
- Keep the test narrow and behavior-focused.
- Reuse the repo's current test framework and style.
- If automated tests do not exist, create the smallest reproducible check and state the limitation.

### 5. Implement the Minimum Fix

- Change only the code required to resolve the confirmed root cause.
- Avoid refactors, renames, and cleanup unrelated to the bug.
- Remove temporary debug logs or instrumentation before finishing.

### 6. Validate

- Run the new/updated regression test.
- Run the affected test file or suite.
- Run lint if the repo uses it and the command is available.
- Report any command that could not be run and why.

## Guardrails

- Do not silence failing tests instead of fixing behavior.
- Do not broaden the fix without evidence of additional impacted paths.
- Do not change public API, response shapes, or UI copy unless required and approved.
- Do not claim a fix is complete without validation output.

## Done Criteria

Consider the task done only when all applicable items are true:

- The failure is reproduced or the reason it cannot be reproduced is explicit.
- The root cause is identified.
- A regression test is added or updated (or a limitation is clearly documented).
- The minimum code fix is implemented.
- Relevant tests pass.
- Lint passes or the inability to run lint is reported.

## Response Format

Return a concise report with these sections:

- Root cause
- Fix applied
- Regression test
- Validation run
- Remaining risks or follow-ups
