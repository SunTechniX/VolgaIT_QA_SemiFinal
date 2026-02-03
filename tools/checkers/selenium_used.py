def check(file_tree, tech, **kwargs):
    return 1.0 if tech["driver"] == "Selenium" else 0.0