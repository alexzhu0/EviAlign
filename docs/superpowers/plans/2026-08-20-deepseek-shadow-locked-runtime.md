# DeepSeek Shadow Locked Runtime Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the unsafe stock-profile PoC with a directly composed, locked external runtime that records one non-executing Flash synthetic-tool intent.

**Architecture:** A local TypeScript launcher composes a minimal Cordis app directly from the pinned Harness source. It never calls `dsh`, loads a profile, accepts overlay paths, mounts settings/credentials services, or scans `.env`; it receives one already-parsed key in its child environment and emits only a bounded observation for AgentHarness.

**Tech Stack:** pinned DeepSeek Harness `99f6f02fecdb7dff40c3fbc9470f5907c29f74ca`, TypeScript, Vitest, Cordis, `@deepseek-ai/dsh-llm-deepseek`.

## Global Constraints

- The checkout is `/home/alex/DTAlex/learningGitHub/deepseek-harness-shadow` on branch `agentharness-shadow-poc`; never change AgentHarness from this repository.
- Do not use stock `dsh`, `dsh-headless`, profiles, `DSH_HOME`, `--patch`, settings, credentials, session persistence, filesystem, shell, subprocess, jobs, web, skills, MCP, delegation, workflow, todo, goal, code runtime, compaction, title, or retry plugins.
- The only model-visible tool is `inspect_policy_summary`; it returns `{ status: "shadow_observed", executed: false }`, performs no action, and every observation uses `execution_attempted:false` and `result_status:"not_executed"`.
- The only route is `deepseek-v4-flash`, thinking disabled, maxTokens 256, stream timeout 60000 ms, and no retry; a first acceptance run performs at most one provider call.
- No `.env` is read by Harness. A literal local parser may provide only `DEEPSEEK_API_KEY` to a cleared child environment; key, prompt, response, absolute path and raw arguments are never logged or emitted.
- Offline tests and independent review pass before any paid run. A provider failure, bound violation, unexpected tool, or AgentHarness rejection fails the PoC without retry.

## File Structure

- `shadow-plugin/src/locked-runtime.ts`: direct minimal Cordis composition and exact registry assertion.
- `shadow-plugin/src/runtime-shadow.ts`: synthetic tool capture and fixed response.
- `shadow-plugin/src/observation.ts`: canonical bounded observation builder.
- `shadow-plugin/src/load-key.ts`: literal one-key parser and child environment builder.
- `shadow-plugin/src/run-shadow.ts`: one-shot locked launcher and bounded output.
- `shadow-plugin/tests/locked-runtime.spec.ts`, `runtime-shadow.spec.ts`, `run-shadow.spec.ts`: offline behavior and adversarial tests.

### Task 1: Direct locked composition

**Files:** Create `shadow-plugin/src/locked-runtime.ts`, `shadow-plugin/tests/locked-runtime.spec.ts`; remove the Task-1 profile overlay/profile test after its replacement passes.

**Interfaces:** `bootLockedRuntime(options: { key?: string; request: ShadowRequest; }): Promise<LockedRuntime>` returns a registry exposing exactly `inspect_policy_summary`; it accepts no profile, patch, cwd, settings or credential-file input.

- [ ] **Step 1: Write failing isolation tests**

```ts
it('registers only the synthetic tool and no prohibited service', async () => {
  const runtime = await bootLockedRuntime({ request: validRequest() })
  expect(runtime.toolNames()).toEqual(['inspect_policy_summary'])
  expect(runtime.activePluginNames()).not.toEqual(expect.arrayContaining([
    '@deepseek-ai/dsh-tool-bash', '@deepseek-ai/dsh-tool-fs',
    '@deepseek-ai/dsh-tool-web', '@deepseek-ai/dsh-credentials-local',
    '@deepseek-ai/dsh-settings-file', '@deepseek-ai/dsh-headless',
  ]))
})
```

- [ ] **Step 2: Verify RED**

