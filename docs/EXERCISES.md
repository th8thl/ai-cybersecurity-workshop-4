# Session 4 exercises

This workshop focuses on identifying vulnerabilities and verifying findings. Use unchanged starter code for the comparisons. Exercise 5 temporarily changes the live ticket creation query and then restores it. Students compare the supplied vulnerable examples with repaired code and recommend repairs in their report. Implementing fixes is outside the student tasks in this workshop.

**Before you start.** Follow the [Codespaces guide](GITHUB_CODESPACES_SETUP.md) or [macOS and Windows guide](LOCAL_SETUP.md). In VS Code, open the folder in your local copy of the starter repo that contains `manage.py`, `scripts/`, and `review_examples/`. Choose **Terminal → New Terminal** and activate the starter Python environment. Run the commands below there unless the exercise specifies a browser or the Claude Code panel. Keep the portal running in a second terminal. If you use GitHub Codespaces, your account or course organization needs an available Codespaces allowance or billing.

Copy the [report template](REPORT_TEMPLATE.md) into your working folder as `session4-report.md`. Keep that file open in VS Code and fill in the matching section after each exercise. For GitHub and Claude Security, get the classroom repository URL, branch, and commit from your instructor before starting.

| Exercise | Tool | What this tests | Exact workshop matrix wording |
|---|---|---|---|
| 1. Map security decisions | Django portal and diagram | Identify where the application checks chat input, ticket permissions and retrieved documents. | “Create a threat-model diagram” |
| 2. Run static analysis | Bandit and Semgrep | Check which warnings are supported by source evidence. | “Classify findings by CWE” |
| 3. Review scanner output | Gemini API via Python google-genai | Check whether AI summarizes the two reports accurately. | “Run AI-assisted vulnerability analysis” |
| 4. Scan your GitHub repository | GitHub CodeQL | Check which known issues CodeQL identifies. | “Evidence validation” |
| 5. Review SQL injection in Request summary | Claude Code extension /security-review | Verify whether Claude identifies the unsafe query used by the live ticket form. | “Require evidence for findings” |
| 6. Scan the source in VS Code | Claude Security plugin | Verify and score a repository scan. | “Tool evidence validation” |
| 7. Review the running portal | Claude Code with Claude in Chrome and Django | Observe ticket approval, sign-out behavior, and deployment warnings. | “Evidence validation” · “Risk communication” |
| 8. Compare three reviews | Gemini API via Python google-genai and both Claude reports | Count confirmed findings, misses and false alarms on the same source. | “Compare models or prompts” · “Measure false positives and false negatives” |
| 9. Compare guardrails | NeMo Guardrails | Count which excerpts pass with the rail off and on. | “Compare guardrail strategies” |
| 10. Publish results | GitHub and report template | Document reproducible findings, repairs and report confidence. | “Write a final security report” |

## 1. Map security decisions

**Software:** Starter Python environment with Django, the running portal, a browser, and seeded demo accounts.

**Accounts and licenses:** No separate paid license. This exercise uses the local test suite and demo data.

1. **VS Code:** Open the [architecture diagram](system-architecture.svg). In your report, sketch the browser, Django portal, ticket service, ticket MCP server, and knowledge base. Add arrows for chat messages, ticket actions, and retrieved documents.
2. **Terminal:** Run `python manage.py test tests.test_prompt_security tests.test_chat_storage tests.test_ticket_access tests.test_authorization tests.test_approval`. Look for the test count and `OK`. If a test fails, record its name and the expected and actual results. Use the test names and assertions to label where chat data is handled and where ticket permissions are enforced.
3. **Open the ticket portal:** In your Codespace, select the **Ports** tab next to **Terminal**. Find port **8000** and click its **Open in Browser** icon. The Django portal should open in a new browser tab. Sign in with a demo account, select **Tickets**, and open one of your open tickets. Click **Close ticket**. Look for **Confirm ticket closure** and check that the status still says **Open**. Click **Yes, close ticket** and record whether the status changes to **Closed**. Mark on your diagram where the user and the ticket service each make a decision.

**Turn in:** The diagram and two observations, one for chat handling and one for ticket approval. Name the UI outcome or test assertion that supports each observation.

## 2. Run static analysis

Use [the scanner results guide](READING_SCAN_RESULTS.md) to interpret the files this exercise produces.

