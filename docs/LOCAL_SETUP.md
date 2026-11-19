# Local setup

The commands below use Python 3.12. If you installed 3.13, replace the version in the environment creation command. Install Ollama, start it, and pull the workshop models:

    ollama pull qwen3:0.6b-q4_K_M
    ollama pull embeddinggemma:300m

## Before class

| Exercises | Install or arrange access | How to check |
|---|---|---|
| 1, 2, 9 | Git, VS Code or a text editor, a browser, Python 3.12 or 3.13, and Ollama. The requirements file installs Django, Bandit, Semgrep and NeMo. No paid license is required. | Run the local setup and smoke test below. |
| 3, 8 | Gemini API key and the classroom model ID. Use the free tier if that model and quota allow it. Otherwise enable billing on the API project. | Set `GEMINI_API_KEY` and `GEMINI_MODEL` in the local `starter/.env`. Exercise 3 makes the first API request. |
| 4, 10 | Personal GitHub account and the URL of your template-created workshop repository. You need admin access to enable CodeQL on your public workshop repository and write access to push your report. | Confirm the repository belongs to your GitHub account. Public-repo CodeQL does not require a paid GitHub Code Security license. |
| 5 | Claude Code CLI and a Claude account with Claude Code access or a billed Anthropic Console account. | Run `claude --version`, then launch `claude` and sign in. If using the course's saved report, skip the CLI setup for this exercise. |
| 6 | Claude Code extension and official Claude Security plugin in the Codespaces workspace. | Use Claude Code account access with available usage or API billing. Install with /plugin install claude-security@claude-plugins-official, then /reload-plugins. Confirm the plugin command appears in the Claude Code panel. |
| 7 | Desktop Google Chrome, the Claude in Chrome extension, Claude Code CLI, and an eligible paid Claude plan with Chrome access enabled. | Sign in to both with the same account and workspace. Launch `claude --chrome`, then enter `/chrome` to check the connection. [Anthropic setup](https://code.claude.com/docs/en/chrome) |

See [the exercises](EXERCISES.md) for the account and license details at each step.

## macOS Terminal

From the workshop folder:

    cd starter
    python3.12 -m venv .venv
    source .venv/bin/activate
    python -m pip install -r requirements.txt

## Windows PowerShell

From the workshop folder, run:

```powershell
Set-Location starter
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

After activation, the prompt should begin with `(.venv)`. Confirm the Python path:

```powershell
python -c "import sys; print(sys.executable)"
```

The printed path should end in `starter\.venv\Scripts\python.exe`.

If PowerShell blocks Activate.ps1 with an execution-policy error, enable scripts for this terminal session and try activation again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

In every new PowerShell terminal, change to the workshop's `starter` folder and run `.\.venv\Scripts\Activate.ps1` before the Python commands below.

## Configure and smoke-test

From starter, with the environment selected:

    python scripts/configure.py
    python manage.py migrate
    python manage.py seed_demo
    python scripts/run_sast.py --examples
    python manage.py runserver

Open http://127.0.0.1:8000/, sign in using the credentials printed by seed_demo, and check Tickets. Confirm both scanner JSON files are in results/examples/current. For Gemini exercises, set GEMINI_API_KEY and GEMINI_MODEL in starter/.env.

