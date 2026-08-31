# DeepSeek Shadow Controlled Diagnostics Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a separate zero-argument DeepSeek shadow diagnostic launcher
that reports one fixed failure stage while preserving the existing launcher,
one-request runtime, and non-executing observation contract exactly.

**Architecture:** Extract descriptor/preflight work and the prepared shadow
execution into shared internal modules. Internal failures carry only a closed
diagnostic stage; `live-launch.ts` maps every stage back to its legacy generic
error, while `diagnostic-launch.ts` emits a bounded two-field JSON document.
Both entrypoints use the same locked adapter, tool registry, request counter,
observation builder, and disposal path.

**Tech Stack:** TypeScript, Cordis, DeepSeek Harness LLM/AgentLoop packages,
Vitest, fake Fetch/SSE, pnpm, repository translation/doc gates.

**Spec:** `docs/superpowers/specs/2026-08-31-deepseek-shadow-controlled-diagnostics-design.md`

## Global Constraints

- Implement runtime work only in the external `deepseek-harness-shadow`
  checkout on branch `agentharness-shadow-poc`, starting from exact commit
  `bd8691b78dc5d91f2420412a7d24dc4dc02cf8d1`.
- AgentHarness receives this plan only. Do not modify AgentHarness product
  source, CLI, schemas, tests, or verifier behavior.
- Do not read `.env`, use a real credential, access a provider/model, open
  network access, or run either launcher against a real API.
- A later live diagnostic attempt is not authorized by this plan.
- Preserve exact `ERROR: shadow.live_failed\n` for every existing-launcher
  failure and preserve empty stdout on failure.
- The diagnostic failure document is exact compact ASCII JSON with fields in
  order: `{"code":"shadow.diagnostic_failed","stage":"<stage>"}\n`.
- The diagnostic document is at most 128 UTF-8 bytes including newline and has
  no optional fields.
- The exact stage set is `request_preflight`, `credential_input`,
  `runtime_boot`, `provider_transport`, `provider_protocol`, `model_contract`,
  and `cleanup_output`.
- Stage classification uses only a known current phase, `instanceof` checks
  against locally owned error classes, or a closed stable error-code mapping.
  Never inspect exception messages, causes, stacks, enumerable properties,
  HTTP bodies, or provider-controlled detail.
- Both launchers remain zero-argument and accept no transport, provider route,
  model, attempt override, retry, profile, overlay, settings, or environment
  diagnostic toggle.
- Keep exactly one provider request, `redirect: "error"`, no retry plugin,
  DeepSeek `deepseek-v4-flash`, thinking disabled, 256 maximum output tokens,
  60,000 ms idle timeout, and 65,536 aggregate response bytes.
- The only model-visible tool remains `inspect_policy_summary`; accepted
  arguments remain exact current-request binding for `challenge` and
  `policy_scope: "agentharness-shadow-poc"`.
- Every successful observation remains byte-identical across both launchers,
  with `execution_attempted:false` and `result_status:"not_executed"`.
- Diagnostic failure is operator information only. It is never AgentHarness
  evidence, permission, `allow_candidate`, deployment readiness, or
  certification.
- Use strict RED/GREEN TDD. Every new behavior needs a failing test observed
  before production code, a minimal implementation, and a green rerun.
- Stage only explicit task paths. Before every commit, verify the staged file
  list and run `git diff --cached --check`. Never push.

## External file map

- Create `shadow-plugin/src/diagnostics.ts`: closed stage type, safe internal
  error, stage extraction, and exact bounded diagnostic serialization.
- Create `shadow-plugin/src/launch-inputs.ts`: shared zero-argument process
  preflight, descriptor reads, request/key parsing, prepared request/env,
  direct-entry matching, and bounded observation-line formatting.
- Create `shadow-plugin/src/shadow-execution.ts`: request/environment
  preparation and the single prepared runtime/observation/disposal path.
- Create `shadow-plugin/src/diagnostic-run-shadow.ts`: diagnostic wrapper that
  maps request/environment preparation to stages and preserves execution stages.
- Create `shadow-plugin/src/diagnostic-launch.ts`: separate zero-argument
  descriptor launcher and exact diagnostic stderr formatter.
- Modify `shadow-plugin/src/live-launch.ts`: use shared input/execution units
  while retaining its existing exports and exact generic error contract.
- Modify `shadow-plugin/src/run-shadow.ts`: retain the sole normal runtime API
  and map internal execution stages back to `shadow.live_failed`.
- Modify `shadow-plugin/src/locked-runtime.ts`: assign typed transport,
  protocol, and model-contract failures without exposing lower-level detail.
- Create `shadow-plugin/tests/diagnostics.spec.ts`: pure stage/document tests.
- Create `shadow-plugin/tests/launch-inputs.spec.ts`: shared preflight and
  credential classification tests.
- Create `shadow-plugin/tests/diagnostic-run-shadow.spec.ts`: runtime stage,
  lifecycle, redaction, and request-count tests.
- Create `shadow-plugin/tests/diagnostic-launch.spec.ts`: process-facing exact
  stdout/stderr and success-parity tests.
