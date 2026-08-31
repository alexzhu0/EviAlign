# DeepSeek Shadow Live Driver Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Install a genuine, one-request DeepSeek Flash driver in the external locked runtime, produce one non-executing observation only from the model's actual synthetic-tool call, and verify it with AgentHarness.

**Architecture:** The external `deepseek-harness-shadow` checkout keeps its direct Cordis composition and drives one programmatic AgentLoop turn through the pinned DeepSeek adapter. The registered synthetic tool captures the model-issued arguments and concludes the turn; only `runShadow()` may turn that live capture into a verifier-compatible observation. A descriptor-based launcher reads the request from stdin and the literal key source from file descriptor 3, so neither the key nor host paths become command arguments or output.

**Tech Stack:** TypeScript 6, Node.js 22, Cordis, pinned DeepSeek Harness packages, Vitest, DeepSeek streaming chat-completions adapter, Python AgentHarness verifier.

**Spec:** `docs/superpowers/specs/2026-08-31-deepseek-shadow-live-driver-design.md`

## Global Constraints

- Implement Tasks 1-3 from the external `deepseek-harness-shadow` repository root; commit them there and never combine them with an AgentHarness commit.
- Keep AgentHarness a pre-execution evidence control-plane. `allow_candidate` is evidence only, `execution_attempted` remains `false`, and `result_status` remains `not_executed`.
- Use exactly provider `deepseek-official`, model `deepseek-v4-flash`, `thinking: { type: "disabled" }`, `max_tokens: 256`, a 60,000 ms stream idle timeout, and no retry plugin.
- The acceptance process permits exactly one provider request. Any further manual campaign run requires a new explicit authorization and the whole campaign is capped at three separately authorized runs.
- Expose only `inspect_policy_summary`; its exact arguments are `challenge` and `policy_scope: "agentharness-shadow-poc"`. It performs no external action and calls `concludeTurn()`.
- Never load `dsh`, a profile, an overlay, settings, credentials, a workspace, persistence, telemetry, or an arbitrary provider route. The already approved in-memory `SessionStore` remains the only session dependency.
- Never print, persist, fixture, or return an API key, raw prompt, raw provider response, reasoning content, raw tool arguments, provider diagnostics, exception text, or an absolute host path.
- Production code must not expose a request-plus-synthetic-call success seam. Offline tests fake provider transport with `globalThis.fetch`; they do not inject a completed call into production APIs.
- Parse the key as exactly one literal `DEEPSEEK_API_KEY=...` assignment. Do not source or evaluate `.env`.
- Stage explicit paths only. Before each external commit, inspect `git diff --cached --name-only` and run `git diff --cached --check`.

---

## File Structure

External `deepseek-harness-shadow` checkout:

- Modify `shadow-plugin/src/locked-runtime.ts`: own the one-request adapter counter, fixed prompt, AgentLoop turn, live tool capture, and terminal-event validation.
- Modify `shadow-plugin/src/run-shadow.ts`: replace `shadow.provider_unavailable` with the genuine driver and privately construct the bounded observation.
- Create `shadow-plugin/src/live-launch.ts`: bounded stdin/fd-3 launcher with stable error output and no path-bearing arguments.
- Modify `shadow-plugin/tests/locked-runtime.spec.ts`: prove one exact wire request and terminal live capture through a fake DeepSeek SSE response.
- Modify `shadow-plugin/tests/run-shadow.spec.ts`: prove only genuine provider capture can produce an observation and every adversarial response fails closed without retry.
- Create `shadow-plugin/tests/live-launch.spec.ts`: prove descriptor input, output bounds, preflight order, redaction, and no provider call on invalid input.
- Modify `shadow-plugin/tests/live-policy.spec.ts`: retain the attempts-before-input-access guarantee after the driver becomes available.
- Modify `shadow-plugin/README.md` and `shadow-plugin/README.zh.md`: document the offline command, descriptor-based authorized command, and evidence-only result.
- Modify `.agents/notes/implemented/feature/2026-08-20-locked-agentharness-shadow-runtime.md`, its `.zh.md` pair, and `.i18n.yaml`: replace the unavailable-driver decision with the authorized one-request driver decision.

