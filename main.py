"""命令行问答"""

import os

import qa


def main():
    has_key = bool(os.environ.get('OPENAI_API_KEY'))
    if not has_key:
        print('没配OPENAI_API_KEY，只显示检索到的片段')
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
        if has_key:
            ans, hits = qa.ask(store, q)
            print(ans)
            print('参考：', [h['source'] for h in hits])
        else:
            hits = qa.search_only(store, q)
            for h in hits:
                print('[' + h['source'] + '] ' + h['text'])


if __name__ == '__main__':
    main()
