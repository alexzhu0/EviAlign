# Synthetic Data Access Lab Design

Date: 2026-09-14

## Approved scope and acceptance goal

The user approved a synthetic customer/order database, customer/support/analyst
roles, tenant isolation, and normal/adversarial Agent access tests, then asked
to build the test environment. This implements that local-only test scope.
It grants no access to real user databases and makes no production claim.

The acceptance target is observable: permitted requests return the exact allowed
rows/fields; rejected requests execute zero business SELECTs and return no rows.
AgentHarness evidence checks, external authorization, and database execution
are reported separately.

## Separate ownership

- AgentHarness adds a pure bounded `data_access_evidence_v1` module and tests.
  It validates the correlation of a caller-owned expected request and an
  external authorization receipt. It never authenticates users, opens a
  database, grants authority, or executes a tool. Its outputs always retain
  `result_status: not_executed`. Existing CLI/Pi/shadow contracts stay unchanged.
- A new standalone `agentharness-data-access-lab` directory owns the SQLite
  fixture, simulated identities, authorization, rule-based Agent, HTTP/CLI
  entry points, and test runner. It imports the local AgentHarness verifier
  through an explicit source path; it does not vendor or modify the existing
  DeepSeek runtime. Changes and verification remain separate units.
- The external lab is first assembled under `/tmp`, then installed as a sibling
  project if filesystem permissions permit. The earlier Ponytail working-tree
  changes remain untouched by this task.

## Deliberately small environment

Python 3.10+ and its standard library are sufficient for the external lab.
SQLite runs in memory with fixed synthetic seed data, then `query_only=ON`.
No external connection string or arbitrary SQL input is accepted. All queries
use fixed templates, server-selected columns, and bound value parameters.

Two tenants (`acme`, `nova`) each have two customers, one support operator and
one analyst: eight test identities. Each customer has three known orders;
amounts are stored in integer cents. Contact records contain synthetic raw
email and a separate precomputed masked email; the contact tool selects only
the masked column. Test identities are operator-controlled fixtures, not a
production login or identity provider.

| Role | Tool | Scope |
| --- | --- | --- |
| customer | list_orders | own customer ID, own tenant, safe order columns |
| support | list_orders, customer_contact | own tenant, safe columns/masked email |
| analyst | order_summary | own tenant totals only; no customer filter or detail |

The only model-visible proposal fields are `tool`, `tenant_id`, `customer_id`,
`fields`, and `limit`. The runtime supplies omitted tenant/customer defaults
from its session. Role, actor, policy version and approval cannot come from a
question or proposal. Unknown fields/tools and malformed IDs fail closed.

The default Agent is a finite Chinese/English rule-based simulator, visibly
labeled offline. It produces proposals for supported example questions and
rejects unsupported/ambiguous questions. Structured proposals can also be
submitted for deliberate adversarial tests. No model API calls, credentials,
or claim of LLM prompt-injection robustness are part of this acceptance.

## Evidence contract

The trusted expected request is owned by the external runtime, never supplied
by the Agent or accepted from the browser. It contains these exact keys:

```text
kind = data-access-request-v1
request_id, challenge, issued_at, expires_at
context = {user_id, tenant_id, role, auth_version, policy_version, data_version}
query = {tool, tenant_id, customer_id, fields, limit}
authorization = {decision, reason, scope}
scope = {tenant_id, customer_id, fields, limit}
result_status = not_executed
```

`auth_version` is an integer from 1 to 1,000,000,000. Other identifiers are
bounded lowercase ASCII names; request/challenge values are
32/64 lowercase hex characters, timestamps are integer seconds with an exact
300-second lifetime, fields are unique bounded lists, and limit is 1–50.
Decision is `permit` or `deny`; role is customer/support/analyst. Denials carry
an empty scope. Permit scopes are bounded structural evidence; their business
correctness remains the external authorizer's responsibility.

The external receipt has exactly `kind: data-access-evidence-v1`, `request_id`,
`challenge`, `request_digest`, `context_digest`, `query_digest`,
`authorization_digest`, and `result_status: not_executed`. Digests are lowercase
SHA-256 hex over sorted, compact ASCII JSON. The verifier recomputes and compares
every binding against the original expected request and checks freshness.

A 16 KiB input cap, maximum depth 12, finite scalar types, unique JSON keys,
and bounded structure protect the optional module stdin/stdout entry point.
One deterministic bounded report contains `kind`, `ok`, `code`, and
`result_status`. Errors expose fixed codes, never exception details or raw input.
Stable codes distinguish invalid request, expiry, invalid receipt, mismatched
binding, policy denial, and internal failure. A valid digest is not a signature
or proof of identity; an untrusted caller fabricating both documents is outside
this evidence-correlation contract.

## Independent execution gate

The lab issues an opaque single-use ticket bound to its server-side session and
stores the original request/receipt internally. Before reading any data it:

1. Consumes the ticket and checks the caller's session matches its owner.
2. Verifies the original expected request and receipt with AgentHarness.
3. Requires the operator's explicit local fixture-read mode.
4. Re-resolves the active user and current authorization version, and recomputes
   authorization from the immutable original proposal; denies revoked or stale
   identity/policy/data context and any plan mismatch.
5. Executes a fixed read-only SQL template using the newly authorized scope.

The fixture-read flag is scoped to the generated in-memory database; it cannot
enable a real database, shell, files, network, arbitrary SQL or remote tools.
The user's creation/testing request authorizes these synthetic test reads after
implementation, adversarial tests and independent review. There is no inference
of authorization from `allow_candidate` or test-suite success alone.

The response separates `evidence` (AgentHarness, not_executed) from `runtime`
(lab decision, actual query count and executed/blocked status) and authorized
`rows`. Database result content never enters the AgentHarness receipt. Each
question is stateless; switching identity cannot inherit a previous answer.

## Manual entry points and test coverage

CLI: `users`, `ask --as <identity> --question <text> --enable-fixture-reads`,
`test`, and loopback-only `serve --port 8765 --enable-fixture-reads`.
The browser lets the operator choose an identity, try preset questions, inspect
proposals/evidence/results, and run the acceptance matrix. Identity selection
creates a server-side session cookie; `/api/ask` does not accept identity claims.
The server bounds request bodies, checks Host/Origin, uses no CORS, and returns
fixed public errors. All displayed data is explicitly synthetic.

Tests cover own rows, another customer's rows, another tenant, masking, aggregate
results, raw-field requests, identity claims, unknown tools/SQL-like input,
revocation, denied evidence, tampered receipts, cross-user/cross-call replay,
same-ticket replay, expiry, execution-mode off, and zero SELECTs on rejection.
Expectations are literal fixture rows/totals, not values computed by the
authorizer under test. HTTP tests exercise session binding and bounded parsing.
Real-model integration is a later separately measured test mode.
