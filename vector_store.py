"""向量存储和检索"""

import numpy as np


def build_store(chunks, vectors):
    """把片段和对应的向量放在一起"""
    return {'chunks': chunks, 'vectors': np.array(vectors)}


def cosine(a, b):
    """算两个向量的余弦相似度"""
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8))


def search(store, qvec, topk=3, threshold=0.3):
    """按向量找最像的几个片段，太不像的丢掉，重复的也去掉"""
    scores = []
    for v in store['vectors']:
        scores.append(cosine(qvec, v))
    order = np.argsort(scores)[::-1]
    out = []
    seen = set()
    for i in order:
        if scores[i] < threshold:
            continue
        c = store['chunks'][i]
        # 切分有重叠，相邻两段内容差不多，按开头去重
        key = c['text'][:30]
        if key in seen:
            continue
        seen.add(key)
        out.append({'text': c['text'], 'source': c['source'], 'score': scores[i]})
        if len(out) >= topk:
            break
    return out
