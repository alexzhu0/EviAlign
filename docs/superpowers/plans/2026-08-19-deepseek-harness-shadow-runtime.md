# DeepSeek Harness Shadow Runtime Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and locally run a pinned DeepSeek Harness plugin that captures one real Flash synthetic-tool intent without exposing filesystem, shell, network, delegation, or business-tool execution.

**Architecture:** A dedicated external checkout at `/home/alex/DTAlex/learningGitHub/deepseek-harness-shadow` is pinned to the official Harness commit `99f6f02fecdb7dff40c3fbc9470f5907c29f74ca`. Its `shadow-plugin` contains a single tool interceptor and a local launcher; it emits one bounded observation to stdout for AgentHarness's separate verifier and never writes credentials or raw model content.

**Tech Stack:** DeepSeek Harness / Cordis, Node.js, pnpm, TypeScript, `@deepseek-ai/dsh-tools`, DeepSeek API model `deepseek-v4-flash`, Node test runner supplied by the pinned checkout.

## Global Constraints

- This is a separate repository and branch: never stage, commit, or release any AgentHarness file from this checkout, and never vendor the Harness into AgentHarness.
- Pin exactly `99f6f02fecdb7dff40c3fbc9470f5907c29f74ca`; if the clone cannot reach that object, stop before dependency install or API use.
- The model is exactly `deepseek-v4-flash`; thinking is disabled; at most 3 requests, 256 output tokens each, and one tool call are permitted.
- The model-visible catalog contains exactly `inspect_policy_summary`; no filesystem, terminal, shell, network, MCP, delegation, skill, workflow, editor, or business tool is visible or callable.
- The synthetic tool never reads a workspace, calls an adapter, dispatches, mutates, retries, or executes an external operation. Its only result is `{ "status": "shadow_observed", "executed": false }`.
- Load only `DEEPSEEK_API_KEY` from the protected AgentHarness `.env` through a launcher that parses the one required assignment without shell-sourcing it; never print it, pass it on the command line, write it to config, or commit it.
- Observation JSON is at most 8192 UTF-8 bytes, has the exact `runtime-shadow-observation-v1` shape from the approved design, and always uses `execution_attempted:false` and `result_status:"not_executed"`.
- A provider error, timeout, non-Flash route, any extra/invalid tool call, unexpected output, or AgentHarness rejection is a failed PoC. There is no retry loop and no CI/scheduled/production execution.

---

## File Structure

All following paths are in the external checkout, not this AgentHarness repo:

- `shadow-plugin/src/runtime-shadow.ts`: one Cordis `defineTool` registration and in-memory observation capture.
- `shadow-plugin/src/observation.ts`: canonical bounded observation builder and redaction checks.
- `shadow-plugin/src/load-key.ts`: literal `.env` assignment reader; it returns a child-process environment map and never logs a value.
- `shadow-plugin/src/run-shadow.ts`: one-shot launcher, quota enforcement, stdout observation emission, and nonzero failures.
- `shadow-plugin/cordis.patch.yml`: profile layer that mounts the shadow plugin and explicitly disables every inherited execution-capable or model-facing tool row except `inspect_policy_summary`.
- `shadow-plugin/profile-package.json`: checked-in profile manifest template; it declares the official base/headless bundles plus the local synthetic-tool bundle.
- `shadow-plugin/package.json` and `shadow-plugin/tsconfig.json`: local plugin scripts and pinned checkout workspace dependencies.
- `shadow-plugin/tests/*.spec.ts`: offline plugin, observation, key-loader, and launch-policy tests.
- `shadow-plugin/README.md`: local-only setup and explicit non-authorization boundary.

### Task 1: Pin the external checkout and prove the closed tool catalog

**Files:**
- Create external checkout: `/home/alex/DTAlex/learningGitHub/deepseek-harness-shadow`
- Create: `shadow-plugin/cordis.patch.yml`
- Create: `shadow-plugin/profile-package.json`
- Create: `shadow-plugin/package.json`
- Create: `shadow-plugin/tests/profile.spec.ts`

**Interfaces:**
- Consumes official repository commit `99f6f02fecdb7dff40c3fbc9470f5907c29f74ca` and `dsh --dump-config`.
- Produces a reproducible profile overlay whose parsed tool names are exactly `["inspect_policy_summary"]`.

- [ ] **Step 1: Create the isolated external checkout**

