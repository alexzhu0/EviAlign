"""Writable copies of the static Pi mapping fixtures for mutation tests."""

from contextlib import contextmanager
from collections.abc import Iterator
from pathlib import Path
import tempfile


@contextmanager
def temporary_payloads() -> Iterator[dict[str, Path]]:
    fixtures = Path(__file__).resolve().parents[1] / "examples" / "pi_tool_call_mapping"
    with tempfile.TemporaryDirectory() as tmpdir:
        paths = {
            "observations": Path(tmpdir) / "pi_tool_call_observations.json",
            "expectations": Path(tmpdir) / "expected_mapping.json",
        }
        for path in paths.values():
            path.write_text(
                (fixtures / path.name).read_text(encoding="utf-8"), encoding="utf-8"
            )
        yield paths
