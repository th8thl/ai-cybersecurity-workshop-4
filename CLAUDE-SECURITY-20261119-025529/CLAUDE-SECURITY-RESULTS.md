# Claude Security results

This is a codebase scan of `starter/review_examples` in this repository, at commit `5bc04aa` on `main`. It ran on 2026-11-19 (UTC) at `medium` effort. The working tree held uncommitted changes or untracked files when the scan ran. **No findings survived verification.** The researcher proposed three candidates. The verification panel rejected all three as unreachable: the code patterns are genuinely unsafe, but no code path an attacker controls leads to them.

## Coverage

The scan covered only `starter/review_examples`, because the request named that directory. That scope holds 3 tracked files: `README.md`, `attachments.py` and `file_imports.py`. Because the scope is small, the run used the single-researcher shape instead of the full component matrix. That is a fast, targeted pass, still checked by the panel, not an exhaustive read. One researcher was dispatched and it returned, reading the scope for every kind of vulnerability. The researcher also examined the untracked `sql_injection_demo.py` in the same directory. A completeness check does not apply to a scoped scan. Nothing was deliberately skipped, and no candidates were lost. The panel finished in one verification run.

Nothing outside `starter/review_examples` was examined as a target, including the live Django application under `starter/tickets`. The panel did consult that code to decide whether the review examples are reachable from it.

## Findings

No findings.

Three candidates were proposed, and the full three-voter panel rejected each one:

- **Unsafe deserialization:** `starter/review_examples/file_imports.py:11`. `pickle.loads` runs on uploaded bytes when the filename ends in `.pkl`, and validation only runs afterward. All three voters rejected it (0/3) because nothing in the repository imports or calls this module.
- **Path traversal:** `starter/review_examples/attachments.py:38`. `(folder / name).open('rb')` opens a path with no containment check, so `../` sequences and absolute names both get through. One voter of three confirmed it, which falls short of the 2-of-3 bar. The other two voters found that the only live route, `starter/tickets/views.py:128`, is bound to the repaired `starter/tickets/attachments.py` and not to this copy.
- **SQL injection:** `starter/review_examples/sql_injection_demo.py:14`. An f-string puts `title` into the query. All three voters rejected it (0/3) because `find_tickets` has no callers. Each call also queries a fresh private in-memory SQLite database seeded with one hard-coded, non-sensitive row, so an injection could reach nothing worth having.

These are intentional teaching examples: the folder's README describes them as source-only material. If any of this code is copied into a reachable request handler, all three patterns become real vulnerabilities. The deserialization and path traversal would be high-impact.

## What was verified

One researcher read the scope for every vulnerability category and proposed three candidates. Each candidate went to an independent three-voter panel, with one voter each checking reachability, impact and defenses, and needed 2 of 3 votes to survive. None survived: the votes were 0/3, 1/3 and 0/3, so the panel cast 9 votes in all. All of this came from reading the code. No code was executed, no tests were run, and no exploit was attempted. The verification status is the one stamped by the renderer alongside this report.
