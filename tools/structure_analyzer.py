# tools/structure_analyzer.py
from pathlib import Path

def safe_read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding="utf-8-sig")
        except:
            return path.read_text(encoding="latin1", errors="ignore")

def _walk(p: Path, root: Path):
    tree = {}
    for item in sorted(p.iterdir()):
        rel_path = item.relative_to(root)
        # ❌ Игнорируем служебные файлы и папки
        if (
            item.name.startswith(".") and item.name not in [".gitignore"]
            or rel_path.parts[0] == "tools"  # ← игнорируем всю папку tools/
            or item.name == "result.json"
            or item.name == "__pycache__"
        ):
            continue
        if item.is_dir():
            subtree = _walk(item, root)
            if subtree:
                tree[item.name] = subtree
        else:
            tree[item.name] = None
    return tree

def build_file_tree(root: Path):
    tree = _walk(root, root)

    py_files_content = {}
    for py in root.rglob("*.py"):
        rel = py.relative_to(root)
        if rel.parts[0] == "tools":
            continue  # ← не читаем свои файлы
        try:
            py_files_content[str(py)] = safe_read_text(py)
        except:
            pass

    dirs = []
    files = []
    for item in root.rglob("*"):
        if item.is_file() or item.is_dir():
            rel = item.relative_to(root)
            if rel.parts[0] == "tools":
                continue
            if item.is_dir():
                dirs.append(str(rel))
            else:
                files.append(str(rel))

    return {
        "tree": tree,
        "py_files_content": py_files_content,
        "dirs": dirs,
        "files": files
    }