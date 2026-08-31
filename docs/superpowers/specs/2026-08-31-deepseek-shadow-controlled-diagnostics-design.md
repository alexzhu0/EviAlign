# DeepSeek Shadow Controlled Diagnostics Design

**Date:** 2026-08-31

**Status:** Approved for planning

**AgentHarness repository impact:** design and plan documents only

**External runtime:** `deepseek-harness-shadow`, branch
`agentharness-shadow-poc`, baseline
`bd8691b78dc5d91f2420412a7d24dc4dc02cf8d1`

## Context

The locked DeepSeek shadow runtime passed its offline suites, type checks,
documentation gates, lint, and independent security review. Its one authorized
live attempt returned only the existing bounded failure
`shadow.live_failed`. The no-retry contract was honored, so no second request,
alternate model, raw provider inspection, or follow-up network activity
occurred.

The current public failure is intentionally non-disclosing, but it cannot
distinguish a descriptor/request problem from credential input, runtime boot,
provider transport, provider protocol, model contract, or cleanup/output. This
design adds a separately invoked, bounded diagnostic surface without weakening
the existing launcher or changing AgentHarness evidence semantics.

## Goals

- Preserve the existing zero-argument `live-launch.ts` behavior exactly.
- Add a separate zero-argument diagnostic entrypoint.
- Use the same descriptor parsing, locked runtime, adapter, one-request counter,
  model configuration, tool registry, observation builder, and lifecycle for
  both entrypoints.
- Expose only one of seven fixed diagnostic stages on failure.
- Keep successful output identical to the existing bounded observation.
- Provide enough stage-level evidence to design the next root-cause
  investigation without exposing sensitive or provider-controlled material.
- Complete implementation, fake-SSE verification, and independent review
  without reading `.env`, using a real credential, accessing a provider, or
  making a network request.

## Non-goals

- This design does not authorize a second live call.
- It does not add retries, alternate models, provider routes, profiles,
  overlays, settings, credential services, logging, tracing, telemetry, or raw
  diagnostics.
- It does not make diagnostic failures AgentHarness evidence.
- It does not change `allow_candidate`, grant execution permission, or alter
  `execution_attempted:false` / `result_status:"not_executed"`.
- It does not add an AgentHarness command, schema, verifier rule, or product
  source change.
- It does not expose HTTP status, exception type/text, response body, prompt,
  tool arguments, request challenge, paths, environment fields, or key data.

## Chosen architecture

The implementation uses one shared execution chain with typed internal stage
errors. It rejects two alternatives:

- An external phase tracker cannot reliably distinguish provider protocol from
  model-contract failures.
- A copied diagnostic execution path can drift from the reviewed one-request
  runtime and create a second provider surface.

The external runtime gains an internal diagnostics module containing only:

- the closed diagnostic-stage union;
- a `ShadowDiagnosticError` that stores only a stage and has no cause;
- helpers that wrap an unknown failure at a known phase without reading or
  matching its message; and
- a deterministic bounded serializer for the public diagnostic document.

Descriptor and preflight processing are extracted into one shared component.
The live execution and observation construction are extracted into one shared
component. The existing launcher and the diagnostic launcher are thin format
adapters over those components:

- the existing launcher maps every failure to exact
  `ERROR: shadow.live_failed\n`;
- the diagnostic launcher emits one fixed stage document on stderr;
- both write the same observation plus newline to stdout on success.

Neither launcher accepts arguments, a transport replacement, a model, a route,
an attempt count, a diagnostic toggle, or an injected provider response. The
diagnostic entrypoint is separate rather than environment-controlled so
ambient state cannot change disclosure behavior.

## Data flow

The shared flow advances monotonically through these boundaries:

```text
request_preflight
  -> credential_input
  -> runtime_boot
  -> provider_transport / provider_protocol
  -> model_contract
  -> cleanup_output
```

1. The launcher validates zero arguments, the external-runtime working
   directory, local marker conflicts, and absence of an external `.env`.
2. Descriptor 0 is read with the existing 4,096-byte bound, fatal UTF-8
   decoding, duplicate-aware JSON parsing, exact request validation, and
   freshness validation.
3. Descriptor 3 is read with the existing 8,192-byte bound, parsed as exactly
   one literal `DEEPSEEK_API_KEY` assignment, and copied into the existing fresh
   environment allowlist.
4. The same locked runtime boots with the same direct composition and exact
   one-tool registry.
5. The same DeepSeek Flash adapter performs at most one request with redirects
   refused, no retry plugin, thinking disabled, 256 maximum output tokens, a
   60-second idle timeout, and the 65,536-byte aggregate response bound.
6. A successfully decoded turn must meet the existing exact tool-call,
   argument-binding, finish, result, and completed-turn contract.
7. The same observation builder emits only non-executing evidence. Runtime
   disposal completes before success is returned.

## Diagnostic stages

The stage set is closed and exact:

- `request_preflight`: argument count, working-directory/marker checks,
  descriptor 0 reads, request UTF-8/JSON/duplicate/schema validation, and
  freshness.
- `credential_input`: descriptor 3 reads, credential-source UTF-8, the literal
  one-assignment parser, and construction of the fresh environment allowlist.
- `runtime_boot`: Cordis composition, provider registration, exact tool
  registry validation, and session/agent creation before provider transport.
- `provider_transport`: request serialization and fetch, redirect refusal,
  connection/timeout failure, non-success HTTP response, and response-byte
  overflow.
