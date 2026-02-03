#!/usr/bin/env python3
import os
import json
import sys
import subprocess
from pathlib import Path
from importlib import import_module

# Добавляем текущую директорию в путь
sys.path.append(str(Path(__file__).parent))

from structure_analyzer import build_file_tree
from tech_detector import detect_tech_stack
from linter_runner import run_linters
from exec_tester import try_run_tests

def load_criteria():
    with open(".github/criteria.json") as f:
        return json.load(f)["criteria"]

def evaluate_criteria(criteria, file_tree, tech):
    results = {}
    checkers_dir = Path("tools/checkers")
    
    for crit in criteria:
        checker_name = crit["checker"]
        try:
            module = import_module(f"tools.checkers.{checker_name}")
            score_ratio = module.check(file_tree=file_tree, tech=tech)
            score = round(score_ratio * crit["weight"], 2)
        except Exception as e:
            print(f"⚠️ Checker {checker_name} failed: {e}", file=sys.stderr)
            score = 0.0
        
        results[crit["id"]] = {
            "name": crit["name"],
            "weight": crit["weight"],
            "score": score,
            "description": crit.get("description", "")
        }
    return results

def main():
    root = Path(".")
    file_tree = build_file_tree(root)
    tech = detect_tech_stack(root)
    
    # Запуск линтеров
    linter_results = run_linters(root)
    
    # Попытка запуска тестов
    exec_result = try_run_tests(root, tech)
    
    # Оценка по критериям
    criteria = load_criteria()
    crit_results = evaluate_criteria(criteria, file_tree, tech)
    
    # Итог
    total = sum(v["score"] for v in crit_results.values())
    max_score = sum(v["weight"] for v in crit_results.values())
    
    output = {
        "file_tree": file_tree,
        "tech_stack": tech,
        "linters": linter_results,
        "execution": exec_result,
        "criteria": crit_results,
        "summary": {
            "total": round(total, 2),
            "max": round(max_score, 2),
            "percent": round(100 * total / max_score, 1) if max_score else 0
        }
    }
    
    with open("result.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print("::set-output name=result::done")
    print("✅ Анализ завершён. Результат в result.json")

if __name__ == "__main__":
    main()