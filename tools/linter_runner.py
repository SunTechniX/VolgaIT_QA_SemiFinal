import subprocess
import sys
from pathlib import Path

def run_linters(root: Path):
    result = {"ruff_errors": 0, "flake8_errors": 0, "pylint_score": 0.0}

    # Ruff
    try:
        out = subprocess.run([sys.executable, "-m", "ruff", "check", "."], cwd=root, capture_output=True, text=True)
        result["ruff_errors"] = len([l for l in out.stdout.splitlines() if ":" in l])
    except:
        pass

    # Flake8
    try:
        out = subprocess.run([sys.executable, "-m", "flake8", "."], cwd=root, capture_output=True, text=True)
        result["flake8_errors"] = len(out.stdout.strip().splitlines()) if out.stdout.strip() else 0
    except:
        pass

    # PyLint (на один случайный .py файл)
    try:
        py_files = list(root.rglob("*.py"))
        if py_files:
            out = subprocess.run([sys.executable, "-m", "pylint", str(py_files[0]), "--exit-zero"], cwd=root, capture_output=True, text=True)
            for line in out.stdout.splitlines():
                if "rated at" in line:
                    score = float(line.split("rated at ")[1].split("/")[0])
                    result["pylint_score"] = score
                    break
    except:
        pass

    return result