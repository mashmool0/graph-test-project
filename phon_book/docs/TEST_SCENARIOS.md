# Test Scenarios

## Purpose
This document defines the scenario structure, grouping model, and traceability rules for high-level QA coverage. The detailed scenario inventory is maintained in `TEST_SCENARIOS.xlsx`.

## Scope of This Document
- scenario template
- scenario grouping model
- traceability rules
- scenario-writing rules

## Scenario ID Convention
- Format: `SCN-###`

## Traceability Rule
- Every scenario should map to one or more `RISK-###` items.
- Every detailed test case should later map to one `SCN-###` item.

## Scenario Entry Template
Each scenario in the Excel file should contain these fields:
- Scenario ID
- Title
- Feature Area
- Related Risk IDs
- Purpose / Risk Covered
- Preconditions Summary
- Scenario Type
- Priority
- Execution Mode
- Notes / Ambiguity

## Scenario Writing Rules
- Scenarios are high-level coverage objectives, not step-by-step test cases.
- Scenarios should be short, clear, and directly traceable to one or more risks.
- Scenarios should describe what must be validated, not how to execute it in detail.
- Requirement ambiguity should remain visible in the notes field where needed.

## Scenario Groups
- Authentication
- Authorization and Access Control
- Contact Creation
- Contact Read and Search
- Contact Update and Delete
- Validation and Negative Behavior
- Response Contract and Error Handling
- Persistence and Repeatability
- Concurrency and Multi-User
- Operational and Environment

## Scenario Inventory
The full detail (related risks, purpose, preconditions, notes/ambiguity) is maintained in `TEST_SCENARIOS.xlsx`. The summary below mirrors that workbook so the inventory is reviewable directly here.

| Scenario ID | Title | Feature Area | Type | Priority | Execution Mode |
|---|---|---|---|---|---|
| SCN-001 | Register a new user with valid signup data | Authentication | Functional | High | Manual |
| SCN-002 | Authenticate a registered user with valid credentials | Authentication | Functional | High | Manual |
| SCN-003 | Validate whether login by email is supported as required | Authentication | Negative | High | Manual |
| SCN-004 | Reject duplicate username registration without server failure | Authentication | Negative | High | Mixed |
| SCN-005 | Reject duplicate email registration according to requirement | Authentication | Negative | High | Mixed |
| SCN-006 | Validate signup email format handling | Authentication | Negative | High | Mixed |
| SCN-007 | Handle wrong password login attempt without server failure | Authentication | Negative | High | Mixed |
| SCN-008 | Logout only the authenticated caller | Authentication | State Transition | High | Exploratory |
| SCN-009 | Block contact creation before authentication | Authorization and Access Control | Security | High | Mixed |
| SCN-010 | Block contact retrieval before authentication | Authorization and Access Control | Security | High | Mixed |
| SCN-011 | Block contact actions after logout | Authorization and Access Control | State Transition | High | Exploratory |
| SCN-012 | Verify contact ownership and user isolation between different accounts | Authorization and Access Control | Security | High | Exploratory |
| SCN-013 | Create a new contact with an initial phone number | Contact Creation | Functional | High | Manual |
| SCN-014 | Add a second phone number to an existing contact | Contact Creation | Functional | High | Manual |
| SCN-015 | Reject duplicate contact creation without crashing the server | Contact Creation | Negative | High | Mixed |
| SCN-016 | Reject duplicate phone number creation without crashing the server | Contact Creation | Negative | High | Mixed |
| SCN-017 | Handle add-phone-number request for a missing contact | Contact Creation | Negative | High | Mixed |
| SCN-018 | Return all contacts after data exists | Contact Read and Search | Functional | Medium | Manual |
| SCN-019 | Search for an existing contact by name | Contact Read and Search | Functional | Medium | Manual |
| SCN-020 | Search for an existing contact by phone number | Contact Read and Search | Functional | Medium | Manual |
| SCN-021 | Handle not-found search requests gracefully | Contact Read and Search | Negative | High | Mixed |
| SCN-022 | Edit only the contact name | Contact Update and Delete | Functional | Medium | Manual |
| SCN-023 | Edit only the phone number | Contact Update and Delete | Functional | Medium | Manual |
| SCN-024 | Edit both contact name and phone number together | Contact Update and Delete | Functional | Medium | Manual |
| SCN-025 | Delete an existing contact | Contact Update and Delete | Functional | Medium | Manual |
| SCN-026 | Handle update or delete operations for non-existing contacts gracefully | Contact Update and Delete | Negative | High | Mixed |
| SCN-027 | Handle missing required authentication fields safely | Validation and Negative Behavior | Negative | High | Mixed |
| SCN-028 | Handle missing required contact-operation fields safely | Validation and Negative Behavior | Negative | High | Mixed |
| SCN-029 | Handle invalid data types safely | Validation and Negative Behavior | Negative | High | Mixed |
| SCN-030 | Handle malformed JSON input at the client boundary | Validation and Negative Behavior | Negative | Medium | Manual |
| SCN-031 | Handle missing command_name or parameters safely | Validation and Negative Behavior | Negative | High | Mixed |
| SCN-032 | Return the documented success response contract | Response Contract and Error Handling | Contract | High | Automated Candidate |
| SCN-033 | Return controlled structured errors for business-rule failures | Response Contract and Error Handling | Contract | High | Mixed |
| SCN-034 | Keep the server alive after invalid requests | Response Contract and Error Handling | Operational | High | Mixed |
| SCN-035 | Avoid leaking internal tracebacks and SQL details in error paths | Response Contract and Error Handling | Security | High | Mixed |
| SCN-036 | Initialize phonebook schema correctly before first contact operation | Persistence and Repeatability | Data Consistency | High | Mixed |
| SCN-037 | Keep test behavior repeatable across runs with persistent database state | Persistence and Repeatability | Operational | High | Manual |
| SCN-038 | Observe batch partial-success behavior when a later command fails | Persistence and Repeatability | State Transition | Medium | Exploratory |
| SCN-039 | Observe concurrent signups or duplicate creations under overlapping requests | Concurrency and Multi-User | Concurrency | Medium | Exploratory |
| SCN-040 | Observe shared session-state behavior under overlapping users | Concurrency and Multi-User | Concurrency | Medium | Exploratory |
| SCN-041 | Verify environment compatibility and dependency setup | Operational and Environment | Operational | Medium | Manual |
| SCN-042 | Verify crash recovery workflow for manual test execution | Operational and Environment | Operational | Medium | Manual |

## Notes for Later Phases
- The detailed scenario inventory is maintained in `TEST_SCENARIOS.xlsx`.
- `TEST_CASES.md` converts the high-priority scenarios into executable manual and automated cases.
