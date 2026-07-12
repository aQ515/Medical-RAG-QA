"""文本切分"""

def split_text(text, size=200, overlap=50):
    """按固定长度切分，段之间留一点重叠"""
    chunks = []
    start = 0
    n = len(text)
    while start < n:
        end = start + size
        chunks.append(text[start:end])
        # 下一段往前退overlap，避免刚好把一句话切断
        start = end - overlap
        if start <= 0:
            break
    return chunks


def build_chunks(docs, size=200, overlap=50):
    """把加载出来的文档切成一堆片段"""
    chunks = []
    for d in docs:
        pieces = split_text(d['content'], size, overlap)
        for c in pieces:
            chunks.append({'text': c, 'source': d['source']})
    return chunks
