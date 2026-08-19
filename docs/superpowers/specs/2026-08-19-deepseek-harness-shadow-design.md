# DeepSeek Harness Shadow Integration Design

Date: 2026-08-19

## Status

Approved design for a local-only DeepSeek Harness shadow integration. This
document authorizes design and later separately reviewed implementation work;
it does not authorize AgentHarness to execute an external tool or grant runtime
permission.

## Goal

Run a tightly bounded, real `deepseek-v4-flash` model request through the
official DeepSeek Harness, capture one synthetic tool-call intent, and verify
the resulting observation against AgentHarness evidence without executing a
tool.

## Scope and repository ownership

The implementation has two separately versioned, committed, reviewed, and
released units:

1. An external checkout of
   [`deepseek-ai/deepseek-harness`](https://github.com/deepseek-ai/deepseek-harness),
   pinned to a reviewed commit, owns the custom no-side-effect plugin/preset and
   local PoC launcher.
2. AgentHarness owns the generic shadow request/observation contract, bounded
   verifier, fixtures, adversarial tests, and user-facing boundary
   documentation.

Neither repository vendors the other or infers permission from its output. The
official Harness is in developer preview and permits compatibility-breaking
changes, so the external integration must pin the exact source revision. The
DeepSeek API model identifier is exactly `deepseek-v4-flash`.

## Architecture and boundary

```text
AgentHarness shadow request
        |
        v
independent DeepSeek Harness checkout (pinned revision)
        |
        v
no-side-effect custom preset + inspect_policy_summary synthetic tool
        |
        v
interceptor writes bounded runtime-shadow observation
        |
        v
AgentHarness verifier -> deterministic verification report
```

The external Harness must not load AgentHarness as a writable workspace and must
not expose shell, filesystem, network, delegation, or real business tools. Its
only model-visible tool is `inspect_policy_summary`. The tool interceptor does
not call an adapter, open a file, dispatch a task, or perform an external
operation. It records the model's request and returns only a deterministic
`shadow_observed` response.

All AgentHarness outputs remain pre-execution evidence. In particular,
`allow_candidate` is candidate evidence only and must never be converted into a
runtime allow, while every current shadow object and verification report uses
`result_status: "not_executed"`.

## Request and observation contract

AgentHarness introduces two bounded JSON documents. `runtime_id` is exactly
`deepseek-harness`; the pinned revision is exactly a 40-character lowercase Git
commit SHA; every document is UTF-8 JSON with no duplicate keys.

- `shadow-request-v1`: at most 4 KiB, containing a 1–64 character ASCII
  `request_id`, a 64-character lowercase-hex 256-bit per-request `challenge`,
  RFC 3339 issue/expiry instants no more than five minutes apart, allowed
  runtime identifier, exact model identifier, exact synthetic tool name, and a
  64-character lowercase-hex digest of the canonical tool schema.
- `runtime-shadow-observation-v1`: an external-runtime observation containing
  at most 8 KiB, the matching request and challenge identifiers, pinned runtime
  revision, exact model and tool names, a 1–128 character opaque correlation
  ID, canonical arguments limited to exactly `challenge` and
  `policy_scope: "agentharness-shadow-poc"`, their 64-character lowercase-hex
  digest, and the fixed execution fields `execution_attempted: false` and
  `result_status: "not_executed"`.

The model receives the challenge only as the required value for the synthetic
tool's call arguments. AgentHarness verifies exact current-call binding:
request ID, unexpired challenge, runtime/model/tool identifiers, schema digest,
argument digest, and correlation ID must agree. This rejects cross-request
response replay. Detecting a byte-identical response replayed against the same
unexpired request requires durable caller-side state and is outside v1. A valid
observation shows only that a real model generated a constrained tool-call
intent; it conveys no execution approval.

## Fail-closed behavior

The verifier rejects, with stable bounded reason codes, an observation that is
malformed, ambiguous, oversized, expired, cross-request-replayed, changed,
linked to another request, or contains an unsupported runtime/model/tool. It also rejects missing
or duplicated tool calls, extra tool calls, a non-JSON payload, an unexpected
field, an absolute path, or a key named `api_key`, `authorization`, `token`,
`secret`, `prompt`, `response`, `path`, `cwd`, or `workspace`. Any string
matching the API-key prefix `sk-` is rejected. Any status other than
`not_executed` / `execution_attempted: false` is rejected.

The external interceptor must abort before recording success when the model
requests a different tool, omits or changes the challenge, attempts more than
one tool call, or exceeds the configured bounds. It must never fall back to a
default tool or re-run the request automatically.

## Real-run safeguards

The local PoC uses exactly `deepseek-v4-flash`, with thinking disabled, a
maximum of three model requests, a maximum of 256 output tokens per request,
and one synthetic tool. It is never a GitHub Actions job, scheduled task, or
production runtime.

`DEEPSEEK_API_KEY` is supplied only to the external Harness child process. The
local `.env` source is Git-ignored and owner-readable only; its value is never
printed, persisted in a fixture, placed in CI, or copied into an observation,
report, test, or command line. The launcher accepts only the key assignment it
needs and fails closed if it is missing or malformed.

The observation/report stores only bounded metadata, digests, and redacted
argument summaries. It never contains an API key, raw model response, raw
prompt, credential-like value, or absolute host path.

## Testing and acceptance

Both repositories require offline automated coverage before a paid run:

- AgentHarness tests valid binding plus adversarial changes to challenge,
  expiry, request binding, runtime/model/tool, duplicate/extra call, oversized
  fields, status, raw text, path, and credential-like values.
- The external Harness plugin/preset tests that its tool catalog contains only
  the synthetic tool, its interceptor never invokes a real adapter, and each
  invalid model call fails without producing an accepted observation.

The one real local acceptance run succeeds only when it uses the pinned
Harness revision and Flash model, records one bounded synthetic tool call, and
AgentHarness verifies it while preserving `result_status: "not_executed"`.
Any API/provider failure, timeout, output-bound violation, verification failure,
or unexpected tool behavior is a failed PoC, not a retry or a partial pass.

## Non-goals

This work does not enable filesystem, shell, network, MCP, delegated, or
business-tool execution; modify DeepSeek Harness upstream; add a GitHub CI API
call; publish credentials; authorize a runtime; or claim production safety.
Any future execution path requires a separate external-runtime design,
implementation, adversarial test suite, and explicit approval gate.
