# Phonebook — QA Assignment

This repository contains my QA work for the Graph hiring assignment (`Q-Test.pdf`).
The application under test is a small Python **client/server phonebook**: the client
sends JSON command batches over ZeroMQ, the server executes them against a SQLite
database and returns a JSON result.

The goal of the assignment is **quality assurance**, not development: design test
scenarios and test cases, split them into manual and automated, automate the
deterministic ones in Python, and report the defects found. The application is
intentionally shipped with bugs — finding and documenting them is the deliverable.

## Repository structure

```
.
├── Q-Test.pdf                 # the original assignment
└── phon_book/
    ├── server.py, client.py   # application under test (left unmodified)
    ├── core/                  # business logic (auth, phonebook, models)
    ├── samples/               # example JSON command files
    ├── docs/                  # QA deliverables (see table below)
    └── tests/                 # automated pytest suite
```

## QA deliverables (`phon_book/docs/`)

| Document | Contents |
|---|---|
| `QA_SYSTEM_UNDERSTANDING.md` | How the system works, state model, expected vs observed behavior |
| `QA_RISK_CATALOG.md` / `.xlsx` | Risk catalog (21 risks) with severity, priority, validation status |
| `TEST_SCENARIOS.md` / `.xlsx` | High-level scenarios (42) grouped by feature area |
| `TEST_CASES.md` / `.xlsx` | Detailed, executable test cases (35) with status |
| `TEST_STRATEGY.md` | Manual vs automated vs exploratory split and the reasoning |
| `BUG_REGISTER.md` | Formal defect entries (22) mapped to failing test cases |
| `TEST_REPORT.md` | Execution summary and findings |
| `README_TESTING.md` | Step-by-step setup and execution guide |

Traceability runs `RISK-### → SCN-### → TC-### → BUG-###`.

## Running the application

The legacy dependencies require **Python 3.8**. A virtual environment is expected at
`phon_book/.venv`.

```bash
cd phon_book
python3.8 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Start the server in one terminal:

```bash
python server.py --port 9090 --ip 127.0.0.1
```

Send a command file from another terminal:

```bash
python client.py --port 9090 --ip 127.0.0.1 --file samples/commands.json
```

## Running the tests

From the `phon_book/` directory:

```bash
./.venv/bin/pytest -q tests
```

The suite is integration-style: each test launches the real server in an isolated
temporary workspace and talks to it over ZeroMQ with request timeouts.

### Interpreting the results

The tests assert the **expected** behavior from the assignment, not the current
(buggy) behavior. Against the shipped application the result is:

```
13 passed, 22 failed
```

The 13 passing tests cover features that already work (signup, signin, logout,
contact CRUD happy paths, search). **The 22 failures are intentional** — each one
documents a real defect and is recorded in `docs/BUG_REGISTER.md`. The application
code is deliberately left unchanged so the failures stay reproducible.

## Bug summary

The defects cluster into a few themes (full detail in `docs/BUG_REGISTER.md`):

- **Service resilience** — many invalid or duplicate inputs crash the server instead of returning a controlled error.
- **Requirement mismatches** — login is by username instead of email; duplicate/invalid emails are accepted.
- **Authorization** — phonebook operations run without sign-in.
- **Error contract** — failure responses are not consistently structured and can leak internal details.
- **Not-found / persistence** — searching, editing, or removing missing records is not handled gracefully.
