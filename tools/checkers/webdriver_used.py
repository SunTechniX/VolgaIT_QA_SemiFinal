# tools/checkers/webdriver_used.py
def check(file_tree, tech, **kwargs):
    if tech["driver"] in ("Selenium", "Playwright"):
        return 1.0
    return 0.0