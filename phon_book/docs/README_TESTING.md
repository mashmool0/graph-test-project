# Testing README

## Purpose
This document provides the practical instructions needed to prepare the environment, run the project manually, execute validation flows, and later run automated tests.

It is intended to support both:
- manual QA execution
- future automated regression execution

## Environment Requirements
Recommended environment for this project:
- Linux environment similar to the current project machine
- Python `3.8.20`
- working virtual environment in `phon_book/.venv`
- project dependencies installed from `requirements.txt`

Important notes:
- the legacy dependency set in this project is compatible with the current setup only when the virtual environment uses Python `3.8.x`
- newer Python versions caused dependency and compatibility failures during validation

## Project Location
Project root used in this QA work:
- `/home/mashmool/Programming/Projects/graph/phon_book`

All commands below assume execution from that directory unless stated otherwise.

## Setup Instructions
Open a terminal and move into the project:

```bash
cd /home/mashmool/Programming/Projects/graph/phon_book
```

Activate the project virtual environment:

```bash
source .venv/bin/activate
```

Verify Python version:

```bash
python --version
```

Expected version:

```bash
Python 3.8.20
```

## Installing Dependencies
Install the project requirements inside the active virtual environment:

```bash
pip install -r requirements.txt
```

If the local shell environment injects SOCKS proxy variables and `pip` fails with SOCKS-related errors, use:

```bash
env -u ALL_PROXY -u all_proxy pip install -r requirements.txt
```

## Running the Server
Start the server in one terminal:

```bash
python server.py --port 7878 --ip 127.0.0.1
```

Expected startup behavior:
- the server starts and waits for a request
- it prints readiness text to the console

Typical ready message:

```text
Server is ready to receive data...
```

## Running the Client
In another terminal, activate the same virtual environment and run the client:

```bash
cd /home/mashmool/Programming/Projects/graph/phon_book
source .venv/bin/activate
python client.py --port 7878 --ip 127.0.0.1 --file samples/commands.json
```

This sends the JSON command file to the server and prints the server response.

## Running Manual Test Files
Additional manual sample files were added under `samples/` for QA work.

Examples:

```bash
python client.py --port 7878 --ip 127.0.0.1 --file samples/test_auth.json
python client.py --port 7878 --ip 127.0.0.1 --file samples/test_add_phone_user.json
python client.py --port 7878 --ip 127.0.0.1 --file samples/test_add_phone_number.json
python client.py --port 7878 --ip 127.0.0.1 --file samples/test_edit_phone_user.json
python client.py --port 7878 --ip 127.0.0.1 --file samples/test_search_and_remove.json
```

## Current Known Manual-Testing Risks
Manual testers should be aware of these validated behaviors:
- some invalid requests terminate the server
- duplicate signup attempts can terminate the server
- some missing-field cases terminate the server
- some failures return raw DB or exception text
- the database persists across runs and can affect repeatability
- phonebook commands on a clean DB may fail if schema creation has not been triggered yet

Because of this, manual execution should be done carefully and with explicit state control.

## Safe Manual Validation Workflow
Recommended manual workflow:

1. Activate `.venv`
2. Start the server
3. Execute one test input file or one targeted command batch
4. Observe client output
5. Observe whether the server stays alive
6. Restart the server if the previous request caused a crash
7. Reset or control DB state before the next deterministic test

## Database State Management
The project uses a persistent SQLite file:

```text
sab.db
```

This file is not automatically reset between runs.

Implications:
- repeated runs can fail because existing usernames or contacts remain in the DB
- one test can influence the next if the DB is not cleaned or isolated

### To reset local DB state
If you want a fresh local run:

```bash
rm sab.db
```

Then restart the server.

Important:
- only do this when you intentionally want a clean state
- this removes existing local test data

### Safer validation approach
For destructive or repeatability-sensitive checks, use:
- a temporary project copy
- or a reset procedure before the run

This was the approach used during the validated QA checks.

## Malformed JSON Testing
Malformed JSON is handled on the client side before transmission.

Example of running a malformed file test:

```bash
python client.py --port 7878 --ip 127.0.0.1 --file path/to/bad.json
```

Observed current behavior:
- client prints an invalid JSON message
- request is not processed normally by the server

## Interpreting Results
When observing results, classify the outcome using the following logic.

### Pass
- behavior matches the expected result for that test case
- server stability and output contract are acceptable for that case

### Fail
- behavior contradicts the expected result
- requirement mismatch is confirmed
- crash, wrong output, raw traceback, or wrong data behavior occurs

### Blocked
- the test could not proceed because setup or a prior system state prevented execution
- example: server already dead, environment not ready, DB state unknown

### Not Run
- case has not yet been executed

## Evidence to Capture During Manual Testing
For each executed case, capture:
- command file or payload used
- client-visible output
- whether the server remained alive
- server console output if relevant
- whether DB state was clean or reused
- whether the result indicates a requirement mismatch, defect, or ambiguity

This evidence is especially important for:
- crash cases
- response contract failures
- duplicate-data failures
- authorization and ownership questions

## Automated Test Execution
Automated tests are planned for the `tests/` directory but are not yet the main completed deliverable at this point.

The current direction is:
- start with Wave 1 deterministic regression candidates
- use isolated DB state
- use timeouts around client/server communication
- focus first on high-risk validated behaviors

Expected future execution pattern:

```bash
pytest
```

Or selectively:

```bash
pytest tests/test_auth.py
pytest tests/test_validation.py
```

## Recommended First Automation Targets
The strongest first automation targets are:
- duplicate username signup
- duplicate email signup
- invalid email handling
- missing required signup field
- invalid password type
- unauthenticated contact action
- success and error response contract checks
- phonebook schema initialization defect
- duplicate contact and duplicate phone number handling
- add-phone-number for non-existing contact

## Troubleshooting Notes
### Problem: `pip install -r requirements.txt` fails
Check:
- Python version is `3.8.x`
- `.venv` is active
- proxy environment variables are not interfering with pip

### Problem: server crashes after one bad request
This is a known current application behavior for several negative paths.

Action:
- restart the server
- record the request payload and crash output as evidence

### Problem: duplicate data errors appear unexpectedly
Likely cause:
- old data remains in `sab.db`

Action:
- verify DB state
- reset `sab.db` if a clean run is required

### Problem: first phonebook command fails on clean DB
Likely cause:
- schema initialization ordering defect

Action:
- record the failure as evidence
- note whether an auth command had run before the phonebook command

## Current Documentation References
Related QA artifacts in `docs/`:
- `QA_SYSTEM_UNDERSTANDING.md`
- `QA_RISK_CATALOG.md`
- `QA_RISK_CATALOG.xlsx`
- `TEST_SCENARIOS.md`
- `TEST_SCENARIOS.xlsx`
- `TEST_CASES.md`
- `TEST_CASES.xlsx`
- `TEST_STRATEGY.md`

## Recommended Immediate Next Steps
From a QA workflow perspective, the next steps after using this guide are:
1. execute or review Wave 1 test cases
2. implement Wave 1 automated regression tests
3. record confirmed outcomes in `TEST_REPORT.md`
4. extend coverage into Wave 3 state/concurrency/operational cases
