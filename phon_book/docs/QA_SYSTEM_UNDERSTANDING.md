# QA System Understanding

## Purpose
This document defines the system under test, explains how it works end to end, identifies where state and persistence exist, and separates expected behavior from observed implementation behavior. Its purpose is to establish a factual baseline before risk analysis, scenario design, and test case creation.

## Project Overview
This project is a Python client/server phonebook system. The client reads user command data from a JSON file and sends those commands to the server through ZeroMQ. The server receives the command batch, dispatches each command to the relevant business-logic function, interacts with a SQLite database when needed, and returns a response to the client.

The system contains two main functional areas:
- user authentication commands
- phonebook contact management commands

From a QA perspective, this is not only a CRUD application. It is a stateful command-processing system with transport behavior, persistence behavior, and requirement-versus-implementation ambiguity.

## Architecture Summary
The request lifecycle of the system is as follows:

1. A user prepares or selects a JSON file containing one or more command objects.
2. `client.py` loads the file, checks that it exists, and parses the JSON content.
3. The client creates a ZeroMQ request socket and sends the parsed command batch to the server.
4. `server.py` waits for incoming data, receives the batch, and iterates through the commands in order.
5. Each command is dispatched through `core/factory_command.py` based on `command_name`.
6. The selected handler in `core/auth.py` or `core/phone_book.py` executes the business logic.
7. Database models in `core/models.py` create, read, update, or delete records in SQLite where needed.
8. The server builds a response and sends it back to the client.
9. The client receives the response and prints it to the console.

This architecture means command ordering matters. A later command in the same request may depend on state created by an earlier command in the same batch.

## Main Components and Responsibilities

### `client.py`
Role in the system:
- command file reader and request sender

Key responsibilities:
- parse command-line arguments
- validate that the JSON file path exists
- load and parse JSON content
- create a ZeroMQ request socket
- send command data to the server
- receive and print the response

Testing relevance:
- source of file-handling and malformed JSON behavior
- source of transport-level request behavior
- useful for manual and end-to-end integration testing

### `server.py`
Role in the system:
- command receiver and processing loop

Key responsibilities:
- parse command-line arguments
- create a ZeroMQ reply socket
- wait for incoming command batches
- dispatch commands one by one
- collect results and send them back
- maintain in-memory online user state

Testing relevance:
- source of batch execution behavior
- source of runtime crash behavior
- source of in-memory authentication/session state

### `core/factory_command.py`
Role in the system:
- command router

Key responsibilities:
- map command names to Python functions
- call the correct handler using `command_name`

Testing relevance:
- source of command dispatch behavior
- likely failure point for invalid or unsupported command names

### `core/auth.py`
Role in the system:
- authentication logic

Key responsibilities:
- register new users
- authenticate users by username/password
- remove users from in-memory online state on logout
- hash passwords using bcrypt

Testing relevance:
- source of signup/signin/logout business rules
- source of password verification behavior
- source of auth-state transition testing

### `core/phone_book.py`
Role in the system:
- phonebook business logic

Key responsibilities:
- add phonebook contacts
- remove contacts
- edit contacts
- add extra phone numbers
- search contacts by name or phone number
- list all contacts

Testing relevance:
- main target for CRUD and search testing
- likely source of duplicate-data and not-found behavior
- likely source of authorization expectation mismatch

### `core/models.py`
Role in the system:
- persistence layer and database schema definition

Key responsibilities:
- define SQLite database connection
- define ORM models
- create tables if needed
- open and close DB connections

Testing relevance:
- source of data constraints
- source of persistence behavior across runs
- source of integrity-error and state-leak behavior

### `samples/*.json`
Role in the system:
- manual test input examples

Key responsibilities:
- provide reusable command batches for manual execution

Testing relevance:
- useful for smoke tests and manual regression checks
- useful for studying request shape and command sequences

## Supported Commands

### `sign_up`
Parameters:
- `username`
- `password`
- `email`

Purpose:
- register a new authentication user

