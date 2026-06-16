# Bug Register

This register maps the 22 failing documented automated cases to formal defect entries. Each entry identifies the failing behavior, impacted area, and likely problem location.

## BUG-001
- Title: Email-based login is not supported and destabilizes the server path
- Related Case: `TC-001`
- Severity: High
- Priority: High
- Area: Authentication / `core/auth.py`
- Preconditions: Registered user exists
- Steps:
  1. Register a user with username, email, and password.
  2. Attempt `sign_in` using the email and password.
- Expected Result: Login by email succeeds or returns a controlled rejection without server termination.
- Actual Result: Email-based login is not supported and the server path stops.
- Problem Detail: Sign-in logic uses username lookup instead of the required email-based authentication flow.

## BUG-002
- Title: Duplicate email registration is accepted
- Related Case: `TC-002`
- Severity: High
- Priority: High
- Area: Registration validation / `core/auth.py`, `core/models.py`
- Preconditions: First user with target email already exists
- Steps:
  1. Register user A.
  2. Register user B with the same email.
- Expected Result: Second registration is rejected with a controlled structured error.
- Actual Result: Second registration succeeds.
- Problem Detail: No effective uniqueness enforcement exists for email at validation or schema level.

## BUG-003
- Title: Duplicate username registration terminates the server
- Related Case: `TC-003`
- Severity: High
- Priority: High
- Area: Registration error handling / `core/auth.py`, `server.py`
- Preconditions: Username already exists
- Steps:
  1. Register a user.
  2. Register another user with the same username.
- Expected Result: Duplicate username is rejected without service termination.
- Actual Result: Raw integrity failure path stops the server.
- Problem Detail: DB constraint exceptions are not translated into controlled application errors.

## BUG-004
- Title: Missing signup username crashes the server
- Related Case: `TC-004`
- Severity: High
- Priority: High
- Area: Input validation / `core/auth.py`
- Preconditions: None
- Steps:
  1. Send `sign_up` without `username`.
- Expected Result: Controlled validation error with server alive.
- Actual Result: Server stops.
- Problem Detail: Required-field validation is missing before direct dictionary access.

## BUG-005
- Title: Non-string password crashes signup flow
- Related Case: `TC-005`
- Severity: High
- Priority: High
- Area: Input validation / password handling / `core/auth.py`
- Preconditions: None
- Steps:
  1. Send `sign_up` with integer password.
- Expected Result: Controlled validation error with server alive.
- Actual Result: Server stops.
- Problem Detail: Password hashing path assumes string-like input and is not type-guarded.

## BUG-006
- Title: Missing phone number in contact creation crashes the server
- Related Case: `TC-006`
- Severity: High
- Priority: High
- Area: Phonebook validation / `core/phone_book.py`
- Preconditions: Authenticated user exists
- Steps:
  1. Send `add_phone_user` without `phone_number`.
- Expected Result: Controlled validation error with server alive.
- Actual Result: Server stops.
- Problem Detail: Required-field validation is missing before command processing.

## BUG-007
- Title: Contact creation is allowed without sign-in
- Related Case: `TC-007`
- Severity: High
- Priority: High
- Area: Authorization / `core/phone_book.py`, `server.py`
- Preconditions: User may be registered but not signed in
- Steps:
  1. Send `add_phone_user` without `sign_in`.
- Expected Result: Unauthorized request is rejected.
- Actual Result: Contact is created successfully.
- Problem Detail: Phonebook handlers do not enforce authenticated-session checks.

## BUG-008
- Title: Contact listing is allowed without sign-in
- Related Case: `TC-008`
- Severity: High
- Priority: High
- Area: Authorization / `core/phone_book.py`
- Preconditions: Contact data exists, caller is not signed in
- Steps:
  1. Send `get_all_phone_users` without `sign_in`.
- Expected Result: Unauthorized request is rejected.
- Actual Result: Contact list is returned.
- Problem Detail: Read operations are not protected by authentication or ownership checks.

## BUG-009
- Title: Duplicate-username failure does not return structured error
- Related Case: `TC-010`
- Severity: High
- Priority: High
- Area: Error contract / `core/factory_command.py`, `server.py`
- Preconditions: Username already exists
- Steps:
  1. Trigger duplicate username registration.
- Expected Result: Structured error result with server alive.
- Actual Result: Failure is unstructured and destabilizes the server.
- Problem Detail: Failure paths do not follow the documented `command_name/result` contract.

## BUG-010
- Title: Invalid auth request terminates the service
- Related Case: `TC-011`
- Severity: High
- Priority: High
- Area: Service resilience / `server.py`
- Preconditions: None
- Steps:
  1. Send malformed signup request.
  2. Attempt a subsequent valid request.
- Expected Result: Service survives invalid request.
- Actual Result: Service terminates on invalid request.
- Problem Detail: Unhandled exceptions propagate to the top-level server loop.

## BUG-011
- Title: Failure responses leak internal implementation details
- Related Case: `TC-012`
- Severity: High
- Priority: High
- Area: Error handling / `server.py`, ORM integration
- Preconditions: Any failure-producing request
- Steps:
  1. Trigger a business or validation failure.