AgentHarness checkout:

- No product source changes. Task 4 uses the existing `shadow issue` and `shadow verify` commands and records only bounded command results in the task report.

---

### Task 1: Drive One Genuine Locked AgentLoop Turn

**Files:**
- Modify: `shadow-plugin/src/locked-runtime.ts`
- Modify: `shadow-plugin/tests/locked-runtime.spec.ts`

**Interfaces:**
- Consumes: `ShadowRequest`, the existing locked adapter configuration, `createUserMessage()`, `SessionId()`, and the registered `inspect_policy_summary` tool.
- Produces: `LockedTurnEvidence` and `LockedRuntime.runOneModelTurn(): Promise<LockedTurnEvidence>`; the method accepts no prompt, call, adapter, fetch, route, or observation input.

- [ ] **Step 1: Add the failing successful-wire test**

Add a helper that returns a DeepSeek-compatible SSE `Response` containing only one tool call:

```ts
function toolCallResponse(request: ShadowRequest): Response {
  const args = JSON.stringify({
    challenge: request.challenge,
    policy_scope: request.policy_scope,
  })
  const events = [
    { choices: [{ delta: { role: 'assistant' } }] },
    { choices: [{ delta: { tool_calls: [{
      index: 0,
      id: 'call_shadow_1',
      type: 'function',
      function: { name: 'inspect_policy_summary', arguments: args },
    }] } }] },
    { choices: [{ delta: {}, finish_reason: 'tool_calls' }], usage: {
      prompt_tokens: 64,
      completion_tokens: 16,
    } },
  ]
  return new Response(`${events.map(event => `data: ${JSON.stringify(event)}\n\n`).join('')}data: [DONE]\n\n`, {
    status: 200,
    headers: { 'content-type': 'text/event-stream' },
  })
}

it('performs one exact Flash request and captures the live terminal tool call', async () => {
  const request = validRequest()
  const bodies: Record<string, unknown>[] = []
  vi.stubGlobal('fetch', vi.fn(async (_input, init) => {
    bodies.push(JSON.parse(String(init?.body)) as Record<string, unknown>)
    return toolCallResponse(request)
  }))
  const runtime = await bootLockedRuntime({ request, key: 'sk-test-only-not-real' })
  try {
    await expect(runtime.runOneModelTurn()).resolves.toEqual({
      arguments: { challenge: request.challenge, policy_scope: request.policy_scope },
    })
    expect(bodies).toHaveLength(1)
    expect(bodies[0]).toMatchObject({
      model: 'deepseek-v4-flash',
      max_tokens: 256,
      thinking: { type: 'disabled' },
      stream: true,
    })
    expect((bodies[0]?.tools as unknown[])).toHaveLength(1)
  } finally {
    await runtime.dispose()
    vi.unstubAllGlobals()
  }
})
```

Also assert `runtime.runOneModelTurn()` rejects a second call with only `shadow.request_limit` and that `fetch` remains at one invocation.

- [ ] **Step 2: Run the focused test to verify RED**

Run:

```bash
corepack pnpm exec vitest run shadow-plugin/tests/locked-runtime.spec.ts
```

Expected: FAIL because `runOneModelTurn` and `LockedTurnEvidence` do not exist.

- [ ] **Step 3: Add the minimal one-turn interface and provider counter**

Add these interfaces and imports in `locked-runtime.ts`:

```ts
import { createUserMessage, type GenerateOptions, type StreamChunk } from '@deepseek-ai/dsh-llm'
import { SessionId } from '@deepseek-ai/dsh-session'
import type { SyntheticToolArguments } from './observation.ts'

export interface LockedTurnEvidence {
  readonly arguments: SyntheticToolArguments
}

export interface LockedRuntime {
  runOneModelTurn(): Promise<LockedTurnEvidence>
  toolNames(): string[]
  activePluginNames(): string[]
  providerConfiguration(): LockedProviderConfiguration
  dispose(): Promise<void>
}
```

