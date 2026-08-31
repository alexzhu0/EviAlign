# DeepSeek Shadow Live Driver Design

Date: 2026-08-31

## Status

Approved design for one manually authorized DeepSeek Flash shadow call. This
extends the locked-runtime design and does not authorize any real tool action.

## Runtime path

The external checkout owns one live driver that calls the already locked
DeepSeek adapter directly. It does not start `dsh`, load a profile, accept an
overlay, mount settings or credentials services, or expose a workspace. The
only model-visible tool is `inspect_policy_summary`.

The adapter uses exactly `deepseek-v4-flash`, thinking disabled, 256 maximum
output tokens, a 60-second stream idle timeout, and no retry plugin. The manual
acceptance command and its process hard-stop after exactly one provider request.
The acceptance campaign may contain at most three separately authorized manual
runs, but the driver does not automate, schedule, or retry those later runs.

## Credential handling

The launcher reads the protected AgentHarness `.env` only through the existing
literal one-assignment parser. It accepts exactly one `DEEPSEEK_API_KEY`, does
not source the file, and passes the value only through a closure to the adapter.
The key is absent from arguments, logs, observations, errors, fixtures, and
committed configuration. The driver rejects duplicate assignments, controls,
unexpected environment keys, an external `.env`, and an AgentHarness working
directory.

## Model-call acceptance

The prompt contains only the issued challenge and fixed policy scope needed to
request the synthetic tool. A successful response must contain exactly one
call to `inspect_policy_summary`, with arguments exactly `challenge` and
`policy_scope: "agentharness-shadow-poc"`. The synthetic tool records intent,
returns `{ "status": "shadow_observed", "executed": false }`, concludes the
turn, and never invokes an adapter, filesystem, shell, network tool, or business
operation.

Text-only output, an unexpected tool, missing/duplicate calls, changed or extra
arguments, a second model round, timeout, provider error, byte overflow, or
failed AgentHarness verification is a failed PoC. There is no automatic retry.

## Output and verification

Raw prompts, responses, reasoning, tool arguments, and provider diagnostics are
kept in bounded process memory only long enough to validate the call and are
never printed or persisted. Success emits exactly one compact
`runtime-shadow-observation-v1` document. It always contains
`execution_attempted:false` and `result_status:"not_executed"`.

The observation is written only to a Git-ignored temporary file and piped to
AgentHarness `shadow verify` with the original request. Acceptance requires
`shadow.ok` and `result_status:"not_executed"`; it conveys evidence only, never
runtime permission.

## Gates

Before the paid call, offline tests use a fake streaming adapter to prove the
exact request configuration, one-call cap, terminal synthetic-tool behavior,
redaction, and every fail-closed outcome. The implementation receives an
independent security review and passes TypeScript, focused tests, documentation
gates, and whitespace checks. The real call occurs once only after those gates
and explicit operator authorization.