```bash
git clone https://github.com/deepseek-ai/deepseek-harness.git /home/alex/DTAlex/learningGitHub/deepseek-harness-shadow
git -C /home/alex/DTAlex/learningGitHub/deepseek-harness-shadow checkout --detach 99f6f02fecdb7dff40c3fbc9470f5907c29f74ca
git -C /home/alex/DTAlex/learningGitHub/deepseek-harness-shadow switch -c agentharness-shadow-poc
```

Before writing code, verify `git rev-parse HEAD` equals the pinned SHA and read
that checkout's `AGENTS.md`. If either condition fails, stop and report the
blocker; do not substitute `master`.

Create the Harness profile under an external-only `DSH_HOME`; do not run the
Harness from the AgentHarness checkout, where its credential resolver could
discover AgentHarness's `.env`:

```bash
mkdir -p .dsh-shadow-home
DSH_HOME="$PWD/.dsh-shadow-home" pnpm dsh plugin --profile agentharness-shadow add ./shadow-plugin
```

Copy `shadow-plugin/profile-package.json` over the generated profile
`package.json` after the add command has created its local dependency link.
The template's `dsh.profile.bundles` order is
`["@deepseek-ai/dsh-base", "@deepseek-ai/dsh-headless", "agentharness-shadow-plugin"]`.
This uses the official headless runner (no Web/HTTP host) while retaining a
profile patch layer that can explicitly close base capabilities.

- [ ] **Step 2: Write a failing profile-surface test**

```ts
it('exposes exactly the synthetic shadow tool', async () => {
  const dump = await dumpComposedProfile('agentharness-shadow')
  const toolNames = await bootWithNoProviderAndListTools('agentharness-shadow')
  expect(toolNames).toEqual(['inspect_policy_summary'])
  expect(toolNames).not.toContain('bash')
  expect(toolNames).not.toContain('str_replace_editor')
  expect(toolNames).not.toContain('web_search')
})
```

Implement `dumpComposedProfile` by invoking the pinned checkout's
`pnpm dsh --profile agentharness-shadow --dump-config` with the external-only
`DSH_HOME`, then parse YAML through the checkout's existing test utilities.
Implement `bootWithNoProviderAndListTools` using the checkout's profile boot
test helper and a no-provider/no-task stub; it must make no network request
and use no credential. The test must inspect the composed profile, not just the
text of the patch file. It also asserts disabled capability rows and the
one-model request configuration described in Step 4.

- [ ] **Step 3: Verify RED**

Run from the external checkout:

```bash
pnpm install --frozen-lockfile
pnpm exec vitest run shadow-plugin/tests/profile.spec.ts
```

Expected: the test fails because the shadow overlay and synthetic tool do not
exist; do not make an API request.

- [ ] **Step 4: Implement the closed overlay**

Create the plugin package with a `dsh.bundle.patch` pointing to
`shadow-plugin/cordis.patch.yml`; its patch mounts the plugin row below and
disables every listed inherited capability row. The dependency's bundle layer
is applied after base/headless, so it is the final capability policy.

```yaml
- insert:
    - id: agentharness-shadow-tool
      name: agentharness-shadow-plugin
      inject: [tools]

- id: subprocess
  disabled: true
- id: sandbox
  disabled: true
- id: bash-sandbox
  disabled: true
- id: pwsh-sandbox
  disabled: true
- id: tool-bash
  disabled: true
- id: tool-pwsh
  disabled: true
- id: tool-jobs
  disabled: true
- id: fs-sandbox
  disabled: true
- id: tool-fs
  disabled: true
- id: tool-fs-search
  disabled: true
- id: tool-skill
  disabled: true
- id: tool-subagent-control
  disabled: true
- id: tool-subagent-list-agents
  disabled: true
- id: tool-subagent
  disabled: true
- id: tool-subagent-fork
  disabled: true
- id: tool-subagent-report
  disabled: true
- id: tool-workflow
  disabled: true
- id: tool-todo
  disabled: true
- id: tool-goal
  disabled: true
- id: tool-ralph
  disabled: true
- id: tool-str-replace-editor
  disabled: true
- id: web
  disabled: true
- id: tool-web
  disabled: true
- id: llm-retry
  disabled: true
- id: session-title-llm
  disabled: true
- id: compaction-basic
  disabled: true
- id: llm-deepseek
  config:
    thinking: disabled
    maxTokens: 256
    streamIdleTimeoutMs: 60000
    models:
      - id: deepseek-v4-flash
        name: DeepSeek-V4-Flash
        maxTokens: 256
- id: agent-default-model
  config:
    provider: deepseek-official
    model: deepseek-v4-flash
```

