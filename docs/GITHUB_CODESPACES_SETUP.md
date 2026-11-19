# GitHub Codespaces setup

Publish this workshop folder as the Codespaces repository root. Its .devcontainer starts the workshop environment. The instructor also supplies a public starter-only repository for the CodeQL exercise.

## Before opening the Codespace

- Use a GitHub account with Codespaces allowance or billing. Get the workshop repository URL for Codespaces and the separate public starter repository URL for your own CodeQL fork.
- Use the [software and account checklist](LOCAL_SETUP.md#before-class) for Gemini, Claude Code, Claude Security, and Claude in Chrome. Codespaces setup installs the Python packages and Ollama. Sign in to the external services separately.
- For Exercise 7, open the private forwarded portal URL in desktop Chrome and run Claude Code locally on the same computer as Chrome. Use the Codespaces terminal for Django commands, including `python manage.py check --deploy`.

1. Open the workshop repository in Codespaces and wait for setup. It installs requirements and Ollama, migrates Django, and creates demo accounts. Keep port 8000 private.
2. Open a terminal at the repository root and run:

    cd starter
    source .venv/bin/activate
    python manage.py seed_demo --show-passwords
    python manage.py runserver 0.0.0.0:8000

3. Open port 8000, log in as a demo user, and check Tickets.
4. In a second terminal, switch to starter, activate the same environment, and run python scripts/run_sast.py --examples. Confirm both JSON files exist under results/examples/current.
