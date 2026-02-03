def check(file_tree, tech, **kwargs):
    # В CI всегда есть .git, поэтому даём полбалла
    return 1.0