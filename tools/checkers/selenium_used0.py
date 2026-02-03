def check(file_tree, tech, **kwargs):
    """Проверяет использование Selenium WebDriver"""
    if "selenium" in tech["imports"]:
        return 1.0
    if any("from selenium" in content or "import selenium" in content
           for content in file_tree.get("py_files_content", {}).values()):
        return 1.0
    return 0.0