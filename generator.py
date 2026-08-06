"""拼prompt和调大模型"""

import os
from openai import OpenAI


def build_prompt(query, hits):
    """把检索到的片段拼进prompt里"""
    ctx = ''
    for i, h in enumerate(hits):
        ctx += str(i + 1) + '. ' + h['text'] + '\n'
    prompt = '下面是一些参考资料：\n' + ctx
    prompt += '\n请只根据上面的资料回答下面的问题，资料里没有提到的就说不知道，不要自己编。\n'
    prompt += '问题：' + query
    return prompt


def call_llm(prompt):
    """调一次大模型"""
    client = OpenAI(
        api_key=os.environ.get('OPENAI_API_KEY'),
        base_url=os.environ.get('OPENAI_BASE_URL'),
    )
    model = os.environ.get('LLM_MODEL', 'deepseek-chat')
    resp = client.chat.completions.create(
        model=model,
        messages=[{'role': 'user', 'content': prompt}],
    )
    return resp.choices[0].message.content


def answer(query, hits):
    """检索完了生成答案"""
    prompt = build_prompt(query, hits)
    return call_llm(prompt)
