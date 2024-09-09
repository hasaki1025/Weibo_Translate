from tqdm import tqdm
import APITranslate
import LLMTranslate


def read_data(file_path):
    with open(file_path, 'r') as f:
        return f.readlines()


def llm_translate(raw_file, model_name, save_file):
    data = read_data(raw_file)
    llm_translate_file = open(save_file, 'w', encoding='utf8')
    for i in tqdm(range(len(data))):
        text = data[i]
        translated_text = LLMTranslate.translate(model_name, text)
        llm_translate_file.write(post_process(translated_text))


def api_translate(raw_file, llm_translate_file, save_file):
    with open(llm_translate_file, 'r', encoding='utf-8') as llm_f:
        llm_data = llm_f.readlines()
        mask = APITranslate.filter_data(llm_data)
        with open(save_file, 'w', encoding='utf-8') as save_file, open(raw_file, 'r', encoding='utf-8') as raw_f:
            raw_data = raw_f.readlines()
            for i in tqdm(range(len(data))):
                try:
                    result_text = APITranslate.translate(raw_data[i]) if mask[i] else llm_data[i]
                except Exception as e:
                    print(f"Error translate in line {i}, error Message:{e}")
                    result_text = data[i]
                save_file.write(post_process(result_text))


def main():
    raw_file = 'weibo_lines.txt'
    llm_translate_file = 'weibo_llm_translated.txt'
    model_name = 'qwen2:7b'
    save_file = 'weibo_last.txt'
    llm_translate(raw_file, model_name, save_file)
    api_translate(raw_file, llm_translate_file, save_file)


if __name__ == '__main__':
    main()
