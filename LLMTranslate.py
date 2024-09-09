import re

import ollama
from tqdm import tqdm


def read_data(file):
    with open(file, 'r', encoding='utf8') as f:
        return f.readlines()


def tex_process(text):
    p1 = re.compile(r'[\u4e00-\u9fff][a-zA-Z]')  # [a-zA-Z][\u4e00-\u9fff]
    p2 = re.compile(r'[a-zA-Z][\u4e00-\u9fff]')
    p3 = re.compile(r'&[a-zA-Z0-9#]+;')
    p4 = re.compile(r'\s+')

    text = p1.sub(lambda x: x.group()[0] + ' ' + x.group()[1], text)
    text = p2.sub(lambda x: x.group()[0] + ' ' + x.group()[1], text)
    text = p3.sub(' ', text)
    return p4.sub(' ', text)


def post_process(text):
    return text.replace('\n', '') + '\n'


def translate(model, text):
    # prefix = "你是一个网络新闻标题翻译助手，翻译过程中保留非中文字符，对于无法翻译的语句请使用None回答，请将以下中文新闻标题翻译成英文："
    prefix2 = ('You are an expert news headline translation assistant. Please translate the following Chinese news '
               'headlines into English while preserving any non-Chinese characters. If you are unable to translate a '
               'sentence, please respond with "None". Here is the headline to translate:')
    sent = tex_process(text.strip())  # 去掉多余空格
    prompt = prefix2 + sent
    response = ollama.generate(model=model, prompt=prompt)
    translated_text = response['response']
    print(translated_text)
    return translated_text


def replace(text):
    return text.replace('\n', ' ') + '\n'




#def main():
#    data = read_data('weibo_lines.txt')
#    model_name = 'qwen2:7b'
#    f = open('weibo.txt', 'w', encoding='utf8')
#    for i in tqdm(range(len(data))):
#        text = data[i]
#        translated_text = translate(model_name, text)
#        f.write(post_process(translated_text))
