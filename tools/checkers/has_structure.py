def check(file_tree, tech, **kwargs):
    dirs = [d.lower() for d in file_tree["dirs"]]
    has_pages = any("page" in d for d in dirs)
    has_tests = any("test" in d for d in dirs)
    has_utils = any("util" in d or "helper" in d for d in dirs)
    score = 0.0
    if has_pages: score += 0.4
    if has_tests: score += 0.4
    if has_utils: score += 0.2
    return min(1.0, score)