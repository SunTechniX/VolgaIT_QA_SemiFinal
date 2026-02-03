def check(file_tree, tech, **kwargs):
    return 1.0 if tech["driver"] == "Playwright" else 0.0