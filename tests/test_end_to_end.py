import pytest
import subprocess
import os
import sys

@pytest.mark.skipif(os.environ.get("SKIP_E2E"), reason="Takes minutes to run full pipeline")
def test_end_to_end_cli_flows():
    python_bin = sys.executable

    res = subprocess.run([python_bin, "scripts/build_company.py", "--company", "TCS", "--year", "2024"], capture_output=True, text=True)
    assert res.returncode == 0, f"Build Failed: {res.stderr}"
    
    res_ask = subprocess.run(
        [python_bin, "scripts/ask.py", "--company", "TCS", "--year", "2024", "--question", "Who is the Chairman?", "--debug"],
        capture_output=True, text=True
    )
    assert res_ask.returncode == 0, f"Ask Failed: {res_ask.stderr}"
    assert "Dense Results:" in res_ask.stdout
    assert "Context Blocks:" in res_ask.stdout
    
    res_eval = subprocess.run([python_bin, "scripts/evaluate.py"], capture_output=True, text=True)
    assert res_eval.returncode == 0, f"Eval Failed: {res_eval.stderr}"
