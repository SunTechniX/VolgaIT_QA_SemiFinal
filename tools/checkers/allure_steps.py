# tools/checkers/allure_steps.py
import ast

def _get_decorator_name(node):
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

def _get_attr_base(node):
    """Получает базовое имя атрибута: allure.step → 'allure'"""
    while isinstance(node, ast.Attribute):
        node = node.value
    if isinstance(node, ast.Name):
        return node.id
    return ""

def check(file_tree, tech, **kwargs) -> float:
    """
    Оценивает использование шагов Allure:
    - Считает @allure.step (как декоратор)
    - Считает with allure.step(...)
    - База для нормализации: количество НЕ-тестовых функций (def ... кроме test_*)
    """
    py_content = file_tree.get("py_files_content", {})
    total_step_calls = 0
    total_non_test_funcs = 0
    total_test_funcs = 0

    for content in py_content.values():
        try:
            tree = ast.parse(content)
        except:
            continue

        # Проходим по всем узлам
        for node in ast.walk(tree):
            # Подсчёт всех функций
            if isinstance(node, ast.FunctionDef):
                if node.name.startswith("test_"):
                    total_test_funcs += 1
                else:
                    total_non_test_funcs += 1

            # Подсчёт @allure.step как декоратора
            if isinstance(node, ast.FunctionDef):
                for deco in node.decorator_list:
                    name = _get_decorator_name(deco)
                    if name == "allure.step":
                        total_step_calls += 1

            # Подсчёт with allure.step(...)
            if isinstance(node, ast.With):
                for item in node.items:
                    if hasattr(item, 'context_expr'):
                        expr = item.context_expr
                        if (isinstance(expr, ast.Call) and
                            isinstance(expr.func, ast.Attribute) and
                            expr.func.attr == "step" and
                            _get_attr_base(expr.func.value) == "allure"):
                            total_step_calls += 1

    # Если вообще нет функций — ориентируемся на наличие хотя бы одного шага
    if total_non_test_funcs == 0:
        return 1.0 if total_step_calls > 0 else 0.0

    # Ожидаем минимум: 1 шаг на каждые 2 не-тестовые функции
    expected_steps = max(1, total_non_test_funcs // 2)
    ratio = total_step_calls / expected_steps
    return min(1.0, ratio)