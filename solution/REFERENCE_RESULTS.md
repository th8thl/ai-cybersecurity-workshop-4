# Reference interpretation

On the starter review examples, Bandit and Semgrep each reported two alerts in the Windows verification run. Count distinct weaknesses after checking the source. Bandit produced two warnings for the importer (B403 and B301). Semgrep flagged both the importer and the attachment path. Both scanners reported zero alerts on the repaired examples.

In the NeMo comparison, both excerpts passed when NeMo was disabled. When enabled, the valid excerpt passed and the misleading excerpt was blocked. That comparison measures the behavior of the configured retrieval rule on two examples.

## File-handling checks

From either copy, run python manage.py test tests.test_file_uploads. The suite covers JSON import and export, upload and authenticated download, file limits, invalid input, login and CSRF. Run python scripts/run_sast.py for the inherited full-application scan or add --examples for the classroom code comparison.

Gemini, the two Claude products, and GitHub CodeQL require their respective service access and separate scans. Record the Git commit and tool configuration when capturing their outputs.