- Modify `shadow-plugin/tests/live-launch.spec.ts`: legacy compatibility after
  extraction.
- Modify `shadow-plugin/tests/locked-runtime.spec.ts`: direct fake-SSE stage
  classification and one-request tests.
- Modify `shadow-plugin/tests/run-shadow.spec.ts`: legacy direct API behavior
  and shared execution regression tests.
- Modify `shadow-plugin/README.md`, `shadow-plugin/README.zh.md`, and
  `shadow-plugin/README.i18n.yaml`: paired operator documentation.
- Modify the existing English/Chinese locked-shadow Agent Note and its pairing
  record to document the separate diagnostic surface and non-evidence boundary.

---

### Task 1: Closed Diagnostic Contract

**Files:**
- Create: `shadow-plugin/src/diagnostics.ts`
- Create: `shadow-plugin/tests/diagnostics.spec.ts`

**Interfaces:**
- Consumes: no prior task interface.
- Produces:
  - `SHADOW_DIAGNOSTIC_STAGES: readonly ShadowDiagnosticStage[]`
  - `type ShadowDiagnosticStage`
  - `class ShadowDiagnosticError extends Error`
  - `diagnosticFailure(stage: ShadowDiagnosticStage): ShadowDiagnosticError`
  - `diagnosticStage(error: unknown, fallback: ShadowDiagnosticStage): ShadowDiagnosticStage`
  - `diagnosticDocument(stage: ShadowDiagnosticStage): string`

- [ ] **Step 1: Write failing tests for the closed stage set and exact documents**

Create `shadow-plugin/tests/diagnostics.spec.ts` with literal expectations:

```ts
import { describe, expect, it } from 'vitest'
import {
  SHADOW_DIAGNOSTIC_STAGES,
  ShadowDiagnosticError,
  diagnosticDocument,
  diagnosticFailure,
  diagnosticStage,
} from '../src/diagnostics.ts'

const stages = [
  'request_preflight',
  'credential_input',
  'runtime_boot',
  'provider_transport',
  'provider_protocol',
  'model_contract',
  'cleanup_output',
] as const

describe('controlled shadow diagnostics', () => {
  it('publishes exactly the approved stages in order', () => {
    expect(SHADOW_DIAGNOSTIC_STAGES).toEqual(stages)
  })

  it.each(stages)('serializes the exact bounded %s document', (stage) => {
    const expected = `{"code":"shadow.diagnostic_failed","stage":"${stage}"}\n`
    const actual = diagnosticDocument(stage)
    expect(actual).toBe(expected)
    expect(Buffer.byteLength(actual, 'utf8')).toBeLessThanOrEqual(128)
  })

  it('stores only the stage and no cause or hostile detail', () => {
    const error = diagnosticFailure('provider_transport')
    expect(error).toBeInstanceOf(ShadowDiagnosticError)
    expect(error.message).toBe('shadow.diagnostic_failed')
    expect(error.stage).toBe('provider_transport')
    expect(error.cause).toBeUndefined()
    expect(Object.keys(error)).toEqual(['stage'])
  })

  it('reads only locally owned errors and otherwise uses the literal fallback', () => {
    const hostile = Object.create(null, {
      stage: { get: () => { throw new Error('/private/key') } },
    })
    expect(diagnosticStage(hostile, 'cleanup_output')).toBe('cleanup_output')
    expect(diagnosticStage(
      diagnosticFailure('provider_protocol'),
      'cleanup_output',
    )).toBe('provider_protocol')
  })
})
```

- [ ] **Step 2: Run RED and confirm the module is missing**

Run:

```bash
corepack pnpm exec vitest run shadow-plugin/tests/diagnostics.spec.ts
```

Expected: FAIL because `../src/diagnostics.ts` does not exist. A syntax or
fixture failure is not acceptable RED evidence.

- [ ] **Step 3: Implement the minimal closed contract**

Create `shadow-plugin/src/diagnostics.ts` with this shape:

```ts
export const SHADOW_DIAGNOSTIC_STAGES = Object.freeze([
  'request_preflight',
  'credential_input',
  'runtime_boot',
  'provider_transport',
  'provider_protocol',
  'model_contract',
  'cleanup_output',
] as const)

export type ShadowDiagnosticStage = typeof SHADOW_DIAGNOSTIC_STAGES[number]

export class ShadowDiagnosticError extends Error {
  readonly stage: ShadowDiagnosticStage

  constructor(stage: ShadowDiagnosticStage) {
    super('shadow.diagnostic_failed')
    Object.defineProperty(this, 'name', {
      configurable: false,
      enumerable: false,
      value: 'ShadowDiagnosticError',
      writable: false,
    })
    Object.defineProperty(this, 'stage', {
      configurable: false,
      enumerable: true,
      value: stage,
      writable: false,
    })
  }
}

export function diagnosticFailure(
  stage: ShadowDiagnosticStage,
): ShadowDiagnosticError {
  return new ShadowDiagnosticError(stage)
}

export function diagnosticStage(
  error: unknown,
  fallback: ShadowDiagnosticStage,
): ShadowDiagnosticStage {
  return error instanceof ShadowDiagnosticError ? error.stage : fallback
}

export function diagnosticDocument(stage: ShadowDiagnosticStage): string {
  const output = `{"code":"shadow.diagnostic_failed","stage":"${stage}"}\n`
  if (Buffer.byteLength(output, 'utf8') > 128) {
    return '{"code":"shadow.diagnostic_failed","stage":"cleanup_output"}\n'
  }
  return output
}
```

