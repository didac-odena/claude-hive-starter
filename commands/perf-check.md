---
description: Analyze code for performance bottlenecks and propose concrete, prioritized optimizations for database queries, loops, rendering, network calls, and caching. Use when the user reports slowness or asks to optimize performance, review if something is optimized, or detect bottlenecks, including prompts like "esto va lento", "optimiza esto", "revisa que esto este optimizado", or "mira si esto realmente esta optimizado". Prefer this over design-review when the main goal is runtime speed rather than architecture.
---

# Perf Check

## Overview

Review code for likely bottlenecks and prioritize recommendations by impact and effort.
Prefer concrete, incremental changes over broad refactors.

## Workflow

1. Define the scope and performance goal (latency, throughput, render speed, query time).
2. Identify hot paths from code structure and any available measurements.
3. Review common bottleneck categories.
4. Rank findings by expected impact and implementation cost.
5. Propose concrete changes and a validation plan.
6. Report prioritized recommendations with evidence.

## Review Categories

Review these categories at minimum when relevant:

- Database access patterns (N+1, missing filters, missing indexes, repeated queries)
- Algorithm and loop costs (nested loops, repeated work, large allocations)
- API or network calls (chatty requests, redundant fetches, serialization overhead)
- Frontend rendering (re-renders, heavy derived calculations, large lists)
- Caching opportunities and invalidation risks

## Review Method

### 1. Establish Context

- Identify the endpoint, component, job, or function that matters.
- Ask for real measurements only when they are needed to choose between options.
- Use existing logs, traces, or slow test output when available.

### 2. Find Hotspots

- Trace repeated work in loops and nested traversals.
- Trace repeated DB queries inside request loops or per-item rendering.
- Trace expensive parsing, sorting, or serialization done on every call.
- Trace unnecessary frontend re-renders or list rendering without virtualization for large datasets.

### 3. Recommend Changes

- Suggest the smallest high-impact change first.
- State tradeoffs (memory, complexity, correctness risk).
- Suggest measurement steps to confirm improvement.

## Prioritization Rules

Rank items using:

- Impact: expected speedup or reduced load
- Frequency: how often the path runs
- Effort: implementation complexity and regression risk

Prefer a short list of strong recommendations over a long list of minor tweaks.

## Guardrails

- Do not recommend micro-optimizations before fixing high-impact bottlenecks.
- Do not suggest caching without naming invalidation or staleness risks.
- Do not assume a problem is real if code evidence is weak; mark it as a hypothesis.
- Do not trade correctness for speed without explicit user approval.

## Done Criteria

Consider the task done only when all applicable items are true:

- Findings are prioritized by impact.
- Each recommendation includes evidence and a concrete change.
- Tradeoffs or assumptions are stated.
- A simple validation plan is included (benchmark, test, profiling step, query plan, etc.).

## Response Format

Return a concise report with these sections:

- Scope and assumptions
- Prioritized bottlenecks
- Recommended changes
- Validation plan
