# QA Planning and Documentation Plan for `phon_book`

## Summary
Build the QA work in ordered phases so the project ends with a professional documentation set plus a clear path to manual and automated coverage. Use both sources of truth throughout: the assignment expectations and the actual code/runtime behavior. Place all deliverables under a `docs/` folder.

## Phase 1 — Create the documentation skeleton
Goal: establish a stable structure before writing content.

Steps:
1. Create `docs/` as the root documentation folder for QA deliverables.
2. Create these planned files:
   - `docs/QA_SYSTEM_UNDERSTANDING.md`
   - `docs/QA_RISK_CATALOG.md`
   - `docs/TEST_SCENARIOS.md`
   - `docs/TEST_CASES.md`
   - `docs/TEST_STRATEGY.md`
   - `docs/TEST_REPORT.md`
   - `docs/README_TESTING.md`
3. Keep all docs cross-referenced so scenarios link to cases and bugs link back to scenarios/cases.
4. Use stable IDs everywhere:
   - Risks: `RISK-###`
   - Scenarios: `SCN-###`
   - Test cases: `TC-###`
   - Bugs: `BUG-###`

## Phase 2 — Document the system and its truth sources
Goal: capture what the system is and where ambiguity exists.

Steps:
1. Write the system overview:
   - client/server shape
   - JSON command/request model
   - ZMQ transport flow
   - command dispatch flow
   - SQLite persistence
   - auth state handling
2. Document the main components:
   - `client.py`
   - `server.py`
   - `core/factory_command.py`
   - `core/auth.py`
   - `core/phone_book.py`
   - `core/models.py`
3. Document the supported commands and expected parameters/results.
4. Add a section called `Expected vs Observed Behavior`.
5. Record requirement ambiguities and open questions as explicit items, not hidden in prose.

## Phase 3 — Build the risk catalog
Goal: enumerate all likely failure areas before designing tests.

Steps:
1. Create risk categories:
   - Authentication
   - Session/state
   - Contact creation
   - Contact update/delete
   - Search/read behavior
   - Validation/input handling
   - Response/contract consistency
   - Persistence/database behavior
   - Crash/error handling
   - CLI/environment/runtime behavior
2. For each risk, document:
   - ID
   - description
   - why it matters
   - likely failure mode
   - severity/priority
   - expected source of evidence
3. Mark each risk as one of:
   - requirement-driven
   - code-observed
   - mismatch between requirement and code
4. Explicitly include known high-value risks:
   - login not enforced for phonebook actions
   - duplicate email behavior unclear vs implementation
   - duplicate usernames/phone numbers
   - malformed JSON handling
   - missing parameter crashes
   - DB state leaking between runs
   - response shape inconsistency
   - logout not protecting later actions
   - one batch request mixing valid and invalid commands

## Phase 4 — Create test scenario inventory
Goal: define high-level coverage by feature and risk.

Steps:
1. Group scenarios by feature area:
   - Authentication
   - Contact creation
   - Contact read/search
   - Contact update/delete
   - Validation/negative behavior
   - State/security behavior
   - Contract/response behavior
   - Persistence/repeatability behavior
   - Manual operational behavior
2. For each scenario include:
   - Scenario ID
   - title
   - purpose/risk
   - precondition summary
   - priority
   - type
   - baseline truth source:
     - expected requirement
     - observed implementation
     - mismatch check
3. Ensure every high-priority risk maps to at least one scenario.
4. Ensure scenarios remain high-level and do not yet contain procedural step detail.

## Phase 5 — Split coverage by test type
Goal: decide what should be manual, automated, exploratory, or deferred.

Steps:
1. Define categories:
   - Manual
   - Automated
   - Exploratory
   - Deferred / future non-functional
2. Manual bucket should include:
   - installation/environment checks
   - CLI interaction behavior
   - server startup/shutdown observations
   - malformed input behavior from the operator perspective
   - crash reproduction and investigation
3. Automated bucket should include:
   - deterministic auth flows
   - deterministic CRUD flows
   - deterministic search/read behavior
   - repeatable validation tests
   - deterministic response contract checks
4. Exploratory bucket should include:
   - mixed command batches
   - dirty database reruns
   - state transitions around login/logout
   - weird sequencing and partial-failure behavior
5. Deferred bucket should include:
   - performance/load
   - concurrency/race behavior
   - long-running soak behavior
   - security hardening beyond the assignment scope
6. Add rationale for each category so the split looks intentional.

## Phase 6 — Write detailed test cases
Goal: convert scenarios into executable tests and submission-grade manual cases.

