# tools/checkers/allure_metadata.py
import ast

def _get_decorator_name(node):
    """Рекурсивно получает полное имя декоратора: allure.feature → 'allure.feature'"""
    if isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Attribute):
        parts = []
        cur = node
        while isinstance(cur, ast.Attribute):
            parts.append(cur.attr)
            cur = cur.value
        if isinstance(cur, ast.Name):
            parts.append(cur.id)
        return ".".join(reversed(parts))
    elif isinstance(node, ast.Call):
        return _get_decorator_name(node.func)
    return ""

def check(file_tree, tech, **kwargs) -> float:
    """
    Оценивает покрытие тестовых функций метаданными Allure:
    - Учитываются @allure.feature, @story, @severity, @epic
    - Не учитываются @allure.step и просто @allure
    """
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
                    # Считаем всё, что начинается с allure., кроме step
                    if name.startswith("allure.") and name not in ("allure.step", "allure"):
                        has_meta = True
                        break
                if has_meta:
                    tests_with_meta += 1

    if total_tests == 0:
        return 1.0  # нет тестов → критерий не применим → полный балл
    return min(1.0, tests_with_meta / total_tests)