Do not accept arbitrary strings or error-detail parameters. Do not use
`JSON.stringify(error)` or attach a cause.

- [ ] **Step 4: Run GREEN and the existing shadow surface tests**

Run:

```bash
corepack pnpm exec vitest run shadow-plugin/tests/diagnostics.spec.ts
corepack pnpm exec vitest run shadow-plugin/tests/runtime-shadow.spec.ts
corepack pnpm exec tsc -p shadow-plugin/tsconfig.json --noEmit
```

Expected: all pass. The runtime surface remains unchanged because no existing
production module exports diagnostics.

- [ ] **Step 5: Stage exact paths, verify, and commit**

```bash
git add -- shadow-plugin/src/diagnostics.ts shadow-plugin/tests/diagnostics.spec.ts
git diff --cached --name-only
git diff --cached --check
git commit -m "feat: define bounded shadow diagnostic stages"
```

Expected staged list: exactly the two paths above.

---

### Task 2: Shared Descriptor and Preflight Pipeline

**Files:**
- Create: `shadow-plugin/src/launch-inputs.ts`
- Create: `shadow-plugin/tests/launch-inputs.spec.ts`
- Modify: `shadow-plugin/src/live-launch.ts`
- Modify: `shadow-plugin/tests/live-launch.spec.ts`

**Interfaces:**
- Consumes: Task 1 `diagnosticFailure`, `diagnosticStage`, and
  `ShadowDiagnosticError`.
- Produces:
  - `interface LiveLaunchInputs` with the existing five fields.
  - `interface PreparedShadowLaunch { request: ShadowRequest; environment: Record<string, string> }`.
  - `prepareShadowLaunch(inputs: LiveLaunchInputs): PreparedShadowLaunch`.
  - `readProcessLaunchInputs(): LiveLaunchInputs` for zero-argument stdin/fd-3
    execution.
  - `boundedObservationLine(observation: RuntimeShadowObservation): string`.
  - `isDirectEntry(moduleUrl: string, argvEntry: string | undefined): boolean`.
  - Existing `runLiveLaunch(inputs: LiveLaunchInputs): Promise<string>` remains
    exported from `live-launch.ts` and retains generic failures.
  - `live-launch.ts` re-exports the `LiveLaunchInputs` type from
    `launch-inputs.ts`; its runtime exports remain exactly `main` and
    `runLiveLaunch`.

- [ ] **Step 1: Write RED tests that name preflight and credential boundaries**

Create `shadow-plugin/tests/launch-inputs.spec.ts`. Reuse literal valid request
fixtures from `live-launch.spec.ts`, but do not call a helper that computes the
expected stage. Include at least these assertions:

```ts
it('classifies duplicate request members as request_preflight', () => {
  const error = captureSyncFailure(() => prepareShadowLaunch({
    ...validInputs(),
    requestSource: Buffer.from(duplicateChallengeDocument(), 'utf8'),
  }))
  expect(error).toBeInstanceOf(ShadowDiagnosticError)
  expect((error as ShadowDiagnosticError).stage).toBe('request_preflight')
})

it('classifies an invalid literal key source as credential_input', () => {
  const error = captureSyncFailure(() => prepareShadowLaunch({
    ...validInputs(),
    keySource: Buffer.from('DEEPSEEK_API_KEY=fake\nEXTRA=forbidden\n'),
  }))
  expect((error as ShadowDiagnosticError).stage).toBe('credential_input')
})
```

Add discriminating cases for zero/extra argv, AgentHarness cwd/marker,
external `.env`, oversized/fatal-UTF-8 descriptor 0, stale/future request,
oversized/fatal-UTF-8 descriptor 3, duplicate/empty/control-bearing key, and
invalid locale environment. Every request-side case expects
`request_preflight`; every key/environment case expects `credential_input`.
Use spies that prove key/environment properties are not read after a request
failure.

In `live-launch.spec.ts`, add a table that feeds one failure from each of the
two stages through `runLiveLaunch()` and expects only
`Error('shadow.live_failed')` with no cause or fake secret/path.

- [ ] **Step 2: Run RED and confirm classification is unavailable**

Run:

```bash
corepack pnpm exec vitest run shadow-plugin/tests/launch-inputs.spec.ts shadow-plugin/tests/live-launch.spec.ts
```

Expected: new tests fail because `launch-inputs.ts` is missing and the existing
launcher owns generic helpers directly.

- [ ] **Step 3: Extract shared input preparation with typed stage wrappers**

