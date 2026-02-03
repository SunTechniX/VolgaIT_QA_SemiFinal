# tools/checkers/allure_metadata.py
import ast

def check(file_tree, tech, **kwargs):
    py_content = file_tree.get("py_files_content", {})
    total_tests = 0
    tests_with_meta = 0

    for content in py_content.values():
        try:
            tree = ast.parse(content)
        except:
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                total_tests += 1
                has_meta = False
                for deco in node.decorator_list:
                    name = _get_decorator_name(deco)
                    if name.startswith("allure.") and name != "allure.step":
                        has_meta = True
                        break
                if has_meta:
                    tests_with_meta += 1

    if total_tests == 0:
        return 1.0
    return min(1.0, tests_with_meta / total_tests)

def _get_decorator_name(deco):
    if isinstance(deco, ast.Name):
        return deco.id
    elif isinstance(deco, ast.Attribute):
        parts = []
        cur = deco
        while isinstance(cur, ast.Attribute):
            parts.append(cur.attr)
            cur = cur.value
        if isinstance(cur, ast.Name):
            parts.append(cur.id)
        return ".".join(reversed(parts))
    elif isinstance(deco, ast.Call):
        return _get_decorator_name(deco.func)
    return ""