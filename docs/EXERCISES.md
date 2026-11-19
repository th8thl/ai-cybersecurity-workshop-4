# Session 4 exercises

This workshop focuses on identifying vulnerabilities and verifying findings. Run every scan on your unchanged starter code. Students compare the supplied vulnerable examples with repaired code and recommend repairs in their report. Implementing fixes is outside the student tasks in this workshop.

**Before you start.** Follow the [Codespaces guide](GITHUB_CODESPACES_SETUP.md) or [macOS and Windows guide](LOCAL_SETUP.md). In VS Code, open the folder in your local copy of the starter repo that contains `manage.py`, `scripts/`, and `review_examples/`. Choose **Terminal → New Terminal** and activate the starter Python environment. Run the commands below there unless the exercise specifies GitHub, Claude Security, or the portal in your browser. Keep the portal running in a second terminal. If you use GitHub Codespaces, your account or course organization needs an available Codespaces allowance or billing.

Copy the [report template](REPORT_TEMPLATE.md) into your working folder as `session4-report.md`. Keep that file open in VS Code and fill in the matching section after each exercise. For GitHub and Claude Security, get the classroom repository URL, branch, and commit from your instructor before starting.

| Exercise | Tool | What this tests | Exact workshop matrix wording |
|---|---|---|---|
| 1. Map security decisions | Django portal and diagram | Identify where the application checks chat input, ticket permissions and retrieved documents. | “Create a threat-model diagram” |
| 2. Run static analysis | Bandit and Semgrep | Check which warnings are supported by source evidence. | “Classify findings by CWE” |
| 3. Review scanner output | Gemini API via Python google-genai | Check whether AI summarizes the two reports accurately. | “Run AI-assisted vulnerability analysis” |
| 4. Scan a GitHub fork | GitHub CodeQL | Check which known issues CodeQL identifies. | “Evidence validation” |
| 5. Review code in the terminal | Claude Code /security-review | Verify and score a terminal review. | “Require evidence for findings” |
| 6. Review a repository scan | Claude Security | Verify and score a repository scan. | “Tool evidence validation” |
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

## 4. Scan your GitHub fork with CodeQL

**Software:** Browser, public starter repository fork, and GitHub Actions enabled on that fork.