Wrap `DeepSeekAdapter.stream()` inside `lockedDeepSeekPlugin` with a closure-owned request count. Increment before the first `yield`; reject count 2 with `new LlmError('shadow.request_limit', 'REQUEST_LIMIT')`. Do not mount the retry plugin and do not accept a replacement adapter or route:

```ts
class OneRequestDeepSeekAdapter extends LlmDeepSeek.DeepSeekAdapter {
  override async *stream(options: GenerateOptions): AsyncIterable<StreamChunk> {
    if (providerRequestCount !== 0) {
      throw new LlmError('shadow.request_limit', 'REQUEST_LIMIT')
    }
    providerRequestCount += 1
    yield * super.stream(options)
  }
}
```

Build the user message internally from the immutable request snapshot:

```ts
function livePrompt(request: ShadowRequest): string {
  return [
    'Call inspect_policy_summary exactly once.',
    `Use challenge ${request.challenge}.`,
    `Use policy_scope ${request.policy_scope}.`,
    'Return no text and do not call another tool.',
  ].join(' ')
}
```

Inside `bootLockedRuntime`, capture the registered tool callback once, create one AgentLoop agent with `{ provider: 'deepseek-official', model: 'deepseek-v4-flash', maxTokens: 256 }`, send the fixed message, await `agent.whenIdle()`, and accept only when all these facts hold:

```ts
const headers = agent.session.events.filter(event => event.type === 'request/header')
const calls = agent.session.events.filter(event => event.type === 'tool/call')
const results = agent.session.events.filter(event => event.type === 'tool/result')
const ends = agent.session.events.filter(event => event.type === 'turn/end')

if (providerRequestCount !== 1
  || headers.length !== 1
  || calls.length !== 1
  || results.length !== 1
  || ends.length !== 1
  || capturedArguments === undefined) {
  throw new Error('shadow.live_failed')
}
```

Inspect the sole `assistant/message` and reject visible `text` or `reasoning` blocks. Require its only semantic block to be the exact one `tool-call`. Return a detached, frozen `{ arguments: capturedArguments }`. Consume the `runOneModelTurn` budget before any asynchronous work so a second call fails before transport.

- [ ] **Step 4: Add adversarial terminal-shape tests**

Use fake SSE responses to prove all these outcomes reject with `shadow.live_failed` and call `fetch` no more than once:

- text-only completion;
- visible text plus the matching tool call;
- unsupported tool name;
- changed challenge;
- extra argument;
- two tool calls in one response;
- provider non-2xx response;
- malformed/truncated SSE.

Keep the assertions on stable codes only. Do not assert or snapshot provider body text.

- [ ] **Step 5: Run GREEN and typecheck**

Run:

```bash
corepack pnpm exec vitest run shadow-plugin/tests/locked-runtime.spec.ts
corepack pnpm exec tsc -p shadow-plugin/tsconfig.json --noEmit
git diff --check
```

Expected: all pass; `git diff --check` prints nothing.

- [ ] **Step 6: Commit Task 1 in the external checkout**

```bash
git add -- shadow-plugin/src/locked-runtime.ts shadow-plugin/tests/locked-runtime.spec.ts
git diff --cached --name-only
git diff --cached --check
git commit -m "feat: drive one locked DeepSeek shadow turn"
```

Expected staged list: exactly the two paths above.

---

### Task 2: Build Observation Only From the Genuine Live Capture

**Files:**
- Modify: `shadow-plugin/src/run-shadow.ts`
- Modify: `shadow-plugin/tests/run-shadow.spec.ts`
- Modify: `shadow-plugin/tests/live-policy.spec.ts`

**Interfaces:**
- Consumes: `bootLockedRuntime({ request, key })`, `LockedRuntime.runOneModelTurn()`, `canonicalDigest()`, `canonicalJson()`, and `RuntimeShadowObservation`.
- Produces: unchanged production export `runShadow(request, environment, options?): Promise<RuntimeShadowObservation>`; no builder, serializer, call source, provider, or adapter becomes an additional export.

- [ ] **Step 1: Replace the unavailable-driver test with a failing live-observation test**

Stub `fetch` with the matching one-call SSE helper and assert:

