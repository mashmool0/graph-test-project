# QA Risk Catalog

## Purpose
This document lists and categorizes the main quality risks, requirement mismatches, failure modes, and uncertainty areas in the project. Its purpose is to create a structured risk baseline before detailed scenario design and test-case creation.

## Scope of This Document
- risk categories
- risk classification rules
- risk entry structure
- requirement-versus-code mismatch areas
- quality risk inventory
- evidence-oriented risk framing

## Risk ID Convention
- Format: `RISKgs
- -###`

## Traceability Rule
- Every risk should later map to one or more `SCN-###` items.
- Where possible, confirmed bugs should trace back to the related risk.

## Risk Classification Rules
- A risk is any behavior, design gap, implementation weakness, or requirement mismatch that may cause incorrect results, unsafe behavior, poor resilience, or unclear system behavior.
- Risks should be based on one or more of these sources:
  - assignment requirements
  - observed runtime behavior
  - observed implementation behavior
- Requirement mismatch should be documented explicitly rather than hidden inside generic functional defects.
- Evidence-oriented wording should be used. Risks should not be written as assumptions unless clearly labeled as ambiguity or suspected behavior.

## Risk Entry Template
Each future `RISK-###` entry should contain the following fields.

### 1. Risk ID
Purpose:
- provide stable traceability across scenarios, test cases, and bug reports

Format:
- `RISK-###`

### 2. Title
Purpose:
- provide a short and readable description of the risk

Guideline:
- title should be concise, specific, and outcome-oriented

### 3. Category
Purpose:
- place the risk under one of the approved top-level risk categories

Guideline:
- each risk should have one primary category
- related cross-category effects can be mentioned in notes if needed

### 4. Description
Purpose:
- describe the risk factually and clearly

Guideline:
- describe what may go wrong or what is already observed to go wrong
- avoid solution language in this field

### 5. Requirement Basis
Purpose:
- identify the requirement, expected business rule, or expected system behavior that gives this risk meaning

Guideline:
- if the task explicitly defines the expected behavior, cite that basis
- if no explicit requirement exists, clearly state whether the expectation comes from common backend/API behavior or inferred product logic

### 6. Observed Behavior / Code Basis
Purpose:
- record the implementation or runtime evidence behind the risk

Guideline:
- cite observed runtime behavior, code inspection findings, schema observations, or sample-command behavior
- this field should explain why the risk is believed to be real or plausible

### 7. Impact
Purpose:
- explain the likely consequence if the risk occurs

Guideline:
- describe business, user, data, stability, or security impact
- focus on the effect, not the cause

### 8. Severity
Purpose:
- indicate how serious the consequence is if the risk is confirmed

Allowed values:
- Critical
- High
- Medium
- Low

Guideline:
- severity reflects consequence seriousness, not testing convenience

### 9. Priority
Purpose:
- indicate how urgently the risk should be tested and tracked

Allowed values:
- High
- Medium
- Low

Guideline:
- priority reflects investigation and coverage urgency
- priority may differ from severity depending on scope and assignment relevance

### 10. Evidence Source
Purpose:
- record the source of belief for the risk

Possible values include:
- assignment requirement
- code inspection
- manual runtime test
- sample input/output behavior
- schema/model inspection
- environment observation

Guideline:
- one risk may have multiple evidence sources

### 11. Candidate Test Direction
Purpose:
- define how the risk should later be explored or covered in testing

Possible forms include:
- manual test
- automated test
- exploratory test
- integration test
- negative test
- contract test
- state-transition test
- concurrency test

Guideline:
- this is not a full test case
- it only points toward the later test design direction

### 12. Notes / Ambiguity
Purpose:
- capture uncertainty, open questions, or requirement ambiguity linked to the risk

Guideline:
- use this field when the requirement is unclear, behavior is only partially observed, or multiple interpretations are possible

## Risk Entry Writing Rules
- Every risk entry should separate expected behavior from observed behavior.
- Every risk entry should be evidence-based.
- Every risk entry should be written in factual language, not emotional or speculative language.
- Every risk entry should be useful for later scenario creation.
- Risk entries should not contain full reproduction steps or final bug-report details.
- Risk entries should not contain implementation fix proposals unless a note is necessary to clarify the nature of the risk.

## Top-Level Risk Categories

### 1. Requirement Compliance Risks
Meaning:
- places where the implementation may not satisfy the assignment requirements or expected behavior described by the task

Typical focus areas:
- login expected by email and password versus implementation using username and password
- post-authentication behavior required by the task
- expected response/result format
- uniqueness rules or workflow rules described by the assignment

Boundary:
- use this category when the primary concern is mismatch with the stated task requirement

### 2. Authentication Risks
Meaning:
- risks in signup, signin, and logout behavior itself