Move the existing constants and pure helpers for cwd/marker checks, bounded
descriptor decoding, request parsing, `.env` detection, literal key parsing,
and environment allowlisting into `launch-inputs.ts` without changing their
bounds or order.

Use explicit boundary wrappers, not exception-message classification:

```ts
function atStage<T>(stage: ShadowDiagnosticStage, operation: () => T): T {
  try {
    return operation()
  } catch (error: unknown) {
    throw diagnosticFailure(diagnosticStage(error, stage))
  }
}

export function prepareShadowLaunch(
  inputs: LiveLaunchInputs,
): PreparedShadowLaunch {
  const request = atStage('request_preflight', () => {
    assertExternalRuntimeDirectory(inputs.cwd)
    if (inputs.externalEnvExists) throw new Error('closed')
    return parseRequest(inputs.requestSource)
  })
  const environment = atStage('credential_input', () => {
    const keySource = decodeBounded(inputs.keySource, MAX_KEY_SOURCE_BYTES)
    return buildChildEnvironment(
      parseLiteralKeyAssignment(keySource),
      inputs.inheritedEnvironment,
    )
  })
  return Object.freeze({ request, environment })
}
```

`readProcessLaunchInputs()` must validate `process.argv.length === 2`, cwd,
marker conflicts, and external `.env` before descriptor 0; then read descriptor
0 under `request_preflight` and descriptor 3 under `credential_input`. It must
not scan parents or read any file path supplied through argv/environment.

- [ ] **Step 4: Refactor the existing launcher as a generic adapter**

Keep `live-launch.ts`'s public type/export compatibility. Its functional path
must have one generic catch:

```ts
export async function runLiveLaunch(inputs: LiveLaunchInputs): Promise<string> {
  try {
    const { request, environment } = prepareShadowLaunch(inputs)
    const observation = await runShadow(request, environment, { attempts: 1 })
    return boundedObservationLine(observation)
  } catch {
    throw new Error('shadow.live_failed')
  }
}
```

The executable `main()` must call `readProcessLaunchInputs()` and
`boundedObservationLine()`, while its terminal catch remains exact:

```ts
main().catch(() => {
  process.stdout.write('')
  process.stderr.write('ERROR: shadow.live_failed\n')
  process.exitCode = 1
})
```

- [ ] **Step 5: Run GREEN, mutation checks, and compatibility tests**

Run:

```bash
corepack pnpm exec vitest run shadow-plugin/tests/launch-inputs.spec.ts shadow-plugin/tests/live-launch.spec.ts
corepack pnpm exec vitest run shadow-plugin/tests/live-policy.spec.ts shadow-plugin/tests/runtime-shadow.spec.ts
corepack pnpm exec tsc -p shadow-plugin/tsconfig.json --noEmit
git diff --check
```

Mutation checks: temporarily swap the two stage literals and verify the stage
tests fail; temporarily let `live-launch.ts` serialize the typed error and
verify the exact generic compatibility tests fail. Restore production before
the GREEN run.

- [ ] **Step 6: Stage exact paths, verify, and commit**

```bash
git add -- shadow-plugin/src/launch-inputs.ts shadow-plugin/src/live-launch.ts shadow-plugin/tests/launch-inputs.spec.ts shadow-plugin/tests/live-launch.spec.ts
git diff --cached --name-only
git diff --cached --check
git commit -m "refactor: share closed shadow launch inputs"
```

Expected staged list: exactly the four paths above.

---

### Task 3: Shared Runtime Execution and Stage Mapping

**Files:**
- Create: `shadow-plugin/src/shadow-execution.ts`
- Create: `shadow-plugin/src/diagnostic-run-shadow.ts`
- Create: `shadow-plugin/tests/diagnostic-run-shadow.spec.ts`
- Modify: `shadow-plugin/src/run-shadow.ts`
- Modify: `shadow-plugin/src/locked-runtime.ts`
- Modify: `shadow-plugin/tests/run-shadow.spec.ts`
- Modify: `shadow-plugin/tests/locked-runtime.spec.ts`

**Interfaces:**
- Consumes: Task 1 diagnostic types and Task 2 prepared request/environment.
- Produces:
  - `type RunShadowOptions = { readonly attempts: number }` from
    `shadow-execution.ts`, re-exported as a type from `run-shadow.ts`.
  - `prepareShadowRequest(request: ShadowRequest, options: RunShadowOptions): ShadowRequest`.
  - `prepareShadowEnvironment(environment: Record<string, string>): Readonly<Record<string, string>>`.
  - `executePreparedShadow(request: ShadowRequest, environment: Readonly<Record<string, string>>): Promise<RuntimeShadowObservation>`.
  - `runShadowDiagnostic(request, environment, options?): Promise<RuntimeShadowObservation>` from `diagnostic-run-shadow.ts`.
  - Existing `runShadow()` remains the only export from `run-shadow.ts`.

- [ ] **Step 1: Write RED runtime-stage tests before extracting code**

Create `shadow-plugin/tests/diagnostic-run-shadow.spec.ts` with controlled time,
fake credentials, and fake runtime spies. Its literal expectations must cover:

```ts
it.each([
  ['expired request', expiredRequest(), 'request_preflight'],
  ['future request', futureRequest(), 'request_preflight'],
] as const)('classifies %s before environment and boot', async (
  _name,
  request,
  stage,
) => {
  const inaccessibleEnvironment = new Proxy({}, {
    ownKeys: () => { throw new Error('/private/environment') },
  }) as Record<string, string>
  const failure = await runShadowDiagnostic(request, inaccessibleEnvironment)
    .catch((error: unknown) => error)
  expect((failure as ShadowDiagnosticError).stage).toBe(stage)
  expect(bootLockedRuntime).not.toHaveBeenCalled()
})
```

Add fake-runtime cases for `runtime_boot`, `model_contract`, and
`cleanup_output`. Assert boot failure has zero fetch calls; model-contract
failure has one; disposal failure is `cleanup_output`; and every error excludes
the fake key, host path, provider body, and original cause.

Add a whitespace/control-invalid credential case that expects
`credential_input`, zero runtime boots, and zero fetch calls.

Modify `locked-runtime.spec.ts` with direct fake-SSE cases:

- fetch rejection, redirect response, non-2xx response, idle timeout, and
  65,537-byte response -> `provider_transport`, one fetch;
- malformed SSE JSON, malformed framing, and EOF without `[DONE]` ->
  `provider_protocol`, one fetch;
- text-only output, wrong tool, duplicate/changed/extra arguments, stop/missing
  finish, error result, wrong step/turn, and non-completed turn ->
  `model_contract`, one fetch;
- a second runtime turn still rejects before a second fetch.

Modify `run-shadow.spec.ts` to prove the normal `runShadow()` retains its safe
preparation errors where currently public and maps every post-preparation typed
stage to only `shadow.live_failed`.

- [ ] **Step 2: Run RED and confirm runtime failures remain undifferentiated**

Run:

```bash
corepack pnpm exec vitest run shadow-plugin/tests/diagnostic-run-shadow.spec.ts shadow-plugin/tests/locked-runtime.spec.ts shadow-plugin/tests/run-shadow.spec.ts
```

Expected: diagnostic module tests fail because no diagnostic execution API
exists; new locked-runtime stage assertions receive generic errors.

- [ ] **Step 3: Extract request/environment preparation and prepared execution**

Move current request snapshot/freshness, environment snapshot, observation
construction, runtime boot/turn, and disposal logic into
`shadow-execution.ts`. Preserve all current exact bounds and field sets.

Use this lifecycle structure:

```ts
export async function executePreparedShadow(
  request: ShadowRequest,
  environment: Readonly<Record<string, string>>,
): Promise<RuntimeShadowObservation> {
  let runtime: LockedRuntime
  try {
    runtime = await bootLockedRuntime({
      request,
      key: environment.DEEPSEEK_API_KEY,
    })
  } catch {
    throw diagnosticFailure('runtime_boot')
  }

  let observation: RuntimeShadowObservation
  try {
    const evidence = await runtime.runOneModelTurn()
    observation = buildLiveObservation(request, evidence.arguments)
  } catch (error: unknown) {
    try {
      await runtime.dispose()
    } catch {
      // The primary typed failure remains authoritative.
    }
    throw diagnosticFailure(diagnosticStage(error, 'model_contract'))
  }

  try {
    await runtime.dispose()
    return observation
  } catch {
    throw diagnosticFailure('cleanup_output')
  }
}
```

Observation construction must map canonicalization/8,192-byte failures to
`cleanup_output`, not `model_contract`.

`prepareShadowRequest()` preserves the exact `attempts === 1`, request
snapshot, five-minute interval, and `issued_at <= now < expires_at` checks.
`prepareShadowEnvironment()` preserves the current plain-record, exact key,
per-field, total-byte, locale, and telemetry constraints.
It must also call the existing `assertUsableApiKey()` before runtime boot,
store the normalized returned key, and replace any rejection with exact
`Error('shadow.environment_invalid')`. This keeps the normal direct API stable
while the diagnostic wrapper classifies the same failure as
`credential_input` before boot or fetch.

- [ ] **Step 4: Preserve the normal `runShadow()` contract**

`run-shadow.ts` remains the sole normal export:

```ts
export async function runShadow(
  request: ShadowRequest,
  environment: Record<string, string>,
  options: RunShadowOptions = { attempts: 1 },
): Promise<RuntimeShadowObservation> {
  const requestSnapshot = prepareShadowRequest(request, options)
  const environmentSnapshot = prepareShadowEnvironment(environment)
  try {
    return await executePreparedShadow(requestSnapshot, environmentSnapshot)
  } catch {
    throw new Error('shadow.live_failed')
  }
}
```

Re-export `RunShadowOptions` with `export type`; do not export the shared
execution helpers from `run-shadow.ts`. Its only runtime export remains
`runShadow`.

- [ ] **Step 5: Implement the diagnostic runtime wrapper**

Create `diagnostic-run-shadow.ts`:

```ts
export async function runShadowDiagnostic(
  request: ShadowRequest,
  environment: Record<string, string>,
  options: RunShadowOptions = { attempts: 1 },
): Promise<RuntimeShadowObservation> {
  let requestSnapshot: ShadowRequest
  try {
    requestSnapshot = prepareShadowRequest(request, options)
  } catch {
    throw diagnosticFailure('request_preflight')
  }
  let environmentSnapshot: Readonly<Record<string, string>>
  try {
    environmentSnapshot = prepareShadowEnvironment(environment)
  } catch {
    throw diagnosticFailure('credential_input')
  }
  return executePreparedShadow(requestSnapshot, environmentSnapshot)
}
```

This module accepts no runtime, adapter, clock, transport, or provider
injection. Tests control only global fake time/fetch or module spies at the
same boundaries already used by the existing suite.

- [ ] **Step 6: Add typed adapter/protocol/model boundaries in the locked runtime**

In `OneRequestDeepSeekAdapter.stream()`:

- preserve the request counter increment before delegation;
- convert duplicate decoded tool-argument members directly to
  `model_contract`;
- preserve an existing `ShadowDiagnosticError`;
- map `MALFORMED_RESPONSE` and `STREAM_CLOSED` to `provider_protocol`;
- map `INVALID_CREDENTIAL` defensively to `credential_input` before fetch;
- map adapter-originated `TRANSPORT`, `TIMEOUT`, `ABORTED`, `AUTH`, `QUOTA`,
  `RATE_LIMIT`, `INVALID_REQUEST`,
  `CONTEXT_WINDOW_EXCEEDED`, `SERVER`, `EMPTY_RESPONSE`,
  `RESPONSE_TOO_LARGE`, and `HTTP_<status>` to `provider_transport`; and
- map any other exception thrown by the adapter stream boundary to
  `provider_transport` without inspecting it.

Use a closed code predicate:

```ts
const PROTOCOL_CODES = new Set(['MALFORMED_RESPONSE', 'STREAM_CLOSED'])
const TRANSPORT_CODES = new Set([
  'TRANSPORT', 'TIMEOUT', 'ABORTED', 'AUTH', 'QUOTA',
  'RATE_LIMIT', 'INVALID_REQUEST', 'CONTEXT_WINDOW_EXCEEDED', 'SERVER',
  'EMPTY_RESPONSE', 'RESPONSE_TOO_LARGE',
])

function adapterFailureStage(error: unknown): ShadowDiagnosticStage {
  if (!(error instanceof LlmError)) return 'provider_transport'
  if (error.code === 'INVALID_CREDENTIAL') return 'credential_input'
  if (PROTOCOL_CODES.has(error.code)) return 'provider_protocol'
  if (TRANSPORT_CODES.has(error.code) || /^HTTP_[1-5][0-9]{2}$/.test(error.code)) {
    return 'provider_transport'
  }
  return 'provider_transport'
}
```

Do not read `error.message`, `error.failure`, `error.cause`, status, request id,
or retry-after data.

After `agent.whenIdle()` returns, the existing exact transcript predicate maps
only to `model_contract`. If `agent.whenIdle()` rejects with a typed diagnostic
error, preserve it; any other rejection at that boundary maps to
`model_contract`. Boot-time composition catches remain outside the provider
request and are classified by `executePreparedShadow()` as `runtime_boot`.

- [ ] **Step 7: Run GREEN, mutation checks, and the complete shadow suite**

Run:

```bash
corepack pnpm exec vitest run shadow-plugin/tests/diagnostic-run-shadow.spec.ts shadow-plugin/tests/locked-runtime.spec.ts shadow-plugin/tests/run-shadow.spec.ts
corepack pnpm exec vitest run shadow-plugin/tests
corepack pnpm exec vitest run packages/llm/llm-deepseek/tests/adapter.spec.ts packages/llm/llm-deepseek/tests/sse.spec.ts packages/llm/llm-deepseek/tests/translate.spec.ts
corepack pnpm exec tsc -p shadow-plugin/tsconfig.json --noEmit
corepack pnpm exec tsc -p packages/llm/llm-deepseek/tsconfig.json --noEmit
```

Expected: all pass using fake transport only.

Mutation checks: swap protocol/transport mapping; remove the typed-error
preservation; move request-count increment after delegation; or return an
observation before disposal. Each corresponding test must fail. Restore and
rerun GREEN.

- [ ] **Step 8: Stage exact paths, verify, and commit**

```bash
git add -- shadow-plugin/src/shadow-execution.ts shadow-plugin/src/diagnostic-run-shadow.ts shadow-plugin/src/run-shadow.ts shadow-plugin/src/locked-runtime.ts shadow-plugin/tests/diagnostic-run-shadow.spec.ts shadow-plugin/tests/run-shadow.spec.ts shadow-plugin/tests/locked-runtime.spec.ts
git diff --cached --name-only
git diff --cached --check
git commit -m "feat: classify locked shadow failure stages"
```

Expected staged list: exactly the seven paths above.

---

### Task 4: Separate Diagnostic Launcher and Offline Closure