Observed implementation notes:
- password is hashed
- DB-level uniqueness exists for username
- email uniqueness is not clearly enforced in the current schema

### `sign_in`
Parameters:
- `username`
- `password`

Purpose:
- authenticate a user and add the username to in-memory online state

Observed implementation notes:
- auth state is stored in a process-local list
- authentication state is not persisted

### `logout`
Parameters:
- `username`

Purpose:
- remove a user from in-memory online state

Observed implementation notes:
- logout affects only in-memory state
- no DB state is changed

### `add_phone_user`
Parameters:
- `username`
- `phone_number`
- `explanation` (optional)

Purpose:
- create a new phonebook contact and attach an initial phone number

Observed implementation notes:
- contact username is stored in the phonebook table, not the auth table
- uniqueness rules depend on DB constraints in the phonebook schema

### `remove_phone_user`
Parameters:
- `username`

Purpose:
- remove a phonebook contact

Observed implementation notes:
- behavior for non-existing contacts should be verified from runtime behavior

### `edit_phone_user`
Parameters:
- `username`
- `phone_number`
- `new_username`
- `new_phone_number`

Purpose:
- edit an existing contact name, phone number, or both

Observed implementation notes:
- command assumes a matching existing contact record
- missing or non-existing values may cause runtime exceptions

### `add_phone_number`
Parameters:
- `username`
- `phone_number`

Purpose:
- add an additional phone number to an existing contact

Observed implementation notes:
- behavior depends on contact existence and phone-number uniqueness constraints

### `get_all_phone_users`
Parameters:
- none

Purpose:
- return all phonebook contacts and their numbers

Observed implementation notes:
- response format should be validated for empty and populated DB states

### `get_phone_user_by_name`
Parameters:
- `username`

Purpose:
- return contact details by contact name

Observed implementation notes:
- behavior for missing contacts should be validated

### `get_phone_user_by_number`
Parameters:
- `phone_number`

Purpose:
- return contact details by phone number

Observed implementation notes:
- phone numbers are treated as strings in the current implementation

## Request Model
The request model is batch-oriented.

The client sends a JSON list of command objects. Each object is expected to contain:
- `command_name`
- `parameters`

Example conceptual shape:

```json
[
  {
    "command_name": "sign_in",
    "parameters": {
      "username": "admin",
      "password": "admin"
    }
  },
  {
    "command_name": "get_all_phone_users",
    "parameters": {}
  }
]
```

Important request-model properties:
- the system accepts multiple commands in a single request
- commands are processed sequentially
- later commands may depend on the result of earlier commands
- malformed JSON is detected at the client file-loading stage before the request is sent

## Response Model
The intended success response shape is a list of result objects, where each item includes:
- `command_name`
- `result`

Observed implementation notes:
- success responses appear to be built as per-command result objects
- error responses may not follow the same structure consistently
- some exceptions may be converted to string messages
- some failures may propagate as runtime errors rather than structured contract responses

This means response consistency is a key QA concern and should be tested explicitly.

## State Model
The system is stateful in more than one way.

### Authentication State
Authentication state is stored in memory through the `online_users` list in `server.py`.

Implications:
- auth state exists only while the server process is running
- restarting the server resets online-user state
- auth state is not stored in SQLite

### Request and Batch State
Commands are executed in sequence within the same request.

Implications:
- command order matters
- a sign-in command earlier in a batch may affect later commands in the same batch
- one invalid command may affect later command execution depending on how exceptions are handled

### Database State
Database records are stored in SQLite and persist across executions.

Implications:
- test runs are not automatically isolated
- repeated runs may fail due to existing records
- runtime behavior can change depending on prior DB contents

## Persistence Model
The project uses SQLite through Peewee ORM. The database file is `sab.db`.

The model layer defines three primary tables.

### `Users`
Purpose:
- store authentication users

Important fields:
- `username`
- `email`
- `password`
- `salt`

Constraint relevance:
- username uniqueness is enforced
- salt uniqueness is enforced
- email uniqueness does not appear to be enforced at the schema level