```ts
it('returns one observation only after the real adapter stream reaches the registered tool', async () => {
  const request = validRequest()
  const fetchMock = vi.fn(async () => toolCallResponse(request))
  vi.stubGlobal('fetch', fetchMock)
  try {
    await expect(runShadow(request, testEnvironment())).resolves.toEqual({
      kind: 'runtime-shadow-observation-v1',
      request_id: request.request_id,
      challenge: request.challenge,
      runtime_id: 'deepseek-harness',
      runtime_revision: request.runtime_revision,
      model: 'deepseek-v4-flash',
      tool_schema_digest: request.tool_schema_digest,
      correlation_id: canonicalDigest(request),
      tool_calls: [{
        tool_name: 'inspect_policy_summary',
        arguments: { challenge: request.challenge, policy_scope: request.policy_scope },
        arguments_digest: canonicalDigest({
          challenge: request.challenge,
          policy_scope: request.policy_scope,
        }),
      }],
      execution_attempted: false,
      result_status: 'not_executed',
    })
    expect(fetchMock).toHaveBeenCalledTimes(1)
    expect(Object.keys(RunShadowModule)).toEqual(['runShadow'])
  } finally {
    vi.unstubAllGlobals()
  }
})
```

- [ ] **Step 2: Run the focused test to verify RED**

Run:

```bash
corepack pnpm exec vitest run shadow-plugin/tests/run-shadow.spec.ts shadow-plugin/tests/live-policy.spec.ts
```

Expected: FAIL with `shadow.provider_unavailable`.

- [ ] **Step 3: Implement private live observation construction**

Keep `assertSingleAttempt()` as the first operation. Snapshot request and environment before boot. Pass only `environment.DEEPSEEK_API_KEY` into `bootLockedRuntime`; do not pass the environment object or read `process.env`.

Add an unexported builder in `run-shadow.ts`:

```ts
function buildLiveObservation(
  request: ShadowRequest,
  argumentsValue: SyntheticToolArguments,
): RuntimeShadowObservation {
  const observation: RuntimeShadowObservation = Object.freeze({
    kind: 'runtime-shadow-observation-v1',
    request_id: request.request_id,
    challenge: request.challenge,
    runtime_id: request.runtime_id,
    runtime_revision: request.runtime_revision,
    model: request.model,
    tool_schema_digest: request.tool_schema_digest,
    correlation_id: canonicalDigest(request),
    tool_calls: Object.freeze([Object.freeze({
      tool_name: 'inspect_policy_summary',
      arguments: argumentsValue,
      arguments_digest: canonicalDigest(argumentsValue),
    })]),
    execution_attempted: false,
    result_status: 'not_executed',
  })
  if (Buffer.byteLength(canonicalJson(observation), 'utf8') > 8_192) {
    throw new Error('shadow.live_failed')
  }
  return observation
}
```

Implement `runShadow()` with stable disposal before returning. A disposal failure is also a failed PoC, but its exception is never exposed:

```ts
let runtime: LockedRuntime | undefined
let observation: RuntimeShadowObservation
try {
  runtime = await bootLockedRuntime({
    request: requestSnapshot,
    key: environmentSnapshot.DEEPSEEK_API_KEY,
  })
  const evidence = await runtime.runOneModelTurn()
  observation = buildLiveObservation(requestSnapshot, evidence.arguments)
} catch {
  if (runtime !== undefined) {
    try { await runtime.dispose() } catch { /* bounded public failure below */ }
  }
  throw new Error('shadow.live_failed')
}
try {
  await runtime.dispose()
} catch {
  throw new Error('shadow.live_failed')
}
return observation
```

Preserve safe preflight errors `shadow.request_limit`, `shadow.request_invalid`, and `shadow.environment_invalid`; map every post-boot provider, stream, event, callback, and disposal detail to `shadow.live_failed` without an exception cause.

- [ ] **Step 4: Add provenance and redaction regression tests**

Add tests proving:

