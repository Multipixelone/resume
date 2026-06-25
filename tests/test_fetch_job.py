import py_compile
from pathlib import Path


def test_fetch_job_compiles():
    script = Path(__file__).parent.parent / "scripts" / "fetch_job.py"
    assert script.exists()
    py_compile.compile(script, doraise=True)
