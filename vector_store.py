"""向量存储和检索"""

import numpy as np


def build_store(chunks, vectors):
    """把片段和对应的向量放在一起"""
    return {'chunks': chunks, 'vectors': np.array(vectors)}


def cosine(a, b):
    """算两个向量的余弦相似度"""
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8))


def search(store, qvec, topk=3):
    """按向量找最像的几个片段"""
    scores = []
    for v in store['vectors']:
        scores.append(cosine(qvec, v))
    order = np.argsort(scores)[::-1][:topk]
    out = []
    for i in order:
        c = store['chunks'][i]
        out.append({'text': c['text'], 'source': c['source'], 'score': scores[i]})
    return out