- Expected Result: Controlled safe error response.
- Actual Result: Internal DB/model details leak.
- Problem Detail: Exceptions are exposed directly instead of being sanitized.

## BUG-012
- Title: Duplicate contact creation terminates the server
- Related Case: `TC-014`
- Severity: High
- Priority: High
- Area: Phonebook duplicate handling / `core/phone_book.py`
- Preconditions: Contact already exists
- Steps:
  1. Create contact.
  2. Create same contact again with `add_phone_user`.
- Expected Result: Controlled duplicate-contact rejection.
- Actual Result: Server stops.
- Problem Detail: Duplicate contact path leaks raw DB constraint behavior.

## BUG-013
- Title: Duplicate phone number creation terminates the server
- Related Case: `TC-015`
- Severity: High
- Priority: High
- Area: Phonebook duplicate handling / `core/phone_book.py`
- Preconditions: Phone number already exists
- Steps:
  1. Create a contact with phone number.
  2. Create another contact using the same number.
- Expected Result: Controlled duplicate-number rejection.
- Actual Result: Server stops.
- Problem Detail: Duplicate phone-number path is not translated into business-level failure.

## BUG-014
- Title: Adding a phone number to a missing contact terminates the server
- Related Case: `TC-016`
- Severity: High
- Priority: High
- Area: Not-found handling / `core/phone_book.py`
- Preconditions: Target contact does not exist
- Steps:
  1. Send `add_phone_number` for a missing contact.
- Expected Result: Controlled not-found result.
- Actual Result: Server stops.
- Problem Detail: Missing-contact path is not handled as a controlled business error.

## BUG-015
- Title: Repeat-run duplicate signup stops the server
- Related Case: `TC-017`
- Severity: Medium
- Priority: High
- Area: Persistence repeatability / `core/auth.py`, `server.py`
- Preconditions: Persistent DB already contains the user
- Steps:
  1. Run signup successfully once.
  2. Run the same signup again without DB reset.
- Expected Result: Predictable controlled duplicate handling.
- Actual Result: Server stops on duplicate repeat-run path.
- Problem Detail: Duplicate handling against persistent state is not operationally safe.

## BUG-016
- Title: Wrong-password login path is not controlled
- Related Case: `TC-020`
- Severity: High
- Priority: High
- Area: Authentication / `core/auth.py`
- Preconditions: Registered user exists
- Steps:
  1. Attempt `sign_in` with wrong password.
- Expected Result: Controlled wrong-password response with server alive.
- Actual Result: Server path does not remain stable.
- Problem Detail: Wrong-password branch is not handled as a safe business failure.

## BUG-017
- Title: Delete-existing-contact flow is not cleanly verifiable
- Related Case: `TC-030`
- Severity: Medium
- Priority: Medium
- Area: Delete flow / `core/phone_book.py`
- Preconditions: Contact exists
- Steps:
  1. Create a contact.
  2. Delete it.
  3. Verify retrieval after deletion.
- Expected Result: Delete succeeds and follow-up verification is controlled.
- Actual Result: Flow does not stay controlled through verification.
- Problem Detail: Delete behavior and follow-up not-found handling do not compose safely.

## BUG-018
- Title: Search by non-existing contact name terminates the server
- Related Case: `TC-031`
- Severity: High
- Priority: High
- Area: Not-found handling / `core/phone_book.py`
- Preconditions: Target contact does not exist
- Steps:
  1. Search by missing contact name.
- Expected Result: Controlled not-found result.
- Actual Result: Server stops.
- Problem Detail: Name-based search lacks safe not-found handling.

## BUG-019
- Title: Search by non-existing phone number terminates the server
- Related Case: `TC-032`
- Severity: High
- Priority: High
- Area: Not-found handling / `core/phone_book.py`
- Preconditions: Target number does not exist
- Steps:
  1. Search by missing phone number.
- Expected Result: Controlled not-found result.
- Actual Result: Server stops.
- Problem Detail: Number-based search lacks safe not-found handling.

## BUG-020
- Title: Removing a non-existing contact reports false success
- Related Case: `TC-033`
- Severity: Medium
- Priority: High
- Area: Delete semantics / `core/phone_book.py`
- Preconditions: Target contact does not exist
- Steps:
  1. Send `remove_phone_user` for a missing contact.
- Expected Result: Controlled not-found outcome.
- Actual Result: Success is reported for a contact that does not exist.
- Problem Detail: Delete command does not validate affected-record existence before reporting success.

## BUG-021
- Title: Editing a non-existing contact terminates the server
- Related Case: `TC-034`
- Severity: High
- Priority: High
- Area: Update flow / `core/phone_book.py`
- Preconditions: Target contact does not exist
- Steps:
  1. Send `edit_phone_user` for a missing contact.
- Expected Result: Controlled not-found outcome.
- Actual Result: Server stops.
- Problem Detail: Update path does not safely handle missing target records.

## BUG-022
- Title: Invalid email format is accepted during registration
- Related Case: `TC-035`
- Severity: Medium
- Priority: High
- Area: Registration validation / `core/auth.py`
- Preconditions: None
- Steps:
  1. Attempt signup with malformed email such as `abc`.
- Expected Result: Controlled invalid-email rejection.
- Actual Result: Signup succeeds.
- Problem Detail: Email format validation is missing.
