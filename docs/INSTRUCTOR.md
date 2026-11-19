# Instructor setup

1. Publish the contents of Session4_AI_Assisted_Vulnerability_Hunting/starter/ as the standalone public classroom repository used for CodeQL. Record the URL and commit. Enable GitHub Actions where needed. For the full Codespaces lab, use this workshop folder with its .devcontainer and starter/ directory.
2. Run Claude Code /security-review on that commit and save its report for Exercise 5 if needed. For Exercise 6, have a Claude Enterprise owner enable Claude Security and grant the Claude GitHub App access to the published starter repository. Give students premium seats and permission to create projects, with usage billing enabled. Before class, give them the Enterprise workspace name, the exact GitHub repository URL, branch name and commit hash. Have students connect their GitHub accounts to Claude so they can select that repository. The first scan may take several minutes or hours, so allow time for it before Exercise 8. Students generate their own scan results during the exercise. Check that the terminal report covers both example files. If the slash command only reviews a branch diff, prepare a review branch that introduces the two example files relative to its base, then use that same head commit for all three reviews. Save Gemini scanner and source outputs if students will use offline copies. Label real tool outputs with the model, tool version when available, and commit.
3. Reveal the solution scoring key after students record their initial verdicts. Compare the reviewed examples with the repaired implementations and run the file-operation tests.
4. For discussion, use the misleading repository excerpt from Exercise 9 and have students contrast it with a contaminated benchmark or a model with unknown training/fine-tuning provenance.

The original Session4_File_Handling_Code_Defense folder remains the reference for its slide deck, threat model, verification notes, and original implementation. The new workshop carries over its import/export and attachment features, static check scripts, and two source review cases. Its live demonstrations teach normal behavior, defensive checks and repair verification.
The instructor's local checks and interpretation are in [reference results](../solution/REFERENCE_RESULTS.md).

For the original application-wide checks, run python scripts/run_sast.py and
python -m scanner.scan_app from either workshop copy. The ten exercises use
the smaller two-file comparison with --examples. Keep the published commit
constant across CodeQL, Claude Code /security-review, Claude Security and the
Gemini source review. Filter scores to review_examples/file_imports.py and
review_examples/attachments.py.

## Service setup references

- [GitHub CodeQL default setup](https://docs.github.com/en/code-security/how-tos/find-and-fix-code-vulnerabilities/configure-code-scanning/configure-code-scanning)
- [Claude Code /security-review](https://support.anthropic.com/en/articles/11932705-automated-security-reviews-in-claude-code/)
- [Claude Security](https://www.anthropic.com/research/glasswing-initial-update)
