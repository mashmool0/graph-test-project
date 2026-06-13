# Test Strategy

## Purpose
This document defines the testing approach for the `phon_book` project, explains how coverage is selected, and formalizes the split between manual, automated, exploratory, and deferred testing.

Its purpose is to show that test implementation decisions are risk-based, not arbitrary.

## Testing Objectives
The testing strategy for this project is designed to:
- verify whether the implementation satisfies the assignment requirements
- identify mismatches between expected behavior and actual code/runtime behavior
- validate the most critical business and security-related risks first
- protect the system against regression in deterministic high-value areas
- capture unstable, ambiguous, and environment-sensitive behavior through manual and exploratory testing

## Strategy Summary
This project should not be tested as a simple CRUD application only. It is a stateful client/server command-processing system with:
- ZeroMQ transport behavior
- JSON request/response contract behavior
- SQLite persistence
- in-memory authentication/session state
- requirement-versus-implementation mismatches

Because of that, the strategy is:
- risk-first
- evidence-driven
- mixed manual and automated
- layered by execution cost and determinism

The recommended delivery order is:
1. system understanding
2. risk catalog
3. scenario inventory
4. test strategy
5. high-priority test cases
6. automated implementation for deterministic cases
7. final test report

## Coverage Principles
Coverage should be selected using these principles:

### 1. Risk-first coverage
Prioritize scenarios and test cases that target:
- requirement mismatches
- unauthorized access behavior
- server crash behavior
- validation failures
- contract inconsistency
- persistence and initialization defects

### 2. Deterministic-first automation
Automate cases that:
- are repeatable
- have clear pass/fail conditions
- are likely to be re-run as regression checks
- do not depend heavily on unstable environment timing

### 3. Exploratory-first uncertainty handling
Where requirements are ambiguous or behavior is unstable, exploratory testing should happen before committing to strong automated assertions.

### 4. Environment-aware execution
Because database persistence and server crash behavior affect repeatability, setup and teardown conditions must be explicit in both manual and automated execution.

## Test-Type Split
The project should be divided into four testing buckets.

### A. Manual Testing
Manual testing is required where:
- the behavior is user-visible and CLI-driven
- recovery workflow matters
- environment setup affects outcome
- output needs qualitative review
- exploratory understanding is needed before stable automation

Manual testing should cover:
- installation and environment setup
- client/server startup workflow
- malformed JSON file behavior from the operator perspective
- crash reproduction and restart workflow
- requirement-compliance checks such as email-based login expectation
- initial validation of newly discovered defects
- business happy paths for baseline understanding

Examples from this project:
- login by email requirement mismatch
- duplicate signup crash reproduction
- first phonebook operation on clean DB
- manual observation of traceback leakage
- repeat-run behavior with persistent `sab.db`

### B. Automated Testing
Automated testing should cover deterministic regression-friendly behavior.

Automated tests should focus on:
- signup/signin business outcomes
- duplicate username and duplicate email behavior
- missing required field handling
- invalid type handling
- unauthenticated contact action behavior
- response contract behavior for success and failure
- schema initialization ordering defect
- duplicate contact and duplicate phone number behavior
- not-found contact behavior where assertions can be made cleanly

Why automate these:
- high value
- clear expected outcomes
- strong regression benefit
- can be executed repeatedly without human interpretation once setup is controlled

### C. Exploratory Testing
Exploratory testing is required where behavior is:
- ambiguous by requirement
- unstable by design
- multi-step and stateful
- difficult to assert safely without first learning runtime behavior

Exploratory testing should cover:
- batch partial-success behavior
- logout interference across users
- user-isolation expectations versus global phonebook behavior
- concurrency and overlapping request behavior
- mixed valid/invalid command batches
- state transitions around login/logout and restart

Why exploratory first:
- these areas may need refinement before strong automated expectations are safe
- useful for finding additional undocumented issues

### D. Deferred / Future Testing
Some testing areas should be documented but not prioritized in the first implementation cycle.

