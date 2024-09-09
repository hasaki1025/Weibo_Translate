import json
import os.path
import re

from pip._vendor import requests

from TranslateDemo.apidemo.utils.AuthV3Util import addAuthParams


# 您的应用ID
# https://ai.youdao.com/?keyfrom=fanyi-new-nav#/
APP_KEY = ''
# 您的应用密钥
APP_SECRET = ''


def need_translate(text):
    ch_pattern = re.compile(r'[\u4e00-\u9fff]+')
    return ch_pattern.search(text) is not None or text == 'None\n'


def filter_data(data):
    return [need_translate(sent) for sent in data]


def doCall(url, header, params, method):
    if 'get' == method:
        return requests.get(url, params)
    elif 'post' == method:
        return requests.post(url, params, header)


def translate(texts):
    '''
        note: 将下列变量替换为需要请求的参数
        '''
    q = texts
    lang_from = 'Chinese'
    lang_to = 'English'

    data = {'q': q, 'from': lang_from, 'to': lang_to}

    addAuthParams(APP_KEY, APP_SECRET, data)

    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = doCall('https://openapi.youdao.com/api', header, data, 'post')
    response = json.loads(str(res.content, 'utf-8'))
    if int(response['errorCode']) != 0:
        raise Exception(f"Translation failed,errorCode:{response['errorCode']}")

    result = response['translation'][0]
    print(result)
    return result


#def get_error_index():
#    ef = 'error.json'
#    if os.path.exists(ef):
#        with open(ef, 'r') as f:
#            return set(json.load(f))
#    return set()


# def main():
#     with open('weibo3.txt', 'r', encoding='utf-8') as f:
#         data = f.readlines()
#         mask = filter_data(data)
#         with open('weibo_last.txt', 'w', encoding='utf-8') as f2, open('weibo_lines.txt', 'r', encoding='utf-8') as raw_f:
#             raw_data = raw_f.readlines()
#             error_index = set()
#             success_index = set()
#             for i in tqdm(range(len(data))):
#                 try:
#                     result_text = translate(raw_data[i]) if mask[i] else data[i]
#                     success_index.add(i)
#                 except Exception as e:
#                     print(f"Error translate in line {i}, error Message:{e}")
#                     error_index.add(i)
#                     result_text = data[i]
#                 f2.write(post_process(result_text))
#
#             with open('error.json', 'w', encoding='utf-8') as error_file:
#                 json.dump(error_index, error_file, indent=4)
#             with open('success.json', 'w', encoding='utf-8') as success_file:
#                 json.dump(success_index, success_file, indent=4)



