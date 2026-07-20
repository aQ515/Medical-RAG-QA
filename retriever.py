"""tfidf检索，最开始写的版本"""

import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def cut(text):
    """先分词，tfidf要按空格分开的词"""
    return ' '.join(jieba.cut(text))


def build_index(chunks):
    """把所有片段做成tfidf矩阵"""
    vec = TfidfVectorizer()
    texts = [cut(c['text']) for c in chunks]
    matrix = vec.fit_transform(texts)
    return {'vec': vec, 'matrix': matrix, 'chunks': chunks}


def search(index, query, topk=3):
    """找和问题最相关的几个片段"""
    q = index['vec'].transform([cut(query)])
    sims = cosine_similarity(q, index['matrix'])[0]
    order = sims.argsort()[::-1][:topk]
    out = []
    for i in order:
        c = index['chunks'][i]
        out.append({'text': c['text'], 'source': c['source'], 'score': float(sims[i])})
    return out
