def check(file_tree, tech, **kwargs):
    if ".gitignore" not in file_tree["files"]:
        return 0.0
    gitignore = Path(".gitignore")
    if not gitignore.exists():
        return 0.0
    text = gitignore.read_text()
    good = any(x in text for x in ["__pycache__", ".venv", "allure-results", "*.log"])
    return 1.0 if good else 0.3