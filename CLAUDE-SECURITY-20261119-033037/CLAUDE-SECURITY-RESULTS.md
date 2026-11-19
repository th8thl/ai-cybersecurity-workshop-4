# Claude Security results

This was a scoped scan of `starter/tickets/local_adapter.py` in this repository at revision `5bc04aa`, run on 2026-11-19 (UTC) at `medium` effort. The working tree held uncommitted changes or untracked files when it was scanned. The scan found **1 finding: 1 HIGH** (SQL injection).

## Coverage

The scan covered one tracked file, `starter/tickets/local_adapter.py`, as requested. Nothing else in the repository was audited. Researchers and verifiers did read nearby code (views, forms, schema validation, the ticket service) to trace where the input comes from and what the impact is, but they reported findings only for this file. Because the scope was this small (1 file), the scan used the proportionate single-researcher shape instead of the full component matrix. That is a fast, targeted pass, still checked by the verification panel, and not an exhaustive read. One researcher was dispatched, looked for every kind of vulnerability, and returned. The panel completed in 1 verification run, and no candidate went unverified.

## Findings

### F1 — SQL injection in create_ticket: user-supplied ticket title is put into a raw INSERT with an f-string (HIGH, confidence high)

**Impact.** Any authenticated user can read the whole database through their own ticket title: password hashes, Django session keys (which allows hijacking an admin's session), and other users' tickets and data. They can also insert ticket rows owned by any other user with any status.

**Where.** `starter/tickets/local_adapter.py:15` (query built), executed at `:18` in `dispatch`. CWE-89.

**What.** The ticket `title` comes from the user through the web form (`tickets/views.py` `ticket_create` and `ticket_import`), the MCP `create_ticket` tool or the chatbot. The code puts it between single quotes in a raw SQL string with an f-string and runs it with `cursor.execute`. Only `owner_id` is bound as a parameter. Upstream validation (`TicketForm`, `validate_proposal`) only enforces a non-blank string of 1–120 characters, so quotes and SQL syntax reach the query unchanged.

**Exploit scenario.** A logged-in user submits `POST /tickets/new/` with the title `x'||(SELECT session_key FROM django_session LIMIT 1)||'`. The statement becomes `VALUES (?, 'x'||(SELECT ...)||'', 'open')`, so SQLite runs the subquery and saves its result as the attacker's ticket title. `dispatch` returns that title and the ticket detail page shows it. Changing `LIMIT`/`OFFSET`, or selecting `password FROM auth_user WHERE is_superuser=1`, reads other rows one at a time. A title like `a','open'),(1,'pwn` inserts extra rows owned by any user ID. sqlite3 rejects stacked statements, but subqueries and extra `VALUES` tuples inside the single INSERT are enough.

**Preconditions.**
- The attacker has a valid low-privilege account (accounts are login-only, with no self-registration), or can reach the MCP `create_ticket` tool or the chatbot, which pass the title into the same path.
- The payload fits within the 120-character title limit. The example payloads do.

**Fix.** Never build SQL from request data. Restore the ORM call in the commented-out lines (`Ticket.objects.create(owner=actor, title=arguments["title"])`), or bind the title as a parameter: `cursor.execute("INSERT INTO tickets_ticket (owner_id, title, status) VALUES (%s, %s, 'open')", [actor.pk, title])`.

**Verification.** 3/3 lens verifiers confirmed (reachability, impact, defenses). Severity was kept at HIGH.

## What was verified

One researcher read the scoped file and looked for every kind of vulnerability. Then a panel of three independent verifiers challenged each candidate, one checking reachability, one impact and one defenses. F1 was confirmed unanimously, 3 of 3. The verification status is the one stamped on this report by the renderer. All findings come from reading the code: nothing in this scan executed the repository's code, ran tests or fired an exploit.