**Software:** Starter Python environment with Bandit and Semgrep Community Edition, VS Code, and a browser for the running portal.

**Accounts and licenses:** No paid scanner license or Semgrep account. Bundled scanner reports can be used if a local scanner fails.

1. **Terminal in your local starter repo:** Run `python scripts/run_sast.py --examples`. Look for one summary line per scanner. Open `results/examples/current/bandit.json` and `results/examples/current/semgrep.json` in VS Code. If a scanner fails, note the error and check its `.stderr.txt` file in the same folder. Use the corresponding `sample_reports/` JSON for the evidence review and label it as a saved report.
2. **VS Code:** In Bandit's `results` list, look at `test_id`, `filename`, and `line_number`. In Semgrep's `results` list, look at `check_id`, `path`, and `start.line`. Open the cited line in `review_examples/file_imports.py` or `review_examples/attachments.py`. Group warnings that describe the same weakness. For each group, cite the code, add the CWE from the instructor key when released, and record whether the code supports the warning.
3. **Portal in your browser:** Under **Tickets**, select **Import a ticket file**, click **Download a JSON example**, and upload the downloaded file in the import form. The portal should open the new ticket under your account. Select **Export ticket as JSON** and check that the downloaded file contains the same title. On that ticket, upload a small harmless text file and download it from the attachment list. Compare its contents with the original.
4. **Terminal:** Run `python manage.py test tests.test_file_uploads`. Look for `OK` and record the test count and one assertion that verifies the repaired behavior.

**Turn in:** The scanner filenames, rule IDs, source lines, verdicts, and test result. Keep both JSON reports open for Exercise 3.

## 3. Review scanner output with Gemini

**Software:** Starter Python environment with the google-genai SDK, internet access, and both Bandit and Semgrep JSON reports.

**Accounts and licenses:** A Gemini API key and an available model ID. A free API tier is sufficient if the selected model offers it and quota is available. Otherwise the API project needs billing. [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing)

1. **VS Code:** Open the local `.env` beside `manage.py`. Set `GEMINI_API_KEY` to your key and `GEMINI_MODEL` to the model ID supplied for class. Save the file and keep the key out of your report and Git commits.
2. **Terminal:** Run `python scripts/review_with_gemini.py scanner`. The script sends the two JSON reports from Exercise 2 to Gemini. If you are using the bundled reports, run `python scripts/review_with_gemini.py scanner --saved`. The terminal prints the output path when Gemini returns a review.
3. **VS Code:** Open `results/gemini-scanner.txt` beside the two input JSON reports. Choose one Gemini summary and match it to the original scanner, rule ID, and file location. Look for duplicate warnings that Gemini combined and claims it added without support in either report.

**Turn in:** The model ID, which pair of reports you used, one verified summary with its matching rule and location, and any unsupported claim you found.

## 4. Scan your GitHub repository with CodeQL

**Software:** Browser, public workshop repository, and GitHub Actions enabled in that repository.

