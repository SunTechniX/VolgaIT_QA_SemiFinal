def check(file_tree, tech, **kwargs):
    content = "\n".join(file_tree["py_files_content"].values())
    has_page_class = any("class " in c and ("Page" in c or "page" in c.lower()) for c in file_tree["py_files_content"].values())
    has_base_page = "BasePage" in content
    return 1.0 if has_page_class and has_base_page else 0.0