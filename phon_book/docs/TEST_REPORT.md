# Test Report

## Project Overview
This report summarizes the executed QA work for the `phon_book` client/server project.

The system under test is a Python-based command-driven phonebook service using:
- ZeroMQ for client/server communication
- JSON command payloads
- SQLite persistence
- authentication and phonebook operations

The test suite was written against expected behavior from `TEST_CASES.xlsx`, not against the current broken behavior. Failing tests therefore represent requirement or quality gaps, not invalid assertions.

## Scope of Executed Testing
Executed scope includes:
- system-understanding review
- risk validation for high-priority items
- Wave 1 pytest implementation and execution
- Wave 2 pytest implementation and execution
- repeatability coverage for persistent database behavior

Executed automated modules:
- `tests/test_auth.py`
- `tests/test_validation.py`
- `tests/test_authorization.py`
- `tests/test_contract.py`
- `tests/test_phonebook_core.py`
- `tests/test_repeatability.py`

## Test Environment
Environment used during execution:
- OS: Linux-like local development environment
- Python: `3.8.20`
- Virtual environment: `phon_book/.venv`
- Test runner: `pytest 8.3.5`
- Workbook tooling: `openpyxl 3.1.5`

Runtime characteristics that affected testing:
- persistent SQLite file `sab.db`
- server process terminates on several invalid and not-found flows
- tests run in isolated temporary workspaces to avoid polluting the primary database
- default application endpoint is `127.0.0.1:9090`

## Testing Approach
Testing followed these principles:
- expected-behavior verification, not bug-preserving assertions
- risk-first ordering
- deterministic integration testing first
- isolated workspace execution for destructive checks
- requirement mismatch treated as a valid failure type
- explicit prerequisite setup for phonebook success cases

## Execution Summary
### Automated execution completed
1. `test_auth.py`
2. `test_validation.py`
3. `test_authorization.py`
4. `test_contract.py`
5. `test_phonebook_core.py`
6. `test_repeatability.py`

### Workbook execution coverage
All documented cases in `TEST_CASES.xlsx` now have statuses recorded.

## Results Summary
### Full suite result
Command executed:
```bash
./.venv/bin/pytest -q tests
```

Suite result:
- Pass: 13
- Fail: 22
- Total: 35

### Passing cases
- `TC-009`
- `TC-013`
- `TC-018`
- `TC-019`
- `TC-021`
- `TC-022`
- `TC-023`
- `TC-024`
- `TC-025`
- `TC-026`
- `TC-027`
- `TC-028`
- `TC-029`

### Failing cases
- `TC-001`
- `TC-002`
- `TC-003`
- `TC-004`
- `TC-005`
- `TC-006`
- `TC-007`
- `TC-008`
- `TC-010`
- `TC-011`
- `TC-012`
- `TC-014`
- `TC-015`
- `TC-016`
- `TC-017`
- `TC-020`
- `TC-030`
- `TC-031`
- `TC-032`
- `TC-033`
- `TC-034`
- `TC-035`

## Consolidated Findings
### 1. Authentication requirement mismatch
Expected behavior:
- users should be able to log in by email and password

Observed behavior:
- implementation authenticates by username and password
- email-based login fails and stops the server path

Related cases:
- `TC-001`

### 2. Registration validation is incomplete and unstable
Expected behavior:
- duplicate email should be rejected
- duplicate username should be rejected cleanly
- invalid email should be rejected
- malformed signup payloads should return controlled validation results

Observed behavior:
- duplicate email is accepted
- duplicate username terminates the server through raw DB integrity handling
- invalid email is accepted
- missing username and non-string password terminate the server

Related cases:
- `TC-002`
- `TC-003`
- `TC-004`
- `TC-005`
- `TC-035`

### 3. Wrong-password handling is not controlled
Expected behavior:
- wrong-password login should return a controlled rejection and keep the server alive

Observed behavior:
- wrong-password path does not preserve server stability

Related cases:
- `TC-020`

### 4. Authorization is not enforced for phonebook operations
Expected behavior:
- contact creation and contact listing should require prior authentication

Observed behavior:
- phonebook operations can be executed without `sign_in`

Related cases:
- `TC-007`
- `TC-008`

### 5. Validation and error resilience remain weak
Expected behavior:
- malformed phonebook requests and invalid auth requests should return controlled structured results
- server should continue running

Observed behavior:
- missing phone number still stops the server
- invalid signup request still stops the server
- duplicate-username failure still stops the server instead of returning a controlled structured error

Related cases:
- `TC-006`
- `TC-010`
- `TC-011`

### 6. Error output safety is poor
Expected behavior:
- failure output should not leak internal DB or traceback details

Observed behavior:
- raw DB/model/internal details are still exposed on failure paths

Related cases:
- `TC-012`

### 7. Happy-path phonebook CRUD works in the authenticated flow
Observed passing behavior:
- first phonebook operation after auth succeeds on a clean database
- creating a contact succeeds
- adding a second phone number succeeds
- get-all, search by name, and search by number succeed
- edit name, edit phone, and edit both succeed

Related passing cases:
- `TC-013`
- `TC-022`
- `TC-023`
- `TC-024`
- `TC-025`
- `TC-026`
- `TC-027`
- `TC-028`
- `TC-029`

### 8. Controlled failure handling for phonebook negative paths is poor
Expected behavior:
- duplicate contact and duplicate phone number should be rejected without server termination
- adding a number to a missing contact should return a controlled not-found result
- delete/search/edit of non-existing contacts should return predictable controlled results
- deleting an existing contact should allow clean verification of removal

Observed behavior:
- duplicate contact and duplicate phone number still terminate the server
- add-phone-number for a missing contact still terminates the server
- delete/search/edit of non-existing contacts are uncontrolled or misleading
- deleting an existing contact does not stay controlled through the verification flow

Related cases:
- `TC-014`
- `TC-015`
- `TC-016`
- `TC-030`
- `TC-031`
- `TC-032`
- `TC-033`
- `TC-034`

### 9. Repeat-run behavior is not handled cleanly
Expected behavior:
- repeated execution against persistent DB state should produce predictable duplicate handling without stopping the server

Observed behavior:
- duplicate repeat-run signup path still stops the server

Related cases:
- `TC-017`

## Root-Cause Areas
The failing cases cluster around a few technical problem areas:
- `core/auth.py`: login identifier mismatch, weak input validation, unstable failure handling
- `core/phone_book.py`: missing authorization checks, unstable duplicate/not-found behavior, misleading delete semantics
- `core/factory_command.py` and command-dispatch flow: inconsistent error handling contract
- `server.py`: server process exits on unhandled exceptions instead of preserving service availability
- `core/models.py` / DB constraints: raw integrity errors leak through instead of being translated into controlled business errors

## Residual Risks
Important areas still not deeply exercised:
- concurrent multi-user overlap
- batch partial-success/partial-failure behavior
- logout ownership weakness across active users
- longer operational recovery workflows
- broader malformed JSON file handling from CLI perspective

## QA Assessment
Current assessment:
- authenticated happy-path CRUD coverage is partially healthy
- negative-path resilience is weak
- authorization behavior does not match the stated flow
- error handling and response-contract quality are poor
- persistent-state duplicate handling is not production-safe

The project currently behaves like a partially working happy-path prototype with weak defensive behavior around invalid, duplicate, and not-found requests.