**Accounts and licenses:** A GitHub account with admin access to your public workshop repository. CodeQL is available on public repositories without buying GitHub Code Security. [GitHub CodeQL setup](https://docs.github.com/en/code-security/how-tos/find-and-fix-code-vulnerabilities/configure-code-scanning/configure-code-scanning)

1. **In your web browser:** Open **github.com** and select the workshop repository you created from the Session 4 template. On that repository page, click the **Actions** tab above the file list, alongside **Code** and **Pull requests**. If GitHub displays a button to enable workflows, click it. Otherwise, continue to **Settings**.
2. **Enable CodeQL.** Open **Settings → Advanced Security → CodeQL analysis → Set up → Default**. Check that Python is selected and enable the scan.
3. **In the same GitHub repository, in your browser:** Open **Actions** and click the CodeQL run to follow its progress. The scan can take **3–5 minutes**; the first run can take longer. Record the scanned branch and commit. Once it succeeds, return to your repository’s main page. Under the repository name, click **Security and quality**. If it is hidden, open the overflow dropdown in that tab row. In the left sidebar, click **Code scanning** to see the results. For any alert about the two reviewed files, open it and check the rule, path, and highlighted lines against your local copy. Record zero relevant alerts only after a successful scan. If the run fails, record the failed step and workflow link.

**Turn in:** Your repository URL, the workflow or alert link, the scanned commit, and a row for each file showing whether CodeQL flagged it. Use the same two files and findings as Exercise 2 when comparing scanners.

[GitHub CodeQL setup guide](https://docs.github.com/en/code-security/how-tos/find-and-fix-code-vulnerabilities/configure-code-scanning/configure-code-scanning)

## 5. Have Claude review SQL injection in Request summary

**What and why:** Change the database operation used by New ticket → Request summary. The current Django ORM call safely passes values to the database. The replacement inserts the submitted title directly into SQL, introducing CWE-89, SQL Injection. This request reaches real ticket storage, so the reviewer can trace its impact through the running application.

**Software and access:** Codespaces VS Code, the running Django portal, and the signed-in Claude Code extension with available usage. Work only in your workshop starter copy. The instructions modify an existing tracked file; no new file, branch, or commit is required.

1. **Open the existing file.** In Codespaces VS Code Explorer, expand starter → tickets and open local_adapter.py. Find the create_ticket block below. The Request summary form sends its value to arguments["title"] through views.ticket_create and ticket_service.execute.

```python
    if tool == "create_ticket":
        ticket = Ticket.objects.create(owner=actor, title=arguments["title"])
```

2. **Replace only those two lines.** Paste the block below in their place and save. Keep the following elif block and the rest of the file as they are. The login, owner assignment, and ticket approval code remain present; the title is the value deliberately placed inside SQL.

```python
    if tool == "create_ticket":
        from django.db import connection

        title = arguments["title"]
        query = (
            "INSERT INTO tickets_ticket (owner_id, title, status) "
            f"VALUES (%s, '{title}', 'open')"
        )
        with connection.cursor() as cursor:
            cursor.execute(query, [actor.pk])
            ticket_id = cursor.lastrowid
        ticket = Ticket.objects.get(pk=ticket_id)
```

3. **Check the normal path.** In the running portal, open Tickets → New ticket. Enter Registration help in Request summary and submit. Expect a new open ticket under your demo account. If it fails, inspect the Codespaces server terminal before continuing.
4. **Confirm the review can see the change.** In a Codespaces terminal, from starter, run:

```bash
git diff -- tickets/local_adapter.py
```

Expect the diff to show Ticket.objects.create replaced by the raw INSERT. No output means the edit was not saved in this repository.

5. **Run the command in the Claude Code panel.** Paste the following and submit:

```text
/security-review Review the uncommitted change in starter/tickets/local_adapter.py using git diff -- starter/tickets/local_adapter.py. Trace Request summary from the POST handler in starter/tickets/views.py through ticket_service.execute to the changed create_ticket database operation. Identify security vulnerabilities and explain the source evidence. Do not edit files.
```

If the workspace root is starter, remove starter/ from the paths in the command. If the built-in step fails on origin/HEAD, use the recovery instructions below and retry.
6. **Verify and record.** Look for CWE-89 and the f-string inserting title into the query. The report should connect the browser's Request summary field to this SQL operation. Authentication does not make a user's title safe SQL. Save the finding and cited lines, or record a miss if the changed code was covered without the issue being reported.
7. **Restore the supplied implementation.** Replace the entire create_ticket block you inserted with the original two-line block from step 1. Save. Run git diff -- tickets/local_adapter.py again from starter and check that the exercise edit is gone. Create another ordinary ticket to confirm normal behavior. This restores the supplied code after the demonstration; students are not asked to design a repair.

**Turn in:** Claude's review, the vulnerable query, and one sentence tracing Request summary to the database. Keep this live-code result separate from the earlier screenshots of isolated teaching examples and from the importer/downloader comparison.

## If /security-review reports unknown revision origin/HEAD

In Codespaces VS Code, select **Terminal → New Terminal**. From the workshop repository, run:

```bash
git fetch origin
git remote set-head origin --auto
git symbolic-ref refs/remotes/origin/HEAD
```

The last command should print `refs/remotes/origin/main` if main is the default branch. Return to the Claude Code panel and retry `/security-review`.

If automatic detection fails, and your GitHub repository's default branch is main, run:

```bash
git remote set-head origin main
git symbolic-ref refs/remotes/origin/HEAD
```

Expect `refs/remotes/origin/main`. If your repository uses another default branch, replace main with that branch name. A completed review with no branch changes is a separate outcome from this Git error.

## 6. Scan the source with the Claude Security plugin

**Software:** Claude Code extension in your Codespaces VS Code workspace and the official Claude Security plugin.

**Accounts and licenses:** Claude Code access with available subscription usage or API billing. The plugin uses the model and usage available in your Claude Code session. A managed organization may need to allow plugin installation. This exercise runs through the plugin in your session.

1. **Install the plugin in the Claude Code panel.** In the message box, enter `/plugin install claude-security@claude-plugins-official`, then `/reload-plugins`. If the marketplace is missing, enter `/plugin marketplace add anthropics/claude-plugins-official` and retry installation. If `/claude-security:scan` already appears in the command list, the plugin is installed.
2. **Start the plugin scan from the Claude Code panel.** Keep the vulnerable Request summary replacement from Exercise 5 in place until this scan completes. If you restored it, reapply the supplied replacement first. In Codespaces VS Code, open the Claude Code panel and click its message box. Paste this request and submit it:

```text
Use the Claude Security plugin to review starter/tickets/local_adapter.py for security vulnerabilities and save the report. Do not modify the code.
```

If the open workspace root is starter, remove starter/ from both paths. The plugin should identify the target files and describe the effort and usage cost. Check that it selected the changed create_ticket query and its request path, then confirm the scan.

3. **Observe the scan.** Watch the stage updates in the Claude Code panel. Wait for the final report path. If the command fails, record the error. A failed run has no findings score.
4. **Read the generated report.** In the VS Code Explorer, open the new CLAUDE-SECURITY-<timestamp> folder and its CLAUDE-SECURITY-RESULTS.md file. Look for each finding’s source location, severity, confidence, explanation, and recommendation. Check the cited lines in the starter source. Record whether they support the claim.
5. **Save your comparison and restore the code.** Restore the original create_ticket ORM call from Exercise 5 after saving the scan report.  Add the report path, files covered, model if shown, and confirmed findings, misses and false alarms to your report. Keep this generated report for Exercise 8.

[Official Claude Security plugin documentation](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/claude-security/README.md)

## 7. Review the running portal with Claude Code

**Software:** Running Django portal, demo account, desktop Google Chrome with Claude in Chrome enabled, and Claude Code CLI.

**Accounts and licenses:** A paid Claude plan with Claude in Chrome access (Pro, Max, Team, or Enterprise). Sign Claude Code and Chrome into the same Claude account and organization. A managed workspace may require admin enablement. [Claude in Chrome access](https://support.claude.com/en/articles/12012173-get-started-with-claude-in-chrome) · [Claude Code integration](https://code.claude.com/docs/en/chrome)

1. **VS Code integrated terminal:** In your local copy of the starter repo, reuse the development server from setup. If it is stopped, activate the Python environment and run `python manage.py runserver 127.0.0.1:8000` locally or `python manage.py runserver 0.0.0.0:8000` in Codespaces. Keep that terminal open. In Chrome on the same machine, open [the local portal](http://127.0.0.1:8000/) and sign in with your workshop demo account. For Codespaces, use the private forwarded port URL from **Ports**.
2. **Claude Code and Chrome:** Install or enable **Claude in Chrome** using the [Anthropic setup guide](https://code.claude.com/docs/en/chrome). In a second VS Code terminal, run `claude --chrome`. At the Claude Code prompt, ask it to observe your workshop portal tab while you perform the checks below. Enter the demo credentials yourself. Give Claude the portal URL and limit its review to that tab.
3. **Chrome:** Open one of your own open demo tickets. Click **Close ticket** and check that the confirmation prompt appears while the ticket still says **Open**. Click **Yes, close ticket** and check that the status changes to **Closed**. Copy the ticket page URL, sign out, then reopen that URL. Look for the login page or redirect. Ask Claude to summarize the observed behavior and identify any unexpected console errors or sensitive information displayed. If Claude cannot see an outcome, record it yourself and label it a manual observation.
4. **Django deployment check:** In another terminal with the same Python environment, run `python manage.py check --deploy`. Ask Claude to explain one warning using the command output. Record the warning ID, why it appeared in this environment, and what should change or be checked before public deployment.

**Turn in:** The portal URL, expected and observed outcomes for closure and sign-out, and one deployment warning with its explanation. Record the visible status or redirect as evidence. Continue to Exercise 8 for the separate source-review comparison.

## 8. Compare Gemini and both Claude reviews

**Software:** Starter Python environment with google-genai, the two source files, both Claude reports, and the instructor scoring key.

**Accounts and licenses:** Reuse the Gemini API key and model access from Exercise 3. Comparing the saved Claude reports requires no additional Claude subscription or scan.

1. **Terminal in your local starter repo:** Using the unchanged starter code, run `python scripts/review_with_gemini.py source`. This sends `review_examples/file_imports.py` and `review_examples/attachments.py` to Gemini. Open `results/gemini-source.txt` in VS Code and check the model ID at the top.
2. **VS Code:** Open that file and the two Claude reports. Make one row per reviewer. Record the commit, model if shown, files reviewed, and any extra repository context. If a report is from a different revision or its scope is unclear, record that in the comparison.
3. **Score from the instructor key:** Count each supported known issue once per reviewer. Mark an issue **missed** when the reviewer covered the file and omitted the issue. Mark a file **not reviewed** when it was outside the review or coverage cannot be established. Count a distinct claim contradicted by source evidence as a false alarm. Record unresolved claims separately.
4. Pick one difference between the reports. Point to the exact source lines and explain why the difference changes your score or confidence.

**Turn in:** Three completed rows in the review-results table, links or paths to the reports, and your evidence for one difference.

## 9. Compare NeMo off and on

**Software:** Starter Python environment with the pinned NeMo Guardrails package and the workshop policy files.

**Accounts and licenses:** No paid plan or API key. This script runs the local deterministic policy and does not call Gemini, Claude, or Ollama.

1. **Terminal in your local starter repo:** Run `python scripts/compare_nemo.py`. The script replays a normal review excerpt and an excerpt containing an instruction embedded in repository text. It runs each once with NeMo disabled and once with NeMo enabled.
2. **Read the terminal output:** Look for four JSON lines. For each, copy `case`, `nemo`, and `passed` into your report. In `trace`, look for `skipped: true` when NeMo is disabled and the decision plus active flows when enabled. Expect both excerpts to pass with NeMo off. With it on, expect the normal excerpt to pass and the misleading excerpt to be blocked. If the worker reports an error, record the error and leave that outcome unscored.
3. **Explain the result:** Cite one trace that shows the decision changed. Separately verify whether the source evidence supports a finding. The benchmark measures how the retrieval rule handles these two excerpts.

**Turn in:** A two-row table with each excerpt's result for NeMo off and on, plus the trace supporting one observed change.

## 10. Publish a report

**Software:** Markdown editor, Git, browser, and the completed report and evidence from the preceding exercises.

**Accounts and licenses:** A GitHub account with write access to your workshop repository. No paid plan is required to commit the Markdown report and push it to that public repository.

1. **VS Code:** In `session4-report.md`, add the repository and commit, your diagram, scanner results, Gemini scanner-output check, three source-review scores, runtime observations from Exercise 7, and NeMo outcomes. For each confirmed issue, include the file and line, CWE, impact, repair, and the test or scan result that supports the repair.
2. **Write the priority:** Choose which issue to fix first. Give the reason in one sentence and name the check you would rerun after the fix. For report confidence, give one sentence each on how prompt injection, poisoned retrieved documents, a poisoned model or fine-tune, and a contaminated benchmark could affect the exercise results.
3. **Terminal in your local starter repo:** Run `git status --short` and check that `session4-report.md` is the intended submission. Stage it with `git add session4-report.md`, review it with `git diff --cached -- session4-report.md`, and confirm the staged files list from `git diff --cached --name-only` contains only your report. Commit with `git commit -m "Add Session 4 security report"`. Run `git remote -v` and identify the remote whose push URL points to your workshop repository. Run `git push <repository-remote> HEAD:<submission-branch>`, replacing both placeholders with that remote name and the branch your instructor provided. Include report excerpts without credentials or private account information.
4. **GitHub in your browser:** Open your workshop repository, select the branch you pushed, and open `session4-report.md`. Check that the tables render and your evidence links open.

**Turn in:** The GitHub link to the rendered report on your submission branch.