**Accounts and licenses:** A GitHub account with admin access to your own public fork. CodeQL is available on public repositories without buying GitHub Code Security. [GitHub CodeQL setup](https://docs.github.com/en/code-security/how-tos/find-and-fix-code-vulnerabilities/configure-code-scanning/configure-code-scanning)

1. **Create your own copy of the starter code on GitHub.** In your browser, sign in to your personal GitHub account and open the course’s public Session 4 starter repository. Click **Fork**. On the **Create a new fork** page, select your own GitHub username under **Owner**, then click **Create fork**. GitHub should open the copy under your account. Check that the URL starts with `https://github.com/YOUR-USERNAME/` and that the file list contains `manage.py` and `review_examples/`. Save this repository URL. If you already have your own fork of the course starter, open it and make the same checks. Then open **Actions** in your copy and enable workflows if GitHub prompts you.
2. **In your fork:** Open **Settings → Advanced Security** under **Security and quality**. Under **Code Security**, select **CodeQL analysis → Set up → Default**. Confirm that Python appears in the configuration and enable CodeQL. If the setting is missing, check that you are in the public fork you own and that Actions is enabled.
3. **GitHub:** Open **Actions** and find the CodeQL run. Record the scanned branch and commit. Wait for it to finish. Once it succeeds, open **Security → Code scanning**. For any alert about the two reviewed files, open it and check the rule, path, and highlighted lines against your local copy. Record zero relevant alerts only after a successful scan. If the run fails, record the failed step and workflow link.

**Turn in:** Your fork URL, the workflow or alert link, the scanned commit, and a row for each file showing whether CodeQL flagged it. Use the same two files and findings as Exercise 2 when comparing scanners.

[GitHub CodeQL setup guide](https://docs.github.com/en/code-security/how-tos/find-and-fix-code-vulnerabilities/configure-code-scanning/configure-code-scanning)

## 5. Review code with Claude Code /security-review

**Software:** Claude Code CLI installed and signed in, Git, and a terminal in your local copy of the starter repo.

**Accounts and licenses:** For a live run, use a Claude plan that includes Claude Code or an Anthropic Console account with pay-as-you-go API billing. If using the in-class saved report, no Claude account is needed for that review. [Claude Code security review access](https://support.anthropic.com/en/articles/11932705-automated-security-reviews-in-claude-code/)

1. **Open a terminal in your local copy of the starter repo.** Use PowerShell on Windows, Terminal on macOS, or the integrated terminal in VS Code. In VS Code, open the starter repo folder and choose **Terminal → New Terminal**. The commands below run in that terminal.
   
   ```text
   claude
   ```

   Launch Claude from the starter folder containing review_examples/. Expect an interactive Claude Code prompt.

2. **Start the review.** At the Claude Code prompt, type `/security-review` and press Enter. Read the response in the same terminal. Look for a file path, a line number or code excerpt, and an explanation of the suspected weakness. This command can focus on pending branch changes. If it reports an empty diff or does not cover both files below, use the instructor's saved Claude Code report from the same commit. Use that report also if you cannot launch or sign in to Claude Code. Record which report you used and the files it covers.

3. **Verify one claim.** Open the cited line in `review_examples/file_imports.py` or `review_examples/attachments.py` in your editor. For the importer, check whether the cited code validates uploaded data before parsing it. For the downloader, check whether the cited code confines access to the current ticket's attachment folder and record. Quote the lines that support or contradict the claim. If the report has no claims about either file, record that and state whether the report establishes that both files were reviewed.

4. **Score and save your results.** Use the instructor key to count confirmed issues, missed issues and false alarms. Count a known issue as missed only when the report covers its file. Mark an omitted file as **not reviewed**. Save the report text and commit hash, then fill in the Claude Code row in the [report template](REPORT_TEMPLATE.md). Keep the report for Exercise 8.

## 6. Generate and verify a Claude Security report

**Software:** Browser, published GitHub starter repository, and a GitHub account connected to Claude.

**Accounts and licenses:** Claude Enterprise with a premium seat, usage billing enabled, and permission to create projects. The Enterprise owner enables Claude Security and a GitHub owner grants the Claude GitHub App access to the course repository. [Claude Security requirements](https://support.claude.com/en/articles/14661296-use-claude-security)

1. **Choose your starter repository.** Open your own GitHub copy of the course starter. Use the same unchanged starter code as the other reviews.
2. **Create a project to start the scan.** Go to [claude.ai/security](https://claude.ai/security) in your browser and sign in to the Enterprise workspace your instructor specifies. Click **New project**, enter a name such as **Session 4 — your name**, and add the course GitHub repository. Select the branch containing the unchanged starter code. Set the folder scope to `review_examples` and include the repository for findings. Click **Create project**. Claude Security starts the first scan automatically. Open **Activity** to see the run and wait until it completes. If **New project** is missing or the repository is unavailable, ask your instructor to check your project permissions and the GitHub App's access. Record the scan status and the scanned commit if shown. A pending or failed scan has no score.
3. **Read the findings.** On the project page, open **Findings** and look for findings citing `review_examples/file_imports.py` or `review_examples/attachments.py`. Open one and compare its **Evidence** path and line range with the same lines in your local copy of the starter repo. Record the finding title, severity, CWE if shown, and the source lines that support or contradict it. If the completed run has no findings for these files, record that and check the scan scope before counting a miss.
4. **Save your report.** Fill in the **Claude Security** row in the [report template](REPORT_TEMPLATE.md) with your scan link, scanned revision, and counts of confirmed findings, misses, and false alarms. Keep the evidence from step 3 for Exercise 8.

[Claude Security documentation](https://support.claude.com/en/articles/14661296-use-claude-security)

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

**Accounts and licenses:** A GitHub account with write access to your submission fork. No paid plan is required to commit the Markdown report and push it to that public fork.

1. **VS Code:** In `session4-report.md`, add the repository and commit, your diagram, scanner results, Gemini scanner-output check, three source-review scores, runtime observations from Exercise 7, and NeMo outcomes. For each confirmed issue, include the file and line, CWE, impact, repair, and the test or scan result that supports the repair.
2. **Write the priority:** Choose which issue to fix first. Give the reason in one sentence and name the check you would rerun after the fix. For report confidence, give one sentence each on how prompt injection, poisoned retrieved documents, a poisoned model or fine-tune, and a contaminated benchmark could affect the exercise results.
3. **Terminal in your local starter repo:** Run `git status --short` and check that `session4-report.md` is the intended submission. Stage it with `git add session4-report.md`, review it with `git diff --cached -- session4-report.md`, and confirm the staged files list from `git diff --cached --name-only` contains only your report. Commit with `git commit -m "Add Session 4 security report"`. Run `git remote -v` and identify the remote whose push URL points to your fork. Run `git push <fork-remote> HEAD:<submission-branch>`, replacing both placeholders with that remote name and the branch your instructor provided. Include report excerpts without credentials or private account information.
4. **GitHub in your browser:** Open your fork, select the branch you pushed, and open `session4-report.md`. Check that the tables render and your evidence links open.

**Turn in:** The GitHub link to the rendered report on your submission branch.