Run `corepack pnpm exec vitest run shadow-plugin/tests/locked-runtime.spec.ts`; expect module-not-found failure.

- [ ] **Step 3: Implement direct composition**

Mount only Cordis, `dsh-tools`, `dsh-system-prompt`, `dsh-llm`, `dsh-llm-deepseek`, `dsh-agent`, `dsh-agent-loop`, and the synthetic plugin. Configure the adapter literal with `thinking: 'disabled'`, `maxTokens: 256`, `streamIdleTimeoutMs: 60000`, `models: [{ id: 'deepseek-v4-flash', maxTokens: 256 }]`, and retry disabled by omission of the retry plugin. Reject boot if the registry differs from the one-tool allowlist.

Mount one in-memory `SessionStore` only because the pinned `AgentLoop` requires
the `sessions` service; do not mount any session persistence plugin.

- [ ] **Step 4: Verify GREEN and commit**

Run `corepack pnpm exec vitest run shadow-plugin/tests/locked-runtime.spec.ts && git diff --check`; explicitly stage the Task-1 replacement paths, cached-check, and commit `feat: lock shadow runtime composition`.

### Task 2: Bounded synthetic evidence and launcher

**Files:** Create `shadow-plugin/src/runtime-shadow.ts`, `observation.ts`, `load-key.ts`, `run-shadow.ts` and matching three test files.

**Interfaces:** `runShadow(request: ShadowRequest, environment: Record<string,string>): Promise<RuntimeShadowObservation>`; only a matching single synthetic call resolves.

- [ ] **Step 1: Write failing behavior tests**

```ts
it('captures one matching call without executing an operation', async () => {
  const observation = await runShadow(validRequest(), testEnvironment())
  expect(observation.execution_attempted).toBe(false)
  expect(observation.result_status).toBe('not_executed')
})
it.each([changedChallenge(), extraArgument(), secondToolCall()])('rejects invalid call', async call => {
  await expect(captureSyntheticCall(validRequest(), call)).rejects.toThrow('shadow.binding_invalid')
})
```

- [ ] **Step 2: Verify RED**

Run `corepack pnpm exec vitest run shadow-plugin/tests/runtime-shadow.spec.ts shadow-plugin/tests/run-shadow.spec.ts`; expect missing-module failure.

- [ ] **Step 3: Implement fixed tool, key parser, and launcher**

Validate exact Challenge/policy arguments; construct canonical SHA-256 digests and the exact AgentHarness observation fields. Parse exactly one literal key line without source/eval; construct only `DEEPSEEK_API_KEY`, `PATH`, locale and `DSH_TELEMETRY_DISABLED=1` environment. Capture child output internally, emit only compact observation JSON, and reject any second call, unsupported tool, transcript, route, retry or byte overflow.

- [ ] **Step 4: Verify GREEN and commit**

Run `corepack pnpm exec vitest run shadow-plugin/tests && git diff --check`; explicitly stage Task-2 paths, cached-check, and commit `feat: capture locked shadow observation`.

### Task 3: Manual one-call Flash acceptance

**Files:** Modify `shadow-plugin/README.md`; add `shadow-plugin/tests/live-policy.spec.ts` without a live test default.

- [ ] **Step 1: Write offline launch-policy test**

```ts
it('refuses a second attempt before provider invocation', async () => {
  await expect(runShadow(validRequest(), testEnvironment(), { attempts: 2 }))
    .rejects.toThrow('shadow.request_limit')
})
```

- [ ] **Step 2: Verify RED then implement**

Run the focused test, implement the one-attempt cap and README command that pipes the observation to `./agentharness shadow verify`, then rerun it green.

- [ ] **Step 3: Offline gate and reviewed manual run**

Run `corepack pnpm exec vitest run shadow-plugin/tests`, `git diff --check`, and independent code review. Only then, with an operator-supplied protected key file, run one request; store the observation in an ignored temporary file and verify it with AgentHarness. Do not rerun automatically or claim authorization.
