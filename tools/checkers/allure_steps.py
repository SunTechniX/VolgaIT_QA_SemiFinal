# tools/checkers/allure_steps.py
import ast

def check(file_tree, tech, **kwargs):
    py_content = file_tree.get("py_files_content", {})
    total_step_calls = 0
    total_non_test_funcs = 0
    total_test_funcs = 0

    for content in py_content.values():
        try:
            tree = ast.parse(content)
        except:
            continue

        for node in ast.walk(tree):
            # Считаем все функции
            if isinstance(node, ast.FunctionDef):
                if node.name.startswith("test_"):
                    total_test_funcs += 1
                else:
                    total_non_test_funcs += 1

            # Считаем @allure.step как декоратор
            if isinstance(node, ast.FunctionDef):
                for deco in node.decorator_list:
                    name = _get_decorator_name(deco)
                    if name == "allure.step":
                        total_step_calls += 1

            # Считаем with allure.step(...)
            if isinstance(node, ast.With):
                for item in node.items:
                    if hasattr(item, 'context_expr'):
                        expr = item.context_expr
                        if (isinstance(expr, ast.Call) and
                            isinstance(expr.func, ast.Attribute) and
                            expr.func.attr == "step" and
                            _get_attr_base(expr.func.value) == "allure"):
                            total_step_calls += 1

    # Ожидаем минимум: 1 шаг на каждые 2 функции (тестовых или нет)
    total_funcs = total_test_funcs + total_non_test_funcs
    if total_funcs == 0:
        return 1.0 if total_step_calls > 0 else 0.0

    expected = max(1, total_funcs // 2)
    return min(1.0, total_step_calls / expected)

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

def _get_attr_base(node):
    while isinstance(node, ast.Attribute):
        node = node.value
    if isinstance(node, ast.Name):
        return node.id
    return ""