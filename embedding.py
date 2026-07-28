"""文本转向量"""

from sentence_transformers import SentenceTransformer

_model = None


def get_model(name='shibing624/text2vec-base-chinese'):
    """模型比较大，加载一次就留着用"""
    global _model
    if _model is None:
        _model = SentenceTransformer(name)
    return _model


def encode(texts):
    """把一批文本变成向量"""
    m = get_model()
    return m.encode(texts, convert_to_numpy=True)


def encode_one(text):
    """单条文本"""
    return encode([text])[0]
