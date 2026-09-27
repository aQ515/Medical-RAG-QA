"""问答主流程，把加载切分检索生成串起来"""

import doc_loader
import chunk
import embedding
import vector_store
import generator


def build_pipeline(datapath='data'):
    """加载文档、切分、算向量"""
    docs = doc_loader.load(datapath)
    chunks = chunk.build_chunks(docs)
    vecs = embedding.encode([c['text'] for c in chunks])
    store = vector_store.build_store(chunks, vecs)
    return store


def search_only(store, query, topk=3):
    """只做检索，不调大模型"""
    qvec = embedding.encode_one(query)
    return vector_store.search(store, qvec, topk)


def ask(store, query, topk=3):
    """问一句，返回答案和用到的片段"""
    hits = search_only(store, query, topk)
    ans = generator.answer(query, hits)
    return ans, hits