Deferred scope includes:
- performance/load testing
- long-running soak behavior
- deep concurrency stress testing
- broader security-hardening review beyond assignment scope
- platform-matrix environment testing

These are valid concerns but not the highest-value first-wave deliverables for this assignment.

## Manual vs Automated Decision Rules
When deciding whether a scenario becomes manual or automated, use these rules.

### Prefer automated when:
- the case is deterministic
- the expected result is exact
- the setup can be controlled
- the same case will be re-run often
- the failure is high value for regression

### Prefer manual when:
- the case needs visual/log review
- the setup is environment-sensitive
- the behavior is qualitative or ambiguous
- the case is useful mainly for first-pass bug discovery

### Prefer exploratory when:
- the requirement is unclear
- the state model is complex
- the expected result is not yet safely specifiable
- the purpose is to discover failure patterns rather than verify one stable rule

## Current Wave-Based Test Plan
The current test-case inventory is intentionally split into waves.

### Wave 1 — High-risk validated failures
Focus:
- authentication requirement mismatch
- duplicate signup behavior
- missing-field crashes
- wrong-type crashes
- unauthorized contact actions
- error response contract failures
- traceback/SQL leakage
- phonebook schema initialization defect
- duplicate contact and duplicate phone-number failures
- add-number to missing contact

Reason:
- these are the highest confirmed risks and strongest submission-value findings

### Wave 2 — Core business flow coverage
Focus:
- signup success
- signin success
- wrong-password login
- logout success
- create contact
- add second phone number
- list contacts
- search by name/number
- edit name only
- edit phone only
- edit both
- delete existing contact
- not-found search/edit/delete cases

Reason:
- these establish normal business coverage and CRUD/search regression baseline

### Wave 3 — State, persistence, concurrency, and operational depth
Planned focus:
- batch partial-success behavior
- persistent-state repeatability
- multi-user logout interference
- shared phonebook access isolation
- concurrent duplicate creation
- overlapping-session state
- crash recovery workflow

Reason:
- these are important but are either more exploratory or more environment-sensitive than Wave 1 and Wave 2

## Automation Approach
The recommended automation approach is mixed.

### Primary automated layer
Target:
- business logic and integration-level deterministic behavior

Recommended focus:
- command handlers and their outcomes
- DB effects where setup can be isolated
- validation/error behavior
- response contract checks

### Secondary end-to-end layer
Target:
- selected client/server protocol flows through ZeroMQ

Recommended focus:
- request/response contract
- batch execution behavior
- end-to-end auth and phonebook flows

### Not recommended as first automation step
- heavy concurrency harnesses
- unstable crash-recovery assertions without isolation
- broad environment automation

## Test Environment and State Control Principles
Because this application is stateful, all execution should respect these rules:
- use a clean or explicitly prepared SQLite state before each deterministic run
- document whether schema initialization has already happened
- isolate destructive validation when possible
- use timeouts for client/server communication in automated checks
- avoid sharing state across automated tests unless the scenario explicitly requires it

Operationally, this project has already shown that:
- persistent DB state affects repeatability
- some bad requests terminate the server
- some defects require isolation to validate safely

## Evidence Collection Rules
During test execution, collect:
- command payload or command file used
- client-visible output
- server-visible output if relevant
- whether server remained alive after the request
- database state note when persistence matters
- exact failure text for raw exception paths

These evidence points are especially important for:
- error-handling defects
- requirement mismatches
- persistence/state defects
- security-related output leakage

## Exit Guidance for Automation Start
Automated implementation should begin only after:
- the main Wave 1 test cases are defined
- risk and scenario traceability is stable
- deterministic setup expectations are documented

At the current project state, those conditions are largely satisfied for Wave 1 automation.

## Recommended Immediate Next Steps
1. Keep `TEST_CASES.xlsx` as the implementation backlog.
2. Start automated implementation with Wave 1 deterministic cases only.
3. Leave Wave 3 areas exploratory until their behavior is better characterized.
4. Use `TEST_REPORT.md` later to distinguish:
   - confirmed defect
   - requirement mismatch
   - environment/setup issue
   - ambiguous behavior