- a `fetch` rejection containing an API key, absolute path, and provider body produces only `shadow.live_failed`;
- a matching request with a text-only or malformed response never returns an observation;
- a second requested attempt rejects before request/environment proxy access and before `fetch`;
- mutation of request/environment after the call starts cannot change the wire request or observation;
- `RuntimeShadowModule` and `ObservationModule` retain their existing export allowlists;
- cloning or casting an arbitrary request-plus-call object cannot reach a production observation builder because none is exported.

- [ ] **Step 5: Run GREEN and the complete shadow suite**

Run:

```bash
corepack pnpm exec vitest run shadow-plugin/tests/run-shadow.spec.ts shadow-plugin/tests/live-policy.spec.ts
corepack pnpm exec vitest run shadow-plugin/tests
corepack pnpm exec tsc -p shadow-plugin/tsconfig.json --noEmit
git diff --check
```

Expected: all pass; no provider network access occurs because every test stubs `globalThis.fetch` or fails before transport.

- [ ] **Step 6: Commit Task 2 in the external checkout**

```bash
git add -- shadow-plugin/src/run-shadow.ts shadow-plugin/tests/run-shadow.spec.ts shadow-plugin/tests/live-policy.spec.ts
git diff --cached --name-only
git diff --cached --check
git commit -m "feat: derive shadow evidence from live intent"
```

Expected staged list: exactly the three paths above.

---

### Task 3: Add the Descriptor-Based Manual Launcher and Documentation

**Files:**
- Create: `shadow-plugin/src/live-launch.ts`
- Create: `shadow-plugin/tests/live-launch.spec.ts`
- Modify: `shadow-plugin/README.md`
- Modify: `shadow-plugin/README.zh.md`
- Modify: `.agents/notes/implemented/feature/2026-08-20-locked-agentharness-shadow-runtime.md`
- Modify: `.agents/notes/implemented/feature/2026-08-20-locked-agentharness-shadow-runtime.zh.md`
- Modify: `.agents/notes/implemented/feature/2026-08-20-locked-agentharness-shadow-runtime.i18n.yaml`

**Interfaces:**
- Consumes: request JSON on stdin, literal key source on file descriptor 3, safe locale fields from `process.env`, `parseLiteralKeyAssignment()`, `buildChildEnvironment()`, and `runShadow()`.
- Produces: executable `corepack pnpm exec tsx shadow-plugin/src/live-launch.ts`; success writes one compact observation plus newline to stdout, while failure writes only `ERROR: shadow.live_failed` plus newline to stderr and exits 1.

- [ ] **Step 1: Write failing launcher tests**

Define `runLiveLaunch()` so tests can supply already bounded byte sources and a write sink without changing the model-call source:

```ts
export interface LiveLaunchInputs {
  readonly requestSource: Uint8Array
  readonly keySource: Uint8Array
  readonly inheritedEnvironment: Readonly<Record<string, string | undefined>>
  readonly cwd: string
  readonly externalEnvExists: boolean
}

export async function runLiveLaunch(inputs: LiveLaunchInputs): Promise<string>
```

Test a matching fake SSE response and assert the returned string is exactly `canonicalJson(observation) + '\n'`. Add preflight tests for oversized stdin, malformed JSON, a non-literal/duplicate key source, `externalEnvExists: true`, AgentHarness cwd, arguments present, and attempt count other than one. For every preflight failure, assert `fetch` is never called.

Add a subprocess-facing `main()` test that supplies a failing provider stub and verifies stdout is empty, stderr is exactly `ERROR: shadow.live_failed\n`, and stderr excludes the fake key, provider message, and cwd.

- [ ] **Step 2: Run launcher tests to verify RED**

Run:

```bash
corepack pnpm exec vitest run shadow-plugin/tests/live-launch.spec.ts
```

Expected: FAIL because `live-launch.ts` does not exist.

- [ ] **Step 3: Implement bounded descriptor input and stable output**

Use these exact limits:

```ts
const MAX_REQUEST_BYTES = 4_096
const MAX_KEY_SOURCE_BYTES = 8_192
const MAX_OBSERVATION_BYTES = 8_192
```

`runLiveLaunch()` must perform this order before `runShadow()`:

1. reject a cwd whose basename is `AgentHarness` or whose repository marker is the AgentHarness executable rather than `shadow-plugin/package.json`;
2. reject `externalEnvExists` without reading that file;
3. bound and UTF-8 decode request bytes, parse exactly one JSON value, and call `snapshotShadowRequest()`;
4. bound and UTF-8 decode fd-3 bytes, then call `parseLiteralKeyAssignment()`;
5. call `buildChildEnvironment()` and pass only its returned allowlisted object to `runShadow()`;
6. canonicalize and bound the observation, then return exactly one newline-terminated document.

The executable entrypoint accepts zero arguments, reads stdin and descriptor 3 with bounded reads, checks `lstat('.env')` without following it, and never scans parent directories. It must call `main().catch(() => { process.stdout.write(''); process.stderr.write('ERROR: shadow.live_failed\n'); process.exitCode = 1 })`. Do not attach the caught error as a cause or log it.

- [ ] **Step 4: Run launcher GREEN and static secret/path scans**

Run:

```bash
corepack pnpm exec vitest run shadow-plugin/tests/live-launch.spec.ts shadow-plugin/tests/run-shadow.spec.ts shadow-plugin/tests/live-policy.spec.ts
corepack pnpm exec tsc -p shadow-plugin/tsconfig.json --noEmit
rg -n "console\.|process\.env\.DEEPSEEK|DEEPSEEK_BASE_URL|DSH_HOME|credentials|profile|overlay" shadow-plugin/src
git diff --check
```

Expected: tests and typecheck pass. The scan shows no logging, ambient key lookup, provider-route override, credentials service, profile, or overlay path; approved comments/constants must be reviewed line by line rather than ignored.

- [ ] **Step 5: Update English and Chinese operator documentation**

Replace `shadow.provider_unavailable` language with the authorized live-driver boundary. Document this exact command shape without embedding the key or a host path in an argument:

```bash
corepack pnpm exec tsx shadow-plugin/src/live-launch.ts \
  3< "$AGENTHARNESS_ENV_FILE" \
  < "$SHADOW_REQUEST_FILE" \
  > "$SHADOW_OBSERVATION_FILE"
```

State that each variable names an operator-owned local file, `.env` is never sourced, one process makes exactly one provider request, failure is not retried, and success remains `not_executed` evidence only. Update both Agent Notes with the same decision and consequences, then refresh the translation-pair record.

- [ ] **Step 6: Run documentation and complete offline gates**

Run:

```bash
corepack pnpm run verify-translation-pairing --write .agents/notes/implemented/feature/2026-08-20-locked-agentharness-shadow-runtime.md
corepack pnpm exec vitest run shadow-plugin/tests
corepack pnpm exec tsc -p shadow-plugin/tsconfig.json --noEmit
corepack pnpm run doc-sync
corepack pnpm run lint
git diff --check
```

Expected: all pass. No real API call occurs during these gates.

- [ ] **Step 7: Commit Task 3 in the external checkout**

```bash
git add -- shadow-plugin/src/live-launch.ts shadow-plugin/tests/live-launch.spec.ts shadow-plugin/README.md shadow-plugin/README.zh.md .agents/notes/implemented/feature/2026-08-20-locked-agentharness-shadow-runtime.md .agents/notes/implemented/feature/2026-08-20-locked-agentharness-shadow-runtime.zh.md .agents/notes/implemented/feature/2026-08-20-locked-agentharness-shadow-runtime.i18n.yaml
git diff --cached --name-only
git diff --cached --check
git commit -m "feat: gate one live DeepSeek shadow call"
```

Expected staged list: exactly the seven paths above.

---

### Task 4: Independent Review, One Authorized Provider Call, and Cross-Verification

**Files:**
- Read: all Task 1-3 external diffs and reports
- Temporary: one request and one observation under a fresh `/tmp/agentharness-shadow-live.*` directory
- Modify: no tracked files unless review finds a defect; any fix returns to its owning task's TDD and review loop.