Steps:
1. Create case templates with these fields:
   - Test Case ID
   - Related Scenario ID
   - Title
   - Objective
   - Preconditions
   - Test data
   - Steps
   - Expected result
   - Actual result
   - Status
   - Type
   - Priority
   - Execution mode
2. Start with high-priority cases:
   - sign up success
   - sign up duplicate username
   - sign up duplicate email expectation check
   - sign in success
   - sign in wrong password
   - sign in non-existing user
   - logout after login
   - logout before login
   - add contact
   - add second phone number
   - search by name/number
   - edit name only
   - edit phone only
   - remove contact
3. Add negative and robustness cases:
   - missing command name
   - unknown command name
   - missing parameters object
   - missing required field
   - empty values
   - invalid value type
   - malformed JSON file
   - repeated execution against existing DB
4. Mark each case as:
   - manual
   - automated candidate
   - exploratory only
5. Ensure each case has explicit expected result wording, including where expected behavior is ambiguous and should be observed rather than asserted from assumptions.

## Phase 7 — Define the automation approach
Goal: choose the test architecture before writing test code.

Steps:
1. Use a mixed strategy as the default:
   - primary coverage at business-logic level
   - smaller end-to-end layer through `client.py`/`server.py`
2. Logic-level automated tests should focus on:
   - command handler behavior
   - DB effects
   - validation and exceptions
3. End-to-end automated tests should focus on:
   - request/response contract
   - batch command execution
   - end-to-end state flow
4. Keep production changes out unless testability is impossible without a minimal seam.
5. Define automation boundaries clearly:
   - what is unit-like
   - what is integration
   - what stays manual
6. Require deterministic setup:
   - isolated DB per run or reset strategy
   - no shared state across tests
   - timeouts around client/server interactions
7. Plan the future test layout:
   - `tests/conftest.py`
   - `tests/test_auth.py`
   - `tests/test_phonebook_crud.py`
   - `tests/test_search.py`
   - `tests/test_validation.py`
   - `tests/test_state_security.py`

## Phase 8 — Define execution and evidence workflow
Goal: make test execution auditable and reportable.

Steps:
1. Establish execution order:
   - smoke/manual sanity
   - high-priority deterministic cases
   - negative cases
   - exploratory passes
2. Decide what evidence to capture:
   - command file used
   - console output
   - DB state note if relevant
   - error logs/tracebacks
3. Track result states:
   - Pass
   - Fail
   - Blocked
   - Not Run
4. Record whether each failure is:
   - confirmed bug
   - expected mismatch
   - environment/setup issue
   - unclear requirement
5. Feed confirmed issues into `TEST_REPORT.md` using bug IDs.

## Phase 9 — Write the final QA report
Goal: produce the final submission-quality summary.

Steps:
1. Include:
   - project overview
   - test scope
   - environment
   - strategy summary
   - scenario summary
   - manual vs automated split
   - execution summary
   - discovered bugs
   - residual risk
   - recommendations
2. Each bug entry should include:
   - Bug ID
   - title
   - severity
   - priority
   - environment
   - preconditions
   - steps
   - expected result
   - actual result
   - evidence
   - suspected root cause
3. Add a final section:
   - what was not tested
   - what should be tested next
   - what product clarifications are still needed

## Key Documentation Conventions
- Every scenario must trace to one or more risks.
- Every test case must trace to one scenario.
- Every bug must trace back to the failing case/scenario.
- Every mismatch between assignment and code must be documented explicitly.
- Do not silently convert ambiguous behavior into expected behavior.

## Test Coverage Themes to Guarantee
- Happy path
- Negative path
- Validation
- State transition
- Contract/response consistency
- Data consistency
- Repeatability/regression
- Exploratory crash hunting
- Environment/runtime behavior

## Public Interfaces and Artifacts
Planned additions:
- `docs/` folder with formal QA deliverables
- `tests/` folder for automated pytest coverage
- no production API changes by default
- no production code changes unless a minimal testability seam becomes necessary and is documented first

## Acceptance Criteria for the Planning Phase
- Documentation structure is fully defined before content writing starts.
- All major system risks are categorized before scenarios are written.
- All scenarios are grouped and prioritized before detailed cases are written.
- Manual, automated, exploratory, and deferred coverage are explicitly separated.
- The later implementation phase can proceed document by document without new structural decisions.

## Assumptions
- `docs/` will be the canonical place for QA deliverables.
- Formal QA style is preferred over lightweight engineering notes.
- Both assignment expectations and observed implementation behavior must be preserved in the docs.
- For automation, the default strategy is mixed: logic-focused tests plus a smaller end-to-end layer.
