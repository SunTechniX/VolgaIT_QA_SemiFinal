from pathlib import Path

def safe_read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding="utf-8-sig")
        except:
            return path.read_text(encoding="latin1", errors="ignore")

def detect_tech_stack(root: Path):
    imports = set()
    content = ""
    for py in root.rglob("*.py"):
        try:
            txt = safe_read_text(py)
            content += txt + "\n"
            for line in txt.splitlines():
                stripped = line.strip()
                if stripped.startswith(("import ", "from ")):
                    imports.add(stripped)
        except:
            pass

    reqs = ""
    req_file = root / "requirements.txt"
    if req_file.exists():
        reqs = safe_read_text(req_file).lower()

    tech = {
        "imports": list(imports),  # ← БЫЛО set → СТАЛО list
        "content": content,
        "requirements": reqs,
        "test_framework": "pytest" if "pytest" in content or "pytest" in reqs else "unittest",
        "driver": None,
        "allure": "allure" in content or "allure" in reqs
    }

    if "selenium" in content or "selenium" in reqs:
        tech["driver"] = "Selenium"
    elif "playwright" in content or "playwright" in reqs:
        tech["driver"] = "Playwright"

    return tech