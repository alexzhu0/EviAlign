# Business action evidence v1

`agentharness.business_action_evidence_v1` is a pure pre-execution correlation
contract for the separate synthetic business sandbox. It performs no database,
filesystem, network, authorization, signing, or tool execution operation. Its
reports and receipts always say `result_status: not_executed`.

## Python interface

- `canonical_digest(value)` returns SHA-256 of sorted, compact ASCII JSON
  (`ensure_ascii=True`, no nonfinite numbers). Invalid input raises a fixed
  `ValueError('business_action.json_invalid')`.
- `build_evidence(request)` returns an unsigned receipt. Invalid requests raise
  a fixed `ValueError('business_action.request_invalid')`.
- `verify_business_action_evidence_v1(request, evidence, *, now: int)` returns
  exactly `kind`, `ok`, `code`, and `result_status`. Kind is
  `business-action-verification-v1`. Codes are `business_action.ok`,
  `request_invalid`, `request_expired`, `evidence_invalid`, `binding_invalid`,
  `policy_denied`, or `internal_error`, each with the `business_action.` prefix.
  Only `business_action.ok` sets `ok: true`.

## Exact envelopes

Request keys are exactly `kind`, `request_id`, `challenge`, `issued_at`,
`expires_at`, `context`, `proposal`, `authorization`, `resources`, `approval`,
and `result_status`. Kind is `business-action-request-v1`; request ID is 32
lowercase hexadecimal characters; challenge is 64 lowercase hexadecimal
characters. Times are nonnegative integers at most 2^63−1, with expiry exactly
300 seconds after issuance. Verification requires `issued_at <= now < expires_at`.
Booleans are not integers for these fields.

Context keys are exactly `actor`, `tenant`, `role`, `auth_version`,
`policy_version`, and `world_id`. Names have 1–64 ASCII alphanumeric, underscore,
or hyphen characters, starting alphanumeric; versions are positive integers at
most 2^63−1. Proposal keys are exactly `tool` and `args`, with a JSON map for args.
Authorization keys are exactly `decision` (`permit` or `deny`) and `reason`
(a bounded name). Resources and approval are bounded JSON maps.

Finite tools: `search_customers`, `list_orders`, `order_detail`, `list_shipments`,
`list_tickets`, `finance_summary`, `search_documents`, `list_events`,
`list_refund_requests`, `create_ticket`, `assign_ticket`, `request_refund`,
and `approve_refund`. Tool argument business schemas belong to the runtime.

Receipt keys are exactly `kind` (`business-action-evidence-v1`), `request_id`,
`challenge`, `result_status`, `request_digest`, `context_digest`,
`proposal_digest`, `authorization_digest`, `resources_digest`, and
`approval_digest`. Each digest is 64 lowercase hexadecimal characters. The
request digest binds the complete envelope, including request identity, time,
actor, tenant, versions, tool arguments, resource state, and approval references.
Every receipt field must match the receipt derived from the current request.

## Bounds and CLI

All values must be plain JSON types. Objects and arrays have at most 64 entries,
object keys at most 64 characters, maximum depth 12, maximum 2,048 visited nodes,
and maximum 16 KiB canonical ASCII JSON. Integers have at most 63 magnitude bits;
floats must be finite. Containers with cycles, custom Python objects and oversized
values are rejected. No paths or links are followed.

`PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m agentharness.business_action_evidence_v1`
reads exactly one UTF-8 JSON envelope containing only `request` and `evidence`.
The entire CLI envelope also has a 16 KiB raw and canonical bound. Duplicate keys
at every depth, invalid Unicode, nonfinite constants and trailing documents are
rejected. It emits one bounded deterministic JSON report with no supplied
identifiers, arguments, exception text or host paths; exit status is 0 for
matching permit evidence, otherwise 2. CLI freshness uses the system clock;
Python callers pass an explicit trusted clock.

## Trust and execution boundary

Digest equality is neither authentication nor authorization. A caller able to
replace the trusted request and receipt can recompute both. The external runtime
must retain the original request, trusted identity and freshly authorized tool
proposal, recheck current resources and approvals before committing, and own
execution and idempotency. Approval expiry, requester/approver separation,
resource-version freshness and policy semantics are bound as supplied but are
validated by the runtime. A denied request cannot produce positive verification.

New request IDs and challenges reject cross-call replay. Same-request replay is
outside this stateless v1 contract. Successful evidence verification does not
establish production readiness or grant runtime authorization. Existing data
access and Pi contracts remain separate and unchanged.
