# 医药文档RAG问答

用检索增强生成做的医药文档问答。先把说明书和资料切碎存成向量，提问的时候先检索出相关片段，再让大模型只根据这些片段回答，比直接问大模型乱编的情况少很多。

## 用法

```bash
pip install -r requirements.txt

# 命令行问答
python main.py

# 跑检索效果评估
python eval.py
```

生成答案那步要配一个兼容OpenAI接口的大模型，用环境变量设置：

OPENAI_API_KEY是必填的，用国内的模型再填OPENAI_BASE_URL，LLM_MODEL不填默认deepseek-chat。

## 文件

- doc_loader.py - 加载txt文档
- chunk.py - 文本切分
- retriever.py - tfidf检索，最开始写的版本，留着做对比
- embedding.py - 文本转向量
- vector_store.py - 向量检索
- generator.py - 拼prompt和调大模型
- qa.py - 把上面几步串起来
- main.py - 命令行交互
- eval.py - 检索效果评估
- test_questions.txt - 测试问题
- data/ - 知识库，四份药品说明书和高血压用药资料

## 检索方式

eval.py 里对比了 tfidf 和 embedding 两种检索在 test_questions.txt 上的 top3 命中情况，跑一下就能看到具体数字。

tfidf 只能匹配字面，问法和资料里的写法不一致就容易漏。比如资料里写的是"头痛"，问"头疼"就检索不到布洛芬那篇，换成向量检索才能匹配上，这也是后来换成 embedding 的主要原因。

## 踩坑

- TfidfVectorizer 直接喂中文不行，它默认按空格切词，得先分词，这里用的 jieba
- jieba 切出来的单字词会被 TfidfVectorizer 默认过滤掉，太短的词匹配不到
- tfidf 只认字面，问"头疼"找不到资料里的"头痛"，后来换成 embedding 向量检索
- 切分一开始是按固定长度硬切，句子经常被切成两半，检索出来的片段读不通，改成在句号附近断开
- 切分留了重叠，top3 里经常有两段内容几乎一样，加了个按开头去重的处理
- 检索没加阈值的时候，问个完全不相干的问题也会硬塞三段进去，反而干扰大模型，加了阈值过滤
- 不配 OPENAI_API_KEY 的话大模型那步会直接报错，main.py 启动时先提示一下
