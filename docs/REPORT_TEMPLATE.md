# Security report

Repository, branch, and commit:

## Threat model

Attach a diagram showing user input, application checks, ticket ownership and approval, file handling, MCP, retrieval and external reviewers.

## Findings

| File and line | Evidence | CWE | Impact | Recommended repair | Verification |
|---|---|---|---|---|---|

## Review results

| Tool and mode | Input and commit | Confirmed | Missed | False alarms | Report link |
|---|---|---:|---:|---:|---|
| Bandit | | | | | |
| Semgrep | | | | | |
| GitHub CodeQL | | | | | |
| Claude Code /security-review | | | | | |
| Claude Security | | | | | |
| Gemini source review | | | | | |

Record your Gemini scanner-summary check here. Include input report paths, Gemini model ID, the original rule and location, and any unsupported claim. Explain one difference between reviewers.

## Runtime review

Portal URL:

| Check | Expected outcome | Observed outcome | Evidence |
|---|---|---|---|
| Ticket closure confirmation | Ticket stays open until confirmed | | |
| Reopen ticket after sign-out | Portal requires sign-in | | |

Deployment warning ID, explanation, and what to check before deployment:

## Guardrail comparison

| Excerpt | Expected behavior | NeMo off | NeMo on | Decision evidence |
|---|---|---|---|---|

## Recommended priority and confidence

Name the first repair and how to verify it. Describe prompt injection, poisoned runtime content, model poisoning and benchmark contamination in terms of how each could affect your results.
