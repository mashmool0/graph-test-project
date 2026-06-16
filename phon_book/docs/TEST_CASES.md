# Test Cases

## Purpose
This document defines the test-case structure, writing rules, and traceability model for executable QA coverage. The detailed test-case inventory is maintained in `TEST_CASES.xlsx`.

## Scope of This Document
- test-case template
- writing rules
- status values
- traceability rules

## Test Case ID Convention
- Format: `TC-###`

## Traceability Rule
- Every test case should map to one `SCN-###` item.
- Test cases may also reference related `RISK-###` items through the linked scenario.

## Test Case Entry Template
Each test case in the Excel file should contain these fields:
- Test Case ID
- Related Scenario ID
- Title
- Objective
- Preconditions
- Test Data
- Steps
- Expected Result
- Actual Result
- Status
- Type
- Priority
- Execution Mode
- Notes / Evidence

## Allowed Status Values
- Not Run
- Pass
- Fail
- Blocked

## Test Case Writing Rules
- Test cases must be executable and deterministic.
- Test cases must contain exact preconditions and exact test data where possible.
- Test cases must separate expected result from actual result.
- Test cases should be concise but precise enough for another tester to execute without guesswork.
- Requirement ambiguity should remain visible in the notes field when necessary.

## Test Case Inventory
The full detail (objective, preconditions, test data, steps, expected/actual result, evidence) is maintained in `TEST_CASES.xlsx`. The summary below mirrors that workbook so the inventory is reviewable directly here.

Execution snapshot: 35 cases total — 13 Pass, 22 Fail. Failing cases are requirement-based and are mapped to defects in `BUG_REGISTER.md`.

| Test Case ID | Title | Type | Priority | Execution Mode | Status |
|---|---|---|---|---|---|
| TC-001 | Validate login by email requirement mismatch | Negative | High | Manual | Fail |
| TC-002 | Reject duplicate email registration | Negative | High | Automated Candidate | Fail |
| TC-003 | Reject duplicate username without crashing server | Negative | High | Automated Candidate | Fail |
| TC-004 | Handle missing signup username safely | Negative | High | Automated Candidate | Fail |
| TC-005 | Handle non-string password safely during signup | Negative | High | Automated Candidate | Fail |
| TC-006 | Handle missing phone number safely on contact creation | Negative | High | Automated Candidate | Fail |
| TC-007 | Block contact creation before authentication | Security | High | Automated Candidate | Fail |
| TC-008 | Block contact list retrieval before authentication | Security | High | Automated Candidate | Fail |
| TC-009 | Return documented success response structure | Contract | High | Automated Candidate | Pass |
| TC-010 | Return structured error for duplicate username failure | Contract | High | Automated Candidate | Fail |
| TC-011 | Keep server alive after invalid auth request | Operational | High | Automated Candidate | Fail |
| TC-012 | Avoid leaking traceback and SQL details in error replies | Security | High | Manual | Fail |
| TC-013 | Initialize phonebook schema before first contact operation | Data Consistency | High | Automated Candidate | Pass |
| TC-014 | Reject duplicate contact name without crashing server | Negative | High | Automated Candidate | Fail |
| TC-015 | Reject duplicate phone number without crashing server | Negative | High | Automated Candidate | Fail |
| TC-016 | Handle add-phone-number for non-existing contact gracefully | Negative | High | Automated Candidate | Fail |
| TC-017 | Observe repeat-run behavior with persistent database state | Operational | High | Manual | Fail |
| TC-018 | Register a new user with valid signup data | Functional | High | Automated Candidate | Pass |
| TC-019 | Authenticate a registered user with valid credentials | Functional | High | Automated Candidate | Pass |
| TC-020 | Handle wrong password login attempt | Negative | High | Automated Candidate | Fail |
| TC-021 | Logout the authenticated user successfully | State Transition | Medium | Automated Candidate | Pass |
| TC-022 | Create a new contact with initial phone number | Functional | High | Automated Candidate | Pass |
| TC-023 | Add a second phone number to an existing contact | Functional | High | Automated Candidate | Pass |
| TC-024 | Return all contacts after data exists | Functional | Medium | Automated Candidate | Pass |
| TC-025 | Search for an existing contact by name | Functional | Medium | Automated Candidate | Pass |
| TC-026 | Search for an existing contact by phone number | Functional | Medium | Automated Candidate | Pass |
| TC-027 | Edit only the contact name | Functional | Medium | Automated Candidate | Pass |
| TC-028 | Edit only the phone number | Functional | Medium | Automated Candidate | Pass |
| TC-029 | Edit both contact name and phone number together | Functional | Medium | Automated Candidate | Pass |
| TC-030 | Delete an existing contact | Functional | Medium | Automated Candidate | Fail |
| TC-031 | Search for a non-existing contact by name | Negative | High | Automated Candidate | Fail |
| TC-032 | Search for a non-existing contact by phone number | Negative | High | Automated Candidate | Fail |
| TC-033 | Delete a non-existing contact | Negative | High | Automated Candidate | Fail |
| TC-034 | Edit a non-existing contact | Negative | High | Automated Candidate | Fail |
| TC-035 | Reject invalid email format during signup | Negative | High | Automated Candidate | Fail |

## Notes for Later Phases
- The workbook now covers authentication, contact CRUD, search, validation, contract, and persistence cases.
- Remaining extensions are concurrency and multi-user isolation, which are tracked as exploratory scenarios.
