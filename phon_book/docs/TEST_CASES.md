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

## Notes for Later Phases
- The current workbook contains only Wave 1 high-priority cases.
- Later waves should extend coverage for business CRUD flows, state behavior, persistence behavior, and concurrency.