Typical focus areas:
- duplicate username registration behavior
- duplicate email registration behavior
- email validation quality
- incorrect credential handling
- missing auth fields
- wrong password behavior
- unsupported login identity rules

Boundary:
- use this category for identity verification and account-authentication logic
- do not use it for data ownership or permission checks after login

### 3. Authorization and Access Control Risks
Meaning:
- risks related to whether a user is permitted to perform an action or access a given set of data

Typical focus areas:
- contact operations without login
- contact operations after logout
- shared global phonebook behavior
- absence of ownership link between auth users and phonebook contacts
- one user viewing or editing another user’s contact data

Boundary:
- use this category for permission and ownership problems
- keep it separate from authentication correctness

### 4. Session and State Risks
Meaning:
- risks caused by in-memory state, execution order, lifecycle behavior, and multi-step transitions over time

Typical focus areas:
- `online_users` behavior
- logout affecting active-user state
- server restart removing in-memory state
- command ordering inside one batch request
- partial success followed by later failure
- stale or inconsistent in-memory state

Boundary:
- use this category for temporal behavior and state transitions
- do not use it for long-term DB consistency or access-control rules

### 5. Contact Management Risks
Meaning:
- business-logic risks in phonebook contact creation, modification, retrieval, and deletion

Typical focus areas:
- add contact behavior
- add second phone number behavior
- edit contact behavior
- delete contact behavior
- search by name or number
- list all contacts
- not-found contact operations
- duplicate contact or duplicate number behavior at business level

Boundary:
- use this category for core phonebook functionality
- do not use it for malformed input shape or generic server-crash handling

### 6. Validation and Input Handling Risks
Meaning:
- risks related to invalid, incomplete, malformed, or unexpected input values and request structures

Typical focus areas:
- missing `command_name`
- missing `parameters`
- missing required fields such as `username`, `password`, or `phone_number`
- wrong input types
- empty values
- invalid email format
- malformed JSON file structure
- unsupported or unexpected field names

Boundary:
- use this category to describe the invalid input itself
- reaction quality to the invalid input belongs under error handling if needed

### 7. Response and Error Handling Risks
Meaning:
- risks related to failure behavior, system resilience, and response consistency

Typical focus areas:
- server crash on bad input
- inconsistent error response shape
- plain string errors versus structured result objects
- traceback exposure
- inability to continue serving requests after one failure
- partial failure handling in batch execution

Boundary:
- use this category for how the system reacts to success and failure
- keep it separate from the definition of invalid input itself

### 8. Persistence and Data Consistency Risks
Meaning:
- risks related to stored data correctness, integrity, uniqueness, and repeatability across runs

Typical focus areas:
- DB uniqueness constraints
- duplicate email not enforced in schema
- duplicate phone-number behavior
- persistent DB state affecting repeated test runs
- consistency of edit/delete behavior
- relationship integrity between contacts and phone numbers
- DB integrity errors surfacing from business actions

Boundary:
- use this category for long-lived stored state and relational correctness
- keep it separate from temporary in-memory auth/session behavior

### 9. Security Risks
Meaning:
- risks with security impact that go beyond ordinary functional failure

Typical focus areas:
- weak authorization model with exposure impact
- denial-of-service style crash behavior
- password hashing quality
- salt handling and credential-storage concerns
- information leakage through exceptions or raw error output
- abuse-oriented input behavior with security consequences

Boundary:
- use this category for vulnerability-oriented concerns and security impact
- do not treat every normal validation defect as a security issue unless the impact justifies it

### 10. Concurrency and Multi-User Risks
Meaning:
- risks that appear when overlapping requests, simultaneous users, or shared mutable state interact

Typical focus areas:
- near-simultaneous signup or edit requests
- races around duplicate data creation
- shared `online_users` state across multiple users
- request interference between active users
- concurrent modification of the same contact data
- DB locking or ordering issues under overlapping activity

Boundary:
- use this category for overlapping-user or overlapping-request behavior
- do not use it for ordinary single-user flows

### 11. Operational and Environment Risks
Meaning:
- risks related to setup, runtime environment, reproducibility, and execution practicality

Typical focus areas:
- Python version compatibility
- dependency installation issues
- proxy or network-environment issues
- DB cleanup between test runs
- server startup and shutdown reliability
- reproducibility of manual test runs
- environment-specific instability

Boundary:
- use this category for execution-environment and testability concerns rather than business-logic defects

## Notes for Later Phases
- The detailed risk inventory is maintained in `QA_RISK_CATALOG.xlsx`.
- This Markdown file defines the structure, rules, and category framework for the risk catalog.
- Later phases should map spreadsheet risks to scenarios and test cases.
