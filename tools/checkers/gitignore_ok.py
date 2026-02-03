# tools/checkers/gitignore_ok.py
from pathlib import Path

def check(file_tree, tech, **kwargs) -> float:
    files = file_tree.get("files", [])
    if ".gitignore" not in files:
        return 0.0
    
    gitignore_path = Path(".gitignore")
    if not gitignore_path.exists():
        return 0.0

    try:
        text = gitignore_path.read_text(encoding="utf-8")
    except:
        try:
            text = gitignore_path.read_text(encoding="utf-8-sig")
        except:
            return 0.0

    # Проверяем наличие типичных исключений
    good_patterns = ["__pycache__", ".venv", "allure-results", "*.log", "results/"]
    found = any(pattern in text for pattern in good_patterns)
    return 1.0 if found else 0.3