**Files:**
- Create: `shadow-plugin/src/diagnostic-launch.ts`
- Create: `shadow-plugin/tests/diagnostic-launch.spec.ts`
- Modify: `shadow-plugin/README.md`
- Modify: `shadow-plugin/README.zh.md`
- Modify: `shadow-plugin/README.i18n.yaml`
- Modify: `.agents/notes/implemented/feature/2026-08-20-locked-agentharness-shadow-runtime.md`
- Modify: `.agents/notes/implemented/feature/2026-08-20-locked-agentharness-shadow-runtime.zh.md`
- Modify: `.agents/notes/implemented/feature/2026-08-20-locked-agentharness-shadow-runtime.i18n.yaml`

**Interfaces:**
- Consumes: Task 2 `readProcessLaunchInputs` / `prepareShadowLaunch`, Task 3
  `runShadowDiagnostic`, and Task 1 `diagnosticDocument` / `diagnosticStage`.
- Produces:
  - `runDiagnosticLaunch(inputs: LiveLaunchInputs): Promise<string>`.
  - zero-argument executable `diagnostic-launch.ts`.
  - exact success parity with `live-launch.ts` and exact failure JSON stderr.

- [ ] **Step 1: Write RED process-facing failure tests**

Create `shadow-plugin/tests/diagnostic-launch.spec.ts`. Use subprocess or the
same process-stream harness as `live-launch.spec.ts`. For every literal stage,
assert:

```ts
expect(result.exitCode).toBe(1)
expect(result.stdout).toBe('')
expect(result.stderr).toBe(
  '{"code":"shadow.diagnostic_failed","stage":"provider_transport"}\n',
)
```

Each fixture includes fake sensitive strings such as
`sk-test-not-real-credential`, `/private/operator/path`, a fake provider body,
raw tool arguments, and control characters. Assert none occur in stdout,
stderr, error cause, or serialized result.

Add zero-fetch subprocess cases for `request_preflight`, `credential_input`,
and `runtime_boot`; one-fetch cases for `provider_transport`,
`provider_protocol`, and `model_contract`; and a disposal/serialization case
for `cleanup_output`. Assert no retry and no second model turn.

- [ ] **Step 2: Write RED success-parity and closed-surface tests**

With one fake matching SSE tool call, call `runLiveLaunch()` and
`runDiagnosticLaunch()` using independently cloned literal inputs. Assert the
returned strings are byte-identical, newline terminated, at most 8,192 bytes,
and parse to `execution_attempted:false` / `result_status:"not_executed"`.

Add export/surface assertions that:

- `live-launch.ts` exports only its existing public names;
- `diagnostic-launch.ts` exports exactly `runDiagnosticLaunch` and `main`;
- neither entrypoint accepts command arguments or options; and
- no environment field enables diagnostic formatting in the normal launcher.

- [ ] **Step 3: Run RED and confirm the diagnostic entrypoint is absent**

Run:

```bash
corepack pnpm exec vitest run shadow-plugin/tests/diagnostic-launch.spec.ts shadow-plugin/tests/live-launch.spec.ts
```

Expected: FAIL because `diagnostic-launch.ts` does not exist. Existing live
tests remain green.

- [ ] **Step 4: Implement the separate zero-argument diagnostic entrypoint**

Create `shadow-plugin/src/diagnostic-launch.ts` with the same direct-entry
guard as `live-launch.ts`:

```ts
export async function runDiagnosticLaunch(
  inputs: LiveLaunchInputs,
): Promise<string> {
  const { request, environment } = prepareShadowLaunch(inputs)
  const observation = await runShadowDiagnostic(
    request,
    environment,
    { attempts: 1 },
  )
  try {
    return boundedObservationLine(observation)
  } catch {
    throw diagnosticFailure('cleanup_output')
  }
}

export async function main(): Promise<void> {
  const output = await runDiagnosticLaunch(readProcessLaunchInputs())
  process.stdout.write(output)
}

if (isDirectEntry(import.meta.url, process.argv[1])) {
  main().catch((error: unknown) => {
    process.stdout.write('')
    process.stderr.write(diagnosticDocument(
      diagnosticStage(error, 'cleanup_output'),
    ))
    process.exitCode = 1
  })
}
```

Reuse Task 2 `boundedObservationLine()` and `isDirectEntry()` from
`launch-inputs.ts` rather than duplicating cwd checks, descriptor reads,
request parsing, key parsing, runtime execution, observation serialization, or
direct-entry comparison.

- [ ] **Step 5: Run GREEN and complete adversarial offline verification**

Run:

```bash
corepack pnpm exec vitest run shadow-plugin/tests/diagnostic-launch.spec.ts shadow-plugin/tests/live-launch.spec.ts
corepack pnpm exec vitest run shadow-plugin/tests
corepack pnpm exec vitest run packages/llm/llm-deepseek/tests/adapter.spec.ts packages/llm/llm-deepseek/tests/sse.spec.ts packages/llm/llm-deepseek/tests/translate.spec.ts
corepack pnpm exec tsc -p shadow-plugin/tsconfig.json --noEmit
corepack pnpm exec tsc -p packages/llm/llm-deepseek/tsconfig.json --noEmit
```

