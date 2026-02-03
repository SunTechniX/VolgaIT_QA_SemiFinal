def detect_tech_stack(root):
    imports = set()
    content = ""
    for py in root.rglob("*.py"):
        try:
            txt = py.read_text(encoding="utf-8", errors="ignore")
            content += txt + "\n"
            if "import " in txt or "from " in txt:
                for line in txt.splitlines():
                    if line.strip().startswith(("import ", "from ")):
                        imports.add(line.strip())
        except:
            pass

    reqs = ""
    if (root / "requirements.txt").exists():
        reqs = (root / "requirements.txt").read_text().lower()

    tech = {
        "imports": imports,
        "content": content,
        "requirements": reqs,
        "test_framework": "pytest" if "pytest" in content or "pytest" in reqs else "unittest",
        "driver": None,
        "allure": "allure" in content or "allure" in reqs
    }

    if "from selenium" in content or "import selenium" in content or "selenium" in reqs:
        tech["driver"] = "Selenium"
    elif "from playwright" in content or "playwright" in reqs:
        tech["driver"] = "Playwright"

    return tech