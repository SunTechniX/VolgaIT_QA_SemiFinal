#!/usr/bin/env python3
import os
import json
import sys
from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec

def load_checker(checker_name):
    checker_path = Path("tools/checkers") / f"{checker_name}.py"
    if not checker_path.exists():
        raise FileNotFoundError(f"Checker {checker_name} not found")
    spec = spec_from_file_location(checker_name, checker_path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def load_criteria():
    with open(".github/criteria.json") as f:
        return json.load(f)["criteria"]

def evaluate_criteria(criteria, file_tree, tech):
    results = {}
    for crit in criteria:
        checker_name = crit["checker"]
        try:
            module = load_checker(checker_name)
            ratio = module.check(file_tree=file_tree, tech=tech)
            score = round(ratio * crit["weight"], 2)
        except Exception as e:
            print(f"⚠️ Checker {checker_name} failed: {e}", file=sys.stderr)
            score = 0.0
        results[crit["id"]] = {
            "name": crit["name"],
            "weight": crit["weight"],
            "score": score
        }
    return results

def main():
    root = Path(".")
    sys.path.insert(0, str(root))  # на всякий случай

    from tools.structure_analyzer import build_file_tree
    from tools.tech_detector import detect_tech_stack
    from tools.linter_runner import run_linters
    from tools.exec_tester import try_run_tests

    file_tree = build_file_tree(root)
    tech = detect_tech_stack(root)
    linter_results = run_linters(root)
    exec_result = try_run_tests(root, tech)
    criteria = load_criteria()
    crit_results = evaluate_criteria(criteria, file_tree, tech)

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

if __name__ == "__main__":
    main()