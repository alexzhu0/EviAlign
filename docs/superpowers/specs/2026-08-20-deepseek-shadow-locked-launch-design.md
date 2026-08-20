# DeepSeek Shadow Locked Launch Design

Date: 2026-08-20

## Status

Approved replacement for the external Harness launch path. It refines the
approved shadow-integration design; it does not authorize tool execution.

## Decision

The external PoC does not boot stock `dsh`, any `dsh` profile, the headless
bundle, or a profile/home/caller patch layer. Its launcher composes a minimal
Cordis application directly from pinned source and exposes one model-visible
tool, `inspect_policy_summary`.

## Composition

The locked launcher mounts only the services necessary for one bounded model
turn: tool registry, system prompt, DeepSeek adapter, direct agent/agent-loop
driver, and the local synthetic-tool plugin. It disables or omits filesystem,
shell, subprocess, jobs, web, skills, MCP, delegation, workflow, todo, goal,
code runtime, session title, compaction, retry, settings, credentials, and
all other provider routes. It does not parse profile manifests or accept a
profile name, a patch path, a workspace path, or arbitrary child arguments.

The one allowed session dependency is an in-memory `SessionStore` required by
the pinned `AgentLoop`; session persistence plugins remain forbidden.

The DeepSeek adapter is configured in code with only `deepseek-v4-flash`,
`thinking: disabled`, `maxTokens: 256`, a 60-second idle timeout, and no retry
policy. The launcher allows at most one provider call in the first acceptance
run and an absolute process cap of three across a manually supplied run count.

## Credential and environment isolation

Before boot, a local parser obtains exactly one `DEEPSEEK_API_KEY` assignment
from the protected AgentHarness `.env`; it never sources that file. The child
environment is constructed from that value plus `PATH`, required locale values,
and `DSH_TELEMETRY_DISABLED=1`. No `.env`, credentials file, settings file,
or inherited provider configuration is mounted or read. The launcher refuses
an AgentHarness working directory, external `.env`, or external DSH home.

## Evidence

The synthetic tool accepts exactly the issued challenge and fixed policy scope,
captures no transcript, performs no operation, and returns only
`{ "status": "shadow_observed", "executed": false }`. The launcher emits one
bounded observation with `execution_attempted:false` and
`result_status:"not_executed"`; raw prompt, response, API key, host path, and
tool arguments never leave the external process. AgentHarness independently
verifies the observation.

## Acceptance gates

Offline tests prove the direct composition has exactly one registered tool and
no prohibited service/tool registrations; adversarial tests prove overlays and
extra provider/tool requests cannot be supplied because the launcher has no
such input surface. The single paid run occurs only after these tests and a
separate review pass. Provider failure, timeout, unexpected output, or failed
AgentHarness verification is a failed PoC and is never retried automatically.
