import shutil
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


def test_manuscript_numbers_match_mem_outputs():
    subprocess.run(
        [sys.executable, "tests/verify_manuscript_numbers.py"],
        cwd=ROOT,
        check=True,
    )


def test_mem_core_outputs_exist():
    required = [
        "data/mem_summary.json",
        "data/mem_velocity_full.csv",
        "data/mem_decay_full.csv",
        "data/mem_integrated_full.csv",
        "data/mem_extended_stats.json",
        "index.html",
    ]
    missing = [path for path in required if not (ROOT / path).exists()]
    assert missing == []


def test_r_verification_passes_when_rscript_is_available():
    rscript = shutil.which("Rscript")
    if rscript is None:
        pytest.skip("Rscript is not installed in this environment")
    subprocess.run([rscript, "tests/run_tests.R"], cwd=ROOT, check=True)