Expected: all pass. No command may reference the protected `.env` or a network
endpoint outside fake fixtures/local mock servers.

- [ ] **Step 6: Update paired operator documentation**

Document this offline-only diagnostic command shape in English and Chinese:

```bash
corepack pnpm exec tsx shadow-plugin/src/diagnostic-launch.ts \
  3< "$AGENTHARNESS_ENV_FILE" \
  < "$SHADOW_REQUEST_FILE" \
  > "$SHADOW_OBSERVATION_FILE" \
  2> "$SHADOW_DIAGNOSTIC_FILE"
```

State all seven stages verbatim. State that the current live launcher retains
exact `shadow.live_failed`; diagnostic JSON is operator information only;
success alone can enter unchanged AgentHarness verification; all results remain
`not_executed`; and running the command with a real key requires a later
separate one-call authorization.

Update both Agent Notes with the same architecture decision and consequences.
Refresh all modified translation-pair records:

```bash
corepack pnpm run verify-translation-pairing --write shadow-plugin/README.md
corepack pnpm run verify-translation-pairing --write .agents/notes/implemented/feature/2026-08-20-locked-agentharness-shadow-runtime.md
```

- [ ] **Step 7: Run complete offline gates and static boundary scans**

Run:

```bash
corepack pnpm exec vitest run shadow-plugin/tests
corepack pnpm exec vitest run packages/llm/llm-deepseek/tests/adapter.spec.ts packages/llm/llm-deepseek/tests/sse.spec.ts packages/llm/llm-deepseek/tests/translate.spec.ts
corepack pnpm exec tsc -p shadow-plugin/tsconfig.json --noEmit
corepack pnpm exec tsc -p packages/llm/llm-deepseek/tsconfig.json --noEmit
corepack pnpm run doc-sync
corepack pnpm run lint
rg -n "console\\.|process\\.env\\.DEEPSEEK|DEEPSEEK_BASE_URL|DSH_HOME|credentials|profile|overlay|retry" shadow-plugin/src
git diff --check
git status --short
```

Review every static-scan hit; approved type names/comments do not excuse a
production credential lookup, route override, loader, logger, or retry path.
The external checkout must contain only the intended unstaged task paths before
commit and be clean afterward.

From AgentHarness, rerun the required unchanged-boundary verification:

```bash
PYTHONDONTWRITEBYTECODE=1 ./agentharness validate examples/agent_policy.example.yaml
PYTHONDONTWRITEBYTECODE=1 ./agentharness eval --cases PI-001,PD-001,SEC-001
PYTHONDONTWRITEBYTECODE=1 ./agentharness loop check examples/agent_bus
PYTHONDONTWRITEBYTECODE=1 ./agentharness loop check examples/agent_bus_adapter_registry
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -q tests.test_handoff_exporter tests.test_handoff_manifest tests.test_loop_bus tests.test_pi_tool_call_mapping tests.test_pi_evidence_contract_v1 tests.test_pi_evidence_contract_cli_v1
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -q
git diff --check
```

Do not stage `.superpowers/` or `.understand-anything/`.

- [ ] **Step 8: Stage exact external paths, verify, and commit**

```bash
git add -- shadow-plugin/src/diagnostic-launch.ts shadow-plugin/tests/diagnostic-launch.spec.ts shadow-plugin/README.md shadow-plugin/README.zh.md shadow-plugin/README.i18n.yaml .agents/notes/implemented/feature/2026-08-20-locked-agentharness-shadow-runtime.md .agents/notes/implemented/feature/2026-08-20-locked-agentharness-shadow-runtime.zh.md .agents/notes/implemented/feature/2026-08-20-locked-agentharness-shadow-runtime.i18n.yaml
git diff --cached --name-only
git diff --cached --check
git commit -m "feat: add controlled shadow diagnostic launcher"
```

Expected staged list: exactly the eight paths above.

- [ ] **Step 9: Independent review and hard stop**

Invoke `superpowers:requesting-code-review` over exact baseline
`bd8691b78dc5d91f2420412a7d24dc4dc02cf8d1` through current external HEAD.
The reviewer must inspect:

- exact legacy launcher compatibility;
- the closed seven-stage mapping and unknown-error fallback;
- no message/cause/property/provider-detail inspection;
- zero fetch before transport and exactly one fetch afterward;
- no second model round or retry;
- identical successful observations;
- exact 128-byte diagnostic and 8,192-byte observation bounds;
- no injectable runtime/provider/route/model/transport success seam;
- no secret, path, request, prompt, response, argument, or HTTP-detail leak;
- diagnostic non-evidence/authorization boundaries; and
- test sensitivity rather than mock-only assertions.

Resolve every Critical or Important finding with focused RED/GREEN work and a
scoped re-review. Then rerun the complete offline gates from Steps 5 and 7.

Stop after a clean review and report. Do not read `.env`, request network
approval, issue a fresh shadow request, execute a real provider call, or run
AgentHarness verification against a live observation. A new user authorization
is required for any later live diagnostic attempt.
