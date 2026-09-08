"""文本切分"""

def split_text(text, size=200, overlap=50):
    """按长度切分，尽量在句号处断，段之间留一点重叠"""
    chunks = []
    start = 0
    n = len(text)
    while start < n:
        end = start + size
        if end >= n:
            chunks.append(text[start:n])
            break
        # 在end前面找句号，不然句子经常被切成两半
        pos = text.rfind('。', start, end)
        if pos > start + size // 2:
            end = pos + 1
        chunks.append(text[start:end])
        # 下一段往前退overlap
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
