# Ponytail Cleanup Implementation Plan

> **For agentic workers:** Use Superpowers execution and independent code review.

**Goal:** Remove duplicated implementation and reviewer guidance while preserving
existing behavior.

**Architecture:** Keep the current evidence pipeline and public CLI. Share only
identical report-merging, bus-reference, and ledger-selection helpers. Use a
standard-library context manager for duplicated test setup.

**Tech Stack:** Python 3.10+, unittest, PyYAML, Markdown; no new dependencies.

**Spec:** The repository audit and conservative cleanup design approved in the
2026-09-14 conversation. Snapshot reuse and evaluator retirement remain separate
design decisions, not part of this behavior-preserving cleanup.

## Global Constraints

- Preserve CLI output, exit codes, ordering, error messages, and validation rules.
- Preserve `allow_candidate` as evidence only and `result_status: not_executed`.
- Do not modify the external runtime, fixtures, schemas, or historical releases.
- Preserve historical reviewer acceptance records in docs/14.
- Leave the pre-existing `.understand-anything/` directory untouched.
- Keep changes reviewable in the working tree; no publication or release.

## Task 1: Consolidate identical helpers

Files: `src/agentharness/validate.py`, `yamlio.py`, `loop_bus.py`,
`adapter_registry.py`, `execution_handoff.py`, `execution_preflight.py`,
`enterprise_audit_report.py`, `handoff_exporter.py`, `handoff_inspector.py`.

- [x] Run the existing full unittest suite as the refactoring baseline.
- [x] Capture representative CLI success/failure stdout, stderr, and exit codes
  outside the repository for exact comparison after the change.
- [x] Add `ValidationReport.merge(source, prefix=None)` using the existing two
  list-extension operations; a supplied prefix retains the literal `prefix.`.
  Replace the six identical prefixed and four unprefixed local merge helpers.
- [x] Move the identical path resolver to `yamlio.resolve_bus_reference` with
  the same `(Path | None, str | None)` return contract. Share all four identical
  resolver bodies (the exporter differs only in its parameter name); preserve
  caller-specific loading and error handling.
- [x] Move the identical handoff reference selector to
  `loop_bus.handoff_report_references(events)`, retaining order and duplicates.
  Use it from the inspector and exporter.
- [x] Run the affected existing regression modules; add no implementation-only
  tests for these behavior-preserving extractions.

## Task 2: Simplify test setup

Files: `tests/pi_mapping_fixtures.py`, `tests/test_pi_tool_call_mapping.py`,
`tests/test_pi_tool_call_mapping_cli.py`.

- [x] Replace both `_temporary_payloads` classes with a shared context manager:
  `with tempfile.TemporaryDirectory() as tmpdir`, copy the two UTF-8 fixture
  documents into that directory, then `yield` the same paths dictionary.
- [x] Preserve all existing test assertions and run both Pi mapping modules.

## Task 3: Consolidate reviewer guidance

Files: `docs/10-enterprise-audit-report-and-buyer-demo.md`,
`docs/11-reproducible-enterprise-demo.md`,
`docs/12-buyer-reviewer-decision-guide.md`,
`docs/13-external-reviewer-checklist.md`.

- [x] Keep docs/10 for audit contract details, docs/11 for commands and expected
  fixture outputs, docs/12 for decision meanings, and docs/13 for the R1–R14 rubric.
- [x] Replace repeated walkthroughs, command flows, and boundary lists with
  links to those sections and the normative docs/08 product contract.
- [x] Preserve unique technical details and check local links and anchors.

## Acceptance

- [x] Run all six verification commands from AGENTS.md without Python bytecode.
- [x] Compare captured CLI outputs exactly; run the six-module evidence suite
  from docs/29 if evidence-contract implementation changes become necessary.
- [x] Obtain independent code review and address actionable findings.
- [x] Report actual line reduction, test results, and deferred architectural work.

## Verification Record

Baseline: 515 tests passed. Final full suite: 515 tests passed. The affected
106-test subset and both Pi direct-script entry points (19 and 10 tests) passed.
All 21 captured CLI outcomes matched exit code, stdout, and stderr exactly;
43 local documentation links/anchors resolved. Required policy, three smoke
evaluations, both loop checks, and whitespace checks passed. Independent review
identified one direct-script import regression, which was fixed and re-reviewed.

Worktree creation was blocked by local Git metadata permissions; changes remain
in the original working tree, without a commit, push, release, or runtime action.
