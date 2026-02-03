def check(file_tree, tech, **kwargs):
    if not tech["allure"]:
        return 0.0
    content = "\n".join(file_tree["py_files_content"].values())
    has_step = "@allure.step" in content
    has_feature = "@allure.feature" in content or "@allure.story" in content
    if has_step and has_feature:
        return 1.0
    elif has_step:
        return 0.5
    return 0.0