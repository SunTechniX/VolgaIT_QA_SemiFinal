def check(file_tree, tech, **kwargs):
    content = "\n".join(file_tree["py_files_content"].values())
    has_wait_class = "class Wait" in content or "class WebDriverWait" in content
    has_explicit = "WebDriverWait" in content or "expect(" in content
    return 1.0 if has_wait_class else (0.5 if has_explicit else 0.0)