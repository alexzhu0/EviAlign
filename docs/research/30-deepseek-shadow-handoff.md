# DeepSeek Shadow Handoff and Runbook

Updated: 2026-09-09

## Start here

AgentHarness issues and verifies bounded evidence locally. The separate
`deepseek-harness-shadow` repository calls the model and exposes exactly one
synthetic tool, `inspect_policy_summary`. Its successful result is fixed and
does not execute a business operation. Keep `result_status: not_executed` and
`execution_attempted: false`; `allow_candidate` is never runtime permission.

Checkpoints before this documentation maintenance:

| Repository | Local branch | Verified source revision |
| --- | --- | --- |
| AgentHarness | `main` | `24340266b9a1e9345e701ec164e0663aae472893` |
| deepseek-harness-shadow | `agentharness-shadow-poc` | `946ba919a1c8a343821ba224aafe698359231fac` |

The external revision contains the descriptor-launch fix, locally fast-forwarded
from `fix/shadow-launch-fd3`. Each repository remains a separate review, commit,
and release unit. At maintenance start, AgentHarness was 14 commits ahead of its
local `origin/main` tracking ref; no remote refresh was performed. This is not a
claim about the current remote server. The pre-existing untracked
`.understand-anything/` directory is outside this maintenance scope.

## Observed acceptance

On 2026-09-09, the operator updated the project credential. After synchronizing
the separately configured shadow credential file, a read-only request to the
official model-list endpoint returned HTTP 200 and exposed `deepseek-v4-flash`.
One subsequent model request exited successfully; verification of its original
request and returned observation produced:

```json
{"code":"shadow.ok","kind":"shadow.verification.v1","model":"deepseek-v4-flash","ok":true,"request_id":"shadow-fd3-live-check","result_status":"not_executed","runtime_id":"deepseek-harness","tool_name":"inspect_policy_summary"}
```

This is a transcription of the session's sanitized verifier output, not a
replayable evidence bundle. Request and observation files were temporary local
artifacts and are not committed here. The original request has a five-minute
validity window; historical success must not be reused as fresh evidence.
No availability, latency, business-tool, or production acceptance claim follows
from this single live sample.

The subsequent offline acceptance passed 158 external shadow tests and 515
AgentHarness tests, plus shadow type checking, policy validation, three smoke
evaluations, both required loop checks, and Git whitespace checks. External
document pairing, doc-sync (28 gates), and lint also passed during the preceding
merge verification; those are historical results, not new maintenance runs.

## Credential and launch procedure

The project `.env` and the operator's dedicated shadow credential file are
separate files. Updating the project file does not automatically update the
shadow file. The configured operator location in this setup is
`~/.config/agentharness/deepseek-shadow.env`. Keep it outside Git with mode
`0600`; its content must be exactly one literal, unquoted assignment named
`DEEPSEEK_API_KEY`, optionally followed by one newline. Never source the file,
print its contents, or paste a key into a report. Confirm the intended file when
rotating credentials; no automatic synchronization is implemented.

After operator authorization for a real call and the required offline review,
use an operator-owned private temporary directory for the request and output
files. Set `SHADOW_REQUEST_FILE`, `SHADOW_OBSERVATION_FILE`,
`SHADOW_DIAGNOSTIC_FILE`, and `AGENTHARNESS_ENV_FILE` to absolute file paths
so they resolve consistently when switching repositories;
set `SHADOW_RUNTIME_REVISION` to the external checkout's current full Git SHA.
Use a restrictive file-creation mask such as `umask 077`. From AgentHarness:

```sh
PYTHONDONTWRITEBYTECODE=1 ./agentharness shadow issue \
  --request-id shadow-acceptance-001 \
  --runtime-revision "$SHADOW_RUNTIME_REVISION" > "$SHADOW_REQUEST_FILE"
```

Within five minutes, run from the external checkout, which must not contain its
own `.env`:

```sh
node --import tsx/esm shadow-plugin/src/diagnostic-launch.ts \
  3< "$AGENTHARNESS_ENV_FILE" \
  < "$SHADOW_REQUEST_FILE" \
  > "$SHADOW_OBSERVATION_FILE" \
  2> "$SHADOW_DIAGNOSTIC_FILE"
```

Start Node directly. `pnpm exec tsx` does not preserve descriptor 3 in this
environment and previously caused `credential_input` before any provider call.
The launcher allows one provider request and no retry. On failure, inspect only
the bounded diagnostic; investigate before another authorized attempt. On
success, immediately run from AgentHarness with the unchanged original request:

```sh
PYTHONDONTWRITEBYTECODE=1 ./agentharness shadow verify \
  "$SHADOW_REQUEST_FILE" < "$SHADOW_OBSERVATION_FILE"
```

Keep only reviewed, sanitized summaries in source control. A verifier success
is candidate evidence and does not authorize subsequent tool execution.

## Failure interpretation

| Observation | Meaning and next check |
| --- | --- |
| `request_preflight` | Check request format, freshness, descriptor inputs, and working directory. |
| `credential_input` | Check the exact credential file and descriptor 3; this alone is not proof that the remote service rejected the key. |
| `provider_transport` | Broad adapter failure bucket, including HTTP authentication and quota failures as well as connection failures. |
| `provider_protocol` or `model_contract` | Provider response or model tool call did not meet the fixed contract; no valid observation should be accepted. |
| `runtime_boot` or `cleanup_output` | Local lifecycle/output failure; withhold evidence and diagnose locally. |

The earlier old-key check returned HTTP 401 from the official `/models`
endpoint. The updated key returned 200. The diagnostic stage alone could not
distinguish them: the adapter maps HTTP 401/403 to `AUTH`, which the current
shadow classifier groups under `provider_transport`. A future refinement needs
a reviewed diagnostic-contract change, not exposure of raw provider messages.

For network diagnosis, compare the actual Node runtime with the intended
execution environment. A sandboxed Node probe previously returned `EAI_AGAIN`,
while the authorized host probe connected successfully. A curl result by itself
does not establish that the application's Node process can connect.

## Next development work

Choose one concrete business proposal to observe and define its evidence and
expected accept/reject cases. The current fixed tool is not a general business
adapter, and input binding alone does not establish business-policy correctness.
Use the repository's Superpowers design and implementation workflow before
adding behavior. Then test the new shadow path with simulated adversarial cases
and a bounded live sample.

Actual business execution requires a separate external-runtime design,
implementation, adversarial tests, and approval gate. Until then the accepted
milestone is the fixed synthetic evidence path only. Public release,
package publication, and deployment are separate outstanding decisions.

## GitHub source synchronization follow-up

After documentation commit `379fa8b`, the user authorized maintaining and
pushing the latest AgentHarness source to GitHub. Fetching `origin` confirmed
that local `main` was 15 commits ahead and zero behind; a normal fast-forward
push can include that history. The target is `alexzhu0/AgentHarness`, branch
`main`. Verify the remote commit and its CI result after pushing; this
pre-push record does not itself prove remote synchronization.

This follow-up authorizes the AgentHarness source push only. The external
runtime checkpoint and locally installed `project-maintainer` skill remain
separate artifacts. The existing prerelease tag and package version stay
unchanged; no new hosted release or package publication is requested.
