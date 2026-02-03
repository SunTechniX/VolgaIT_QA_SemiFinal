# tools/checkers/has_screenshots.py
def check(file_tree, tech, **kwargs) -> float:
    content = "\n".join(file_tree.get("py_files_content", {}).values())
    # Ищем признаки скриншотов
    if "get_screenshot_as_png" in content or "save_screenshot" in content:
        return 1.0
    return 0.0