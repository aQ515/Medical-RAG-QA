"""评估检索效果，对比tfidf和embedding"""

import doc_loader
import chunk
import embedding
import vector_store
import retriever


def load_cases(path='test_questions.txt'):
    """读测试问题，一行是 问题 + 答案应该在哪个文件里"""
    cases = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            cases.append({'q': parts[0], 'src': parts[1]})
    return cases


def run(cases, chunks, mode):
    """算top3里有没有命中正确的文档"""
    if mode == 'tfidf':
        index = retriever.build_index(chunks)
    else:
        vecs = embedding.encode([c['text'] for c in chunks])
        store = vector_store.build_store(chunks, vecs)
    right = 0
    for c in cases:
        if mode == 'tfidf':
            hits = retriever.search(index, c['q'], 3)
        else:
            hits = vector_store.search(store, embedding.encode_one(c['q']), 3)
        srcs = [h['source'] for h in hits]
        if c['src'] in srcs:
            right += 1
        else:
            print('没命中：' + c['q'] + ' -> ' + str(srcs))
    return right, len(cases)


if __name__ == '__main__':
    cases = load_cases()
    docs = doc_loader.load('data')
    chunks = chunk.build_chunks(docs)
    print('一共' + str(len(chunks)) + '个片段')
    a, total = run(cases, chunks, 'tfidf')
    print('tfidf命中：' + str(a) + '/' + str(total))
    b, total = run(cases, chunks, 'embedding')
    print('embedding命中：' + str(b) + '/' + str(total))
