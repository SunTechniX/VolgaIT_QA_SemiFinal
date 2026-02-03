def check(file_tree, tech, **kwargs):
    content = "\n".join(file_tree["py_files_content"].values())
    reqs = tech["requirements"]
    has_xdist = "pytest-xdist" in reqs or "-n " in content or "addopts = -n" in content
    return 1.0 if has_xdist else 0.0