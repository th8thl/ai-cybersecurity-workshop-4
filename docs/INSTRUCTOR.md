# Instructor setup

1. Make https://github.com/th8thl/ai-cybersecurity-workshop-4 a template repository. Students create their own public repository from this template before class and open their Codespace from it. Use that same repository for CodeQL and Claude Security. Scope Claude Security to starter/review_examples and score CodeQL alerts for the two files in that folder.
2. Verify the Claude Code extension and official Claude Security plugin are available to students. Exercise 5 uses a direct request to review the student-created SQL example; Exercise 6 generates a scan through the plugin in the same VS Code panel. Check available account usage and organization plugin permissions before class. Keep the source scope on the two starter/review_examples files for the comparison.
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