- `provider_protocol`: malformed or incomplete SSE/JSON, abnormal stream end,
  missing `[DONE]`, or another inability to decode the provider stream into a
  complete typed response.
- `model_contract`: a decoded response that violates the exact no-text,
  one-tool, duplicate-free arguments, request binding, finish, result, step,
  turn, or completion contract.
- `cleanup_output`: runtime disposal, observation construction,
  canonicalization, or output byte-limit failure.

Classification uses only a known current phase or a closed internal error/code
mapping. It must never inspect exception messages, enumerable attacker-owned
properties, stack traces, or causes. A failure whose lower-level category is
not recognized is assigned to the narrowest active phase. No new stage is
created at runtime.

Before the first provider request, a `runtime_boot` failure must prove the
request count remained zero. Inside the adapter wrapper, known transport and
protocol codes map to their respective stages. Exact-binding failures raised
after decoding a tool-call block map to `model_contract`. The completed
transcript predicate also maps only to `model_contract`.

## Public output contracts

The existing launcher remains byte-for-byte compatible:

```text
ERROR: shadow.live_failed
```

On diagnostic failure, stdout is empty and stderr is exactly one compact ASCII
JSON object plus newline:

```json
{"code":"shadow.diagnostic_failed","stage":"provider_transport"}
```

The document has exactly the two fields `code` and `stage`, in that order, and
must be at most 128 UTF-8 bytes including its newline. It contains no optional
detail. A formatting failure produces the constant cleanup document:

```json
{"code":"shadow.diagnostic_failed","stage":"cleanup_output"}
```

On success, both entrypoints write exactly the same bounded canonical
`runtime-shadow-observation-v1` document plus one newline to stdout and write
nothing to stderr. Only that success document can be passed to AgentHarness
`shadow verify`.

## Repository and authorization boundary

All runtime implementation, tests, paired documentation, and translation
records belong to the external `deepseek-harness-shadow` repository and form a
separate commit/review unit. AgentHarness receives only this design and its
implementation plan; no AgentHarness product source, CLI, schema, or verifier
changes are allowed.

Diagnostic JSON is operator information, not evidence. AgentHarness does not
parse, store, verify, or authorize from it. A diagnostic stage cannot mean
PASS, `allow_candidate`, execution permission, deployment readiness, or
production certification.

This implementation phase is offline-only. Reading the protected `.env`,
opening network access, or executing either live entrypoint with a real key is
outside its authorization. After implementation, all offline gates and an
independent security review must pass. A later live diagnostic attempt requires
a new explicit authorization and remains one request with no retry.

## Test design

All behavior changes follow strict RED/GREEN TDD using fake fetch/SSE and fake
credentials only. Tests derive expected documents and stages from literals,
not the formatter under test.

Focused coverage must prove:

- every one of the seven stages is distinguishable;
- request-preflight, credential-input, and runtime-boot failures perform zero
  fetch calls;
- provider-transport, provider-protocol, and model-contract failures perform
  exactly one fetch call and cannot request a second model round;
- cleanup/output failure cannot turn a failed run into evidence;
- the existing launcher still emits exact `ERROR: shadow.live_failed\n` with
  empty stdout for every stage;
- the diagnostic launcher emits empty stdout and the exact two-field JSON line
  for every stage;
- both launchers produce byte-identical successful observations;
- neither entrypoint accepts arguments, a route, a transport, a model, an
  attempt override, or ambient diagnostic configuration;
- injected fake keys, absolute paths, provider bodies, raw arguments,
  exception text, control characters, and hostile objects are absent from all
  output and causes;
- oversize, malformed UTF-8, duplicate JSON members, redirect, timeout,
  response overflow, missing `[DONE]`, wrong tool, changed/extra arguments,
  text output, bad finish/result/turn, boot failure, disposal failure, and
  serialization failure each land at the specified boundary; and
- success retains `execution_attempted:false` and
  `result_status:"not_executed"`.

Regression gates include the complete shadow suite, directly affected
DeepSeek adapter/SSE suites, both affected TypeScript type checks, translation
pairing, `doc-sync`, lint, static credential/path/route/logging scans, Git
whitespace checks, exact staged-path review, and a clean external checkout.
The existing AgentHarness required verification suite is also rerun to prove
the repositories remain separated and evidence behavior is unchanged.

## Documentation and operator flow

The English and Chinese external-runtime documentation will name the separate
zero-argument diagnostic command, its descriptor inputs, its seven fixed
stages, and its non-evidence meaning. It will state that the current live
launcher remains the normal acceptance command and continues to reveal only
`shadow.live_failed`.

The offline implementation report records RED/GREEN evidence and bounded gate
totals only. It contains no key, request challenge, observation, provider
response, host path, or external error text. The independent review verifies
the error mapping, one-request boundary, output determinism, redaction, and
absence of an injectable production success path.

After review, work stops. The operator may then decide whether to authorize one
new live diagnostic attempt. Failure of that later attempt is reported only by
its fixed stage and is not retried. Success is verified through the unchanged
AgentHarness observation path and remains `not_executed` candidate evidence.

## Acceptance criteria

The design is satisfied when:

1. the existing launcher is byte-for-byte backward compatible;
2. a separate zero-argument diagnostic launcher uses the same one-request
   execution chain;
3. every failure produces exactly one approved stage without untrusted detail;
4. every stage has discriminating fake-SSE or preflight coverage;
5. successful observations are identical across entrypoints and remain
   non-executing;
6. complete offline verification and independent review have no open Critical
   or Important findings; and
7. no `.env`, credential, provider, model, network, or API access occurs during
   implementation or verification.
