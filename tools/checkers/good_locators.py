def check(file_tree, tech, **kwargs):
    content = "\n".join(file_tree["py_files_content"].values())
    has_css = "By.CSS_SELECTOR" in content or ".locator(" in content
    has_xpath = "By.XPATH" in content or "xpath=" in content
    has_id = "By.ID" in content or "id=" in content
    return 1.0 if (has_css or has_xpath or has_id) else 0.0