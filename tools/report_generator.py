import json
import sys
from pathlib import Path

def format_tree(tree, prefix=""):
    lines = []
    items = sorted(tree.items())
    for i, (name, subtree) in enumerate(items):
        is_last = i == len(items) - 1
        lines.append(f"{prefix}{'└── ' if is_last else '├── '}{name}")
        if isinstance(subtree, dict):
            ext = "    " if is_last else "│   "
            lines.extend(format_tree(subtree, prefix + ext))
    return lines

def main():
    with open(sys.argv[1]) as f:
        data = json.load(f)

    lines = []
    lines.append("## 📊 Автоматическая оценка QA-проекта\n")

    # Дерево
    lines.append("### 🗂 Структура проекта")
    tree_lines = format_tree(data["file_tree"]["tree"])
    lines.extend(["```", *tree_lines, "```\n"])

    # Технологии
    tech = data["tech_stack"]
    lines.append("### ⚙️ Обнаруженные технологии")
    lines.append(f"- **Тестовый фреймворк**: {tech.get('test_framework', '—')}")
    lines.append(f"- **Драйвер**: {tech.get('driver', '—')}")
    lines.append(f"- **Allure**: {'✅' if tech.get('allure') else '❌'}")
    lines.append("")

    # Критерии
    lines.append("### 🎯 Оценка по критериям")
    lines.append("| Критерий | Балл | Макс. | Статус |")
    lines.append("|----------|------|-------|--------|")
    for cid, info in data["criteria"].items():
        score = info["score"]
        max_s = info["weight"]
        status = "✅" if score >= max_s * 0.9 else ("⚠️" if score > 0 else "❌")
        lines.append(f"| `{cid}`<br>{info['name']} | {score} | {max_s} | {status} |")
    s = data["summary"]
    lines.append(f"| **ИТОГО** | **{s['total']}** | **{s['max']}** | **{s['percent']}%** |")
    # lines.append(f"\n**Итого**: {s['total']} / {s['max']} ({s['percent']}%)")

    # Линтеры
    lint = data["linters"]
    lines.append("\n### 🔍 Линтеры")
    lines.append(f"- **Ruff**: {lint['ruff_errors']} ошибок")
    lines.append(f"- **Flake8**: {lint['flake8_errors']} ошибок")
    lines.append(f"- **PyLint**: {lint['pylint_score']}/10")

    # Исполняемость
    exec_res = data["execution"]
    lines.append("\n### ▶️ Запуск тестов")
    if exec_res["success"]:
        lines.append("✅ Тесты успешно запущены")
    else:
        lines.append(f"❌ Ошибка: {exec_res['error'][:200]}...")

    print("\n".join(lines))

if __name__ == "__main__":
    main()