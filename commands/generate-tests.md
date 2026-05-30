---
description: Generate targeted automated tests for an existing module, function, route, or component with edge cases, error paths, and minimal mocks. Use when the user asks to write tests, generate tests, increase coverage, or validate behavior with tests, including prompts like "generame los test", "haz los test que consideres necesarios", or "comprueba que la API funciona con tests". Prefer this over fix-bug when the main goal is coverage or test creation, not debugging an active failure.
---

# Generate Tests

## Overview

Generate focused tests that improve confidence, not just line coverage.
Prioritize behavior, edge cases, and failure modes over implementation details.

## Workflow

1. Inspect the target module and existing tests.
2. Identify the public behaviors and missing coverage.
3. Build a small test matrix (happy path, edges, errors, invalid input).
4. Implement tests using the project's current framework and style.
5. Use mocks only when isolation is necessary.
6. Run the relevant tests and coverage command if available.
7. Report what was covered and any remaining gaps.

## Step Details

### 1. Inspect the Surface Area

- Read the target file and identify exported functions, routes, or component behavior.
- Read nearby tests first to match naming, assertions, and setup style.
- Prefer testing the public interface over private helpers.

### 2. Identify Missing Cases

- Cover the main success path.
- Cover boundary values and empty states.
- Cover invalid inputs and thrown/rejected errors.
- Cover branching logic and fallback behavior.
- Cover async behavior, timing assumptions, or loading/error states when relevant.

### 3. Build the Test Matrix

- Start with a minimal list of high-value scenarios.
- Add edge cases only when they map to real branches or likely failures.
- Avoid redundant tests that repeat the same behavior with different names.

### 4. Implement Tests

- Reuse existing helpers and fixtures before creating new abstractions.
- Keep each test readable and focused on one behavior.
- Use descriptive names that explain the expected outcome.
- Prefer deterministic assertions over snapshots unless snapshots are already the repo norm.

### 5. Use Mocks Carefully

- Mock network, time, randomness, or external services when needed for determinism.
- Avoid mocking internal modules if the test can exercise real behavior cheaply.
- Do not create elaborate mock setups for simple logic.

### 6. Validate

- Run the target test file first.
- Run a broader related suite if changes touch shared helpers.
- Run coverage when the user requested a threshold or the repo has a standard command.
- Report exact commands not executed if tooling is unavailable.

## Guardrails

- Do not rewrite production code only to make tests easier unless a real testability issue exists.
- Do not assert on implementation details that make tests brittle.
- Do not add unnecessary `beforeEach` or helper layers for a small test file.
- Do not fake coverage by testing trivial lines only.

## Done Criteria

Consider the task done only when all applicable items are true:

- New tests compile and run in the project test framework.
- High-value behaviors (success, edge, error) are covered.
- Mocks are minimal and justified.
- Coverage target is met if the user specified one, or coverage improvement is reported.
- Validation commands and outcomes are reported clearly.

## Response Format

Return a concise report with these sections:

- Scope tested
- Cases added
- Mocking choices
- Validation run
- Remaining gaps