**Interfaces:**
- Consumes: clean external commits, current external HEAD SHA, AgentHarness `shadow issue`, protected AgentHarness `.env` through fd 3, the live launcher, and AgentHarness `shadow verify`.
- Produces: one verifier result with `status: PASS`, `code: shadow.ok`, and `result_status: not_executed`, or one bounded failure report with no retry.

- [ ] **Step 1: Request independent code review before any provider call**

Invoke `superpowers:requesting-code-review` over the exact Task 1-3 commit range. The reviewer must specifically inspect:

- no injectable production success path;
- one provider request before any possible second round;
- exact Flash/thinking/token/timeout configuration and no retry plugin;
- only one model-visible tool and terminal `concludeTurn()` behavior;
- exact current-request/call binding;
- stable redaction for key, paths, provider diagnostics, raw response, and raw arguments;
- descriptor input bounds, symlink/file checks, and preflight-before-network order;
- observation always `execution_attempted:false` and `result_status:not_executed`.

Resolve every Critical or Important finding through a focused RED/GREEN fix and re-review. Do not call the provider until the final review has no Critical or Important findings.

- [ ] **Step 2: Re-run fresh offline verification**

From the external checkout:

```bash
corepack pnpm exec vitest run shadow-plugin/tests
corepack pnpm exec tsc -p shadow-plugin/tsconfig.json --noEmit
corepack pnpm run doc-sync
corepack pnpm run lint
git diff --check
git status --short
```

Expected: all pass and the external worktree is clean.

From AgentHarness:

```bash
PYTHONDONTWRITEBYTECODE=1 ./agentharness validate examples/agent_policy.example.yaml
PYTHONDONTWRITEBYTECODE=1 ./agentharness eval --cases PI-001,PD-001,SEC-001
PYTHONDONTWRITEBYTECODE=1 ./agentharness loop check examples/agent_bus
PYTHONDONTWRITEBYTECODE=1 ./agentharness loop check examples/agent_bus_adapter_registry
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -q
git diff --check
```

Expected: all pass. Do not stage `.superpowers/` or `.understand-anything/`.

- [ ] **Step 3: Issue a fresh five-minute request immediately before launch**

Create a bounded temporary directory and capture the external revision without printing secrets:

```bash
shadow_run_dir="$(mktemp -d /tmp/agentharness-shadow-live.XXXXXX)"
shadow_request_file="$shadow_run_dir/request.json"
shadow_observation_file="$shadow_run_dir/observation.json"
shadow_runtime_revision="$(git -C ../deepseek-harness-shadow rev-parse HEAD)"
PYTHONDONTWRITEBYTECODE=1 ./agentharness shadow issue \
  --request-id shadow-live-20260831-001 \
  --runtime-revision "$shadow_runtime_revision" \
  > "$shadow_request_file"
```

Expected: exit 0 and one request document. Do not print the request because the challenge is live binding material.

- [ ] **Step 4: Perform exactly one authorized provider request**

From the external checkout, after the controller approves network access for this exact command:

```bash
corepack pnpm exec tsx shadow-plugin/src/live-launch.ts \
  3< ../AgentHarness/.env \
  < "$shadow_request_file" \
  > "$shadow_observation_file"
```

Expected: exit 0, empty stderr, and one bounded observation. If it fails for any reason, stop. Do not rerun, fall back to another model, inspect raw provider output, or alter the request.

- [ ] **Step 5: Verify the observation in AgentHarness**

From AgentHarness:

```bash
PYTHONDONTWRITEBYTECODE=1 ./agentharness shadow verify \
  "$shadow_request_file" \
  < "$shadow_observation_file"
```

Expected bounded output:

```json
{"code":"shadow.ok","kind":"shadow.verification.v1","result_status":"not_executed","status":"PASS"}
```

Treat this as candidate evidence only. It is not permission, deployment, runtime authorization, or production certification.

- [ ] **Step 6: Run completion verification and report truthfully**

Invoke `superpowers:verification-before-completion`. Confirm both worktrees' status, the exact external commits, offline test totals, and the verifier document. Report whether the single provider request succeeded; if any gate failed, report the stable failing gate and explicitly state that no retry occurred. Do not include the temporary directory, absolute paths, request challenge, observation body, API key, provider response, or exception detail.