The test must additionally assert that every capability ID above marked
`disabled` has `disabled: true` in the composed dump, that no active row name
begins `@deepseek-ai/dsh-tool-`,
that the `llm-deepseek` row locks `thinking: disabled` and `maxTokens: 256`,
and that the registry's exported tool names are exactly the synthetic tool.
If any required service dependency prevents boot after disabling a row, stop:
do not silently re-enable it. Amend the profile only with a reviewed minimal
replacement that still proves the registry and active service assertions.

- [ ] **Step 5: Verify GREEN and commit external profile setup**

Run:

```bash
pnpm exec vitest run shadow-plugin/tests/profile.spec.ts
DSH_HOME="$PWD/.dsh-shadow-home" pnpm dsh --profile agentharness-shadow --dump-config > /tmp/dsh-shadow-config.json
git diff --check
```

Expected: exact one-tool assertion passes and config dump contains no terminal,
filesystem, MCP, web, delegation, or workflow tool name.

```bash
git add shadow-plugin/cordis.patch.yml shadow-plugin/profile-package.json shadow-plugin/package.json shadow-plugin/tests/profile.spec.ts
git diff --cached --check
git commit -m "feat: add closed shadow runtime profile"
```

### Task 2: Synthetic tool, canonical observation, and credential isolation

**Files:**
- Create: `shadow-plugin/src/runtime-shadow.ts`
- Create: `shadow-plugin/src/observation.ts`
- Create: `shadow-plugin/src/load-key.ts`
- Create: `shadow-plugin/tests/runtime-shadow.spec.ts`
- Create: `shadow-plugin/tests/observation.spec.ts`
- Create: `shadow-plugin/tests/load-key.spec.ts`

**Interfaces:**
- Consumes an AgentHarness `shadow-request-v1` JSON object and `DEEPSEEK_API_KEY` only as a child-process environment value.
- Produces `buildObservation(request, toolCall, runtimeRevision): RuntimeShadowObservation` and `registerShadowTool(ctx, request, capture): void`.

- [ ] **Step 1: Write failing offline behavior tests**

```ts
it('records one matching call and returns only the non-executing response', async () => {
  const result = await executeSyntheticTool({
    challenge: 'a'.repeat(64),
    policy_scope: 'agentharness-shadow-poc',
  })
  expect(result).toEqual({ status: 'shadow_observed', executed: false })
  expect(captured.execution_attempted).toBe(false)
  expect(captured.result_status).toBe('not_executed')
})

it.each([
  ['changed challenge', { challenge: 'b'.repeat(64), policy_scope: 'agentharness-shadow-poc' }],
  ['extra argument', { challenge: 'a'.repeat(64), policy_scope: 'agentharness-shadow-poc', path: '/tmp/x' }],
])('rejects %s without emitting an observation', async (_name, args) => {
  await expect(executeSyntheticTool(args)).rejects.toThrow('shadow.binding_invalid')
  expect(capture).toHaveLength(0)
})
```

Add key-loader cases for missing key, key with newline/control character, key
line after a duplicate key assignment, non-key `.env` line, and `sk-` value
that never appears in an error or returned object.

- [ ] **Step 2: Verify RED**

Run: `pnpm exec vitest run shadow-plugin/tests/runtime-shadow.spec.ts shadow-plugin/tests/observation.spec.ts shadow-plugin/tests/load-key.spec.ts`

Expected: FAIL because no shadow tool/builder/key loader exists.

- [ ] **Step 3: Implement only the bounded synthetic behavior**

Register `inspect_policy_summary` with parameters exactly `challenge` (required
64-lowercase-hex string) and `policy_scope` (required literal), with no
additional properties. Define that schema as one checked-in canonical JSON
literal; calculate its sorted-compact UTF-8 SHA-256 and reject a request whose
`tool_schema_digest` differs before model startup. The tool validates one
matching call, captures no raw model message, and returns the fixed
non-executing JSON value. `buildObservation` allows only the exact fields/limits
in the approved design, computes sorted compact UTF-8 SHA-256 argument digest
and request-derived opaque correlation ID, and rejects any credential-like
value, forbidden key, absolute path, or byte count above 8192.

`load-key.ts` must read the specified `.env` as UTF-8 text, select exactly one
literal `DEEPSEEK_API_KEY=<value>` line, reject duplicates and controls, and
return `{ DEEPSEEK_API_KEY: value }` to the child launcher. It must never use
`source`, `eval`, shell expansion, console logging, or a saved configuration
file. The launcher starts the child from the external checkout with an
external-only `DSH_HOME`, a cleared inherited environment, and only
`DEEPSEEK_API_KEY`, `DSH_HOME`, `DSH_TELEMETRY_DISABLED=1`, `PATH`, and
platform-required locale variables. It must reject a current working directory
or DSH_HOME nested inside the AgentHarness repository, and reject any `.env`
in the external checkout or external DSH_HOME before starting Harness.

