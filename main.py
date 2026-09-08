"""命令行问答"""

import os

import qa


def main():
    if not os.environ.get('OPENAI_API_KEY'):
        print('没检测到OPENAI_API_KEY，生成答案那步会报错')
    print('正在加载文档算向量，第一次会比较慢')
    store = qa.build_pipeline('data')
    print('好了，可以问了，输入q退出')
    while True:
        q = input('问：')
        q = q.strip()
        if q == 'q':
            break
        if not q:
            continue
        ans, hits = qa.ask(store, q)
        print(ans)
        print('参考：', [h['source'] for h in hits])


if __name__ == '__main__':
    main()
