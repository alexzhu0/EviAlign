# ActLumen Synthetic Data Access Lab

> 项目品牌：ActLumen · 明行。现有命令与包名保留 `agentharness`；[文档导航](README.md)与[能力范围](actlumen-brand-and-scope.md)提供当前入口。

ActLumen supplies pre-execution evidence correlation for a separate local
customer/order test lab. The external lab owns simulated identity,
authorization and actual reads of its synthetic in-memory SQLite database.

See the [lab specification](superpowers/specs/2026-09-14-data-access-lab-design.md).
The verifier can also be invoked as a module:

```bash
PYTHONPATH=src PYTHONDONTWRITEBYTECODE=1 \
  python3 -m agentharness.data_access_evidence_v1 < envelope.json
```

Input is one bounded `{request, evidence}` JSON envelope. The caller owns the
trusted expected request; the receipt binds its challenge, context, query,
authorization evidence and full-request digest. The report always preserves
`result_status: not_executed`; success is never runtime permission. This is not
identity authentication or signature verification. Existing Pi, shadow, audit
and file-bus CLI behavior is unchanged.

## Run the independent lab

The lab source is maintained as the sibling `agentharness-data-access-lab/`.
From that directory:

```bash
./run-lab test
./run-lab serve --port 8765 --enable-fixture-reads
```

Open `http://127.0.0.1:8765`. The lab README lists identities, questions and
expected results. The default Agent is an offline rule-based simulator;
this acceptance does not evaluate a real LLM.

Fixture-read mode only permits reads from a newly generated in-memory database
after independent fresh runtime authorization. Its execution records remain
external to ActLumen. Production identity, real databases and real-model
calls remain separate work.
