import subprocess
import sys
from pathlib import Path

def try_run_tests(root: Path, tech):
    try:
        if tech["test_framework"] == "pytest":
            cmd = [sys.executable, "-m", "pytest", "--tb=short", "-v", "--maxfail=1"]
        else:
            cmd = [sys.executable, "-m", "unittest", "discover"]
        
        subprocess.run(cmd, cwd=root, timeout=60, capture_output=True, check=True)
        return {"success": True, "error": ""}
    except Exception as e:
        return {"success": False, "error": str(e)}