### `PhoneUsers`
Purpose:
- store phonebook contacts

Important fields:
- `username`
- `explanation`

Constraint relevance:
- contact username uniqueness is enforced in the phonebook table

### `PhoneUsersNumbers`
Purpose:
- store one or more phone numbers linked to a phonebook contact

Important fields:
- `phone_number`
- `to_user`

Constraint relevance:
- phone number uniqueness is enforced
- one contact can have multiple numbers through the foreign-key relationship

## Business Behavior Notes
Several behaviors are important from a QA standpoint.

- Authentication commands exist, but current phonebook operations do not clearly enforce logged-in state.
- The system separates authentication users from phonebook contacts, even though both use the name `username`.
- Repeated runs against the same database may fail because old records remain in `sab.db`.
- Some invalid or duplicate operations may surface as DB integrity errors instead of user-friendly application errors.
- Some commands appear to assume that required records exist and may fail hard if the assumption is false.
- The command batch model creates a risk of partial success, where earlier commands succeed before a later command fails.

## Expected vs Observed Behavior

### Authentication required before phonebook actions
Expected:
- phonebook modification or retrieval may be expected to require login

Observed:
- phonebook functions do not clearly check `online_users`

Status:
- mismatch / suspected defect or undocumented behavior

### Duplicate email handling
Expected:
- assignment-style expectation suggests each email should be unique

Observed:
- `Users.email` is not clearly unique in the DB schema

Status:
- mismatch / suspected defect

### Logout effect on later actions
Expected:
- logout should prevent further authenticated actions if auth is required

Observed:
- because auth enforcement is unclear, logout may not protect phonebook actions in practice

Status:
- mismatch or ambiguous behavior

### Response contract consistency
Expected:
- response format should consistently contain `command_name` and `result`

Observed:
- success paths appear structured, but error paths may return plain strings or crash behavior

Status:
- mismatch / risk area

### Malformed JSON handling
Expected:
- malformed JSON should be handled gracefully

Observed:
- malformed JSON is caught on the client side before network transmission

Status:
- likely match, but should still be verified

### Duplicate phone number behavior
Expected:
- system should either reject duplicates cleanly or define duplicate behavior explicitly

Observed:
- phone number uniqueness is enforced by DB constraints

Status:
- partially defined, runtime behavior still requires verification

### Missing parameter behavior
Expected:
- system should return clear validation errors

Observed:
- some handlers directly access dictionary keys and may raise runtime errors if fields are missing

Status:
- mismatch / likely robustness defect

### User isolation behavior
Expected:
- if auth exists, data ownership or access rules may be expected

Observed:
- phonebook data appears global rather than user-scoped

Status:
- ambiguous requirement / observed global behavior

### Repeated execution against existing DB data
Expected:
- repeated runs should ideally be predictable or explicitly documented

Observed:
- persistent DB state causes repeat-run conflicts such as uniqueness failures

Status:
- known operational risk

## Assumptions and Ambiguities
The following questions remain important for later QA design:

- Is login required before phonebook operations?
- Is the phonebook global for all users, or scoped per authenticated user?
- Should duplicate email addresses be rejected?
- Should non-existing contact edit/delete/search operations return graceful errors or behave as no-ops?
- Should malformed or invalid command batches partially succeed or fail as a whole?
- Should all error responses use a structured JSON contract?
- Should logout have any effect on phonebook commands in the current business model?

These items should be treated as explicit ambiguity points until validated by code behavior, assignment wording, or stakeholder clarification.

## QA-Relevant Observations
This system is QA-relevant for several reasons:
- it is stateful both in memory and in persistent storage
- it processes multiple commands in one request batch
- transport behavior and business behavior interact through the client/server boundary
- persistence across runs changes runtime results and repeatability
- the current implementation likely differs from normal backend expectations in several places
- defect-prone areas are concentrated around validation, state transitions, persistence constraints, and inconsistent error handling

This document provides the factual system baseline that later phases will use for risk analysis, test scenario design, detailed test cases, and bug reporting.