- [ ] **Step 4: Verify GREEN and commit plugin behavior**

Run:

```bash
pnpm exec vitest run shadow-plugin/tests/runtime-shadow.spec.ts shadow-plugin/tests/observation.spec.ts shadow-plugin/tests/load-key.spec.ts
rg -n 'console\.log|DEEPSEEK_API_KEY|source\(|eval\(' shadow-plugin/src
git diff --check
```

Expected: tests pass; the search shows no key logging or dynamic shell loading.

```bash
git add shadow-plugin/src shadow-plugin/tests
git diff --cached --check
git commit -m "feat: capture bounded shadow tool observations"
```

### Task 3: One-shot PoC launcher and acceptance run

**Files:**
- Create: `shadow-plugin/src/run-shadow.ts`
- Create: `shadow-plugin/tests/run-shadow.spec.ts`
- Create: `shadow-plugin/README.md`

**Interfaces:**
- Consumes `request.json` from AgentHarness, the protected absolute `.env` path supplied only by the local operator, and the pinned runtime revision.
- Produces exactly one `runtime-shadow-observation-v1` JSON document on stdout, or a bounded nonzero failure on stderr without credentials/prompt/response/path.

- [ ] **Step 1: Write failing launcher-policy tests**

```ts
it('refuses more than three requested attempts before provider startup', async () => {
  const outcome = await runShadow({ request, maxRequests: 4 })
  expect(outcome).toEqual({ ok: false, code: 'shadow.request_limit' })
  expect(provider.calls).toHaveLength(0)
})

it('passes only Flash, disabled thinking, maxTokens 256, and the synthetic tool', async () => {
  await runShadow({ request, maxRequests: 1 })
  expect(provider.calls[0]).toMatchObject({
    model: 'deepseek-v4-flash', thinking: 'disabled', maxTokens: 256,
  })
  expect(provider.calls[0].tools.map((tool: { name: string }) => tool.name))
    .toEqual(['inspect_policy_summary'])
})
```

- [ ] **Step 2: Verify RED**

Run: `pnpm exec vitest run shadow-plugin/tests/run-shadow.spec.ts`

Expected: FAIL because the launcher does not exist; no provider credential is
loaded by this test.

- [ ] **Step 3: Implement one-shot launcher and README**

The launcher accepts only a request-file descriptor and operator-supplied
protected `.env` path, validates the request before loading the key, then
launches the pinned `dsh` binary under the closed `agentharness-shadow` profile
for at most one model call in the first acceptance run. Its child stdout and
stderr are bounded in memory and are never forwarded or written: the launcher
discards the raw final answer/transcript and emits only the captured canonical
observation. It configures only Flash/non-thinking/256 tokens and the single
tool, waits for a matching capture, prints one compact observation to stdout,
and exits nonzero for every other outcome. It does not write raw transcripts,
retries, or sessions. It must reject a child config dump that is not the
Task-1-approved one before it makes the provider request.

Document the exact two-repository command sequence, including piping the
observation to AgentHarness `shadow verify`; state that a successful result is
evidence-only and not runtime authorization.

- [ ] **Step 4: Verify GREEN, then perform the one authorized live run**

Run offline first:

```bash
pnpm exec vitest run shadow-plugin/tests/run-shadow.spec.ts
pnpm exec vitest run shadow-plugin/tests
git diff --check
```

Only if all offline tests pass, the key loader succeeds, and the local operator
again confirms the 3-request/256-token cap, run one invocation. Save the
observation only to a Git-ignored temporary file, then run AgentHarness:

```bash
./agentharness shadow verify request.json < /tmp/runtime-shadow-observation.json
```

Expected: the external process emits one bounded observation; AgentHarness
returns `ok:true` and `result_status:"not_executed"`. Any other output is a
failed PoC and is not retried automatically.

- [ ] **Step 5: Commit external runtime code and perform final reviews**

```bash
git add shadow-plugin/src/run-shadow.ts shadow-plugin/tests/run-shadow.spec.ts shadow-plugin/README.md
git diff --cached --check
git commit -m "feat: run bounded DeepSeek shadow PoC"
```

Invoke `superpowers:requesting-code-review` in the external checkout. Resolve
Critical/Important findings, run its full offline suite, and retain the external
checkout for review. Do not push or publish it until the operator separately
chooses an external-repository publishing action.
