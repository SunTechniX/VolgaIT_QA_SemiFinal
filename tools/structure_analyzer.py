from pathlib import Path

def build_file_tree(root: Path):
    def _walk(p):
        tree = {}
        for item in sorted(p.iterdir()):
            if item.name.startswith(".") and item.name not in [".gitignore"]:
                continue
            if item.is_dir():
                subtree = _walk(item)
                if subtree:
                    tree[item.name] = subtree
            else:
                tree[item.name] = None
        return tree

    py_files_content = {}
    for py in root.rglob("*.py"):
        try:
            py_files_content[str(py)] = py.read_text(encoding="utf-8", errors="ignore")
        except:
            pass

    return {
        "tree": _walk(root),
        "py_files_content": py_files_content,
        "dirs": [str(d.relative_to(root)) for d in root.rglob("*") if d.is_dir()],
        "files": [str(f.relative_to(root)) for f in root.rglob("*") if f.is_file()]
    }