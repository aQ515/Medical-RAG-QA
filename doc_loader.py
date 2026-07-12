"""文档加载"""

import os


def load_file(path):
    """读单个txt"""
    with open(path, 'r', encoding='utf-8') as f:
        txt = f.read()
    return txt


def load_dir(dirpath):
    """读目录里的所有txt"""
    docs = []
    for name in os.listdir(dirpath):
        if not name.endswith('.txt'):
            continue
        p = os.path.join(dirpath, name)
        docs.append({'content': load_file(p), 'source': name})
    return docs


def load(path):
    """传文件或者目录都行"""
    if os.path.isdir(path):
        return load_dir(path)
    docs = [{'content': load_file(path), 'source': os.path.basename(path)}]
    return docs
