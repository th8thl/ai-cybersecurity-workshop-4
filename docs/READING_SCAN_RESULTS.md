# How to read the scanner results

Start with results/examples/current. These reports cover the two Python files in review_examples/. They were produced by python scripts/run_sast.py --examples.

| File | What it contains | What to look for |
|---|---|---|
| bandit.json | Python security warnings | Each item in results is one warning. Read test_id, issue_text, filename and line_number. |
| semgrep.json | Matches against scripts/semgrep.yml | Each item in results is one warning. Read check_id, extra.message, path and start.line. |
| bandit.stderr.txt | Scanner diagnostics | Empty can be normal. Read it if Bandit fails to produce a valid report. |
| semgrep.stderr.txt | Progress and scanner diagnostics | Look for Scan completed successfully. Text in this file can be ordinary progress output. |

## What the supplied solution reports say

Both JSON reports have an empty results list and no reported errors. Semgrep's log confirms a completed scan of two Python files using four rules. The solution examples produced zero warnings in that run. This result applies to those files and those checks. It does not establish that the entire application is secure.

## What the supplied starter reports say

| Scanner | Warning | Code location | Interpretation |
|---|---|---|---|
| Bandit | B403 | review_examples/file_imports.py, line 3 | Importing pickle deserves review. The import alone does not establish unsafe handling of uploaded data. |
| Bandit | B301 | review_examples/file_imports.py, line 11 | The parser calls pickle.loads. Check whether uploaded data reaches it. |
| Semgrep | workshop-unsafe-deserialization | review_examples/file_imports.py, line 11 | The supplied rule matched the same pickle call. Count one underlying deserialization issue after verifying the data source. |
| Semgrep | workshop-path-traversal | review_examples/attachments.py, line 38 | The supplied rule matched a file path operation. Read the surrounding code to check containment and attachment ownership. |

## How to verify one warning

1. Open the path named by the warning in the same starter or solution copy that produced the report.
2. Use VS Code's Go to Line command (Ctrl+G) and enter its line number.
3. Read the function around that line. Identify where the input comes from and what checks happen before the operation.
4. Record the warning, source evidence and verdict. Group repeated warnings about the same underlying weakness.
5. Record an unsuccessful scan as failed. A failed scan cannot be scored as zero findings.

Students review the starter examples. The solution folder supplies the repaired comparison. Reports are snapshots of a particular run and can become outdated if the files or rules change.
