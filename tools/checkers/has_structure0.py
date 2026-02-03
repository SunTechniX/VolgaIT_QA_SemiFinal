def check(file_tree, tech, **kwargs):
    dirs = set(file_tree.get("dirs", []))
    has_pages = any("pages" in d.lower() or "page" in d.lower() for d in dirs)
    has_tests = any("test" in d.lower() for d in dirs)
    has_utils = any("util" in d.lower() or "helper" in d.lower() for d in dirs)
    
    score = 0.0
    if has_pages: score += 0.4
    if has_tests: score += 0.4
    if has_utils: score += 0.2
    return min(1.0, score)