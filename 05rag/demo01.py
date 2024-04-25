"""
demo01 - rag

使用elastic search和openai的API，实现一个简单的问答机器人。
就是检索出来关键词将关键词输入到prompt中，让openai根据已知的prompt和用户的提问来回答问题
主要还是靠prompt的构建，这里的prompt是一个模板，里面包含了已知信息和用户的提问

Author: weiren
Date: 2024/4/25
"""
import time

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer

from elasticsearch7 import Elasticsearch, helpers
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import re

import warnings
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

from utils.chinese_utils import to_keywords as to_keywords_chinese

warnings.simplefilter("ignore")  # 屏蔽 ES 的一些Warnings

# nltk.download('punkt')  # 英文切词、词根、切句等方法
# nltk.download('stopwords')  # 英文停用词库


def extract_text_from_pdf(filename, page_numbers=None, min_line_length=1):
    """从 PDF 文件中（按指定页码）提取文字"""
    paragraphs = []
    buffer = ''
    full_text = ''
    # 提取全部文本
    for i, page_layout in enumerate(extract_pages(filename)):
        # 如果指定了页码范围，跳过范围外的页
        if page_numbers is not None and i not in page_numbers:
            continue
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                full_text += element.get_text() + '\n'
    # 按空行分隔，将文本重新组织成段落
    lines = full_text.split('\n')
    for text in lines:
        if len(text) >= min_line_length:
            buffer += (' ' + text) if not text.endswith('-') else text.strip('-')
        elif buffer:
            paragraphs.append(buffer)
            buffer = ''
    if buffer:
        paragraphs.append(buffer)
    return paragraphs


paragraphs = extract_text_from_pdf("/Users/weiren/Downloads/需求背景.pdf",
                                   min_line_length=10)
# for para in paragraphs:
#     print(para + "\n")


def to_keywords(input_string):
    """（英文）文本只保留关键字"""
    # 使用正则表达式替换所有非字母数字的字符为空格
    no_symbols = re.sub(r'[^a-zA-Z0-9\s]', ' ', input_string)
    word_tokens = word_tokenize(no_symbols)
    # 加载停用词表
    stop_words = set(stopwords.words('english'))
    ps = PorterStemmer()
    # 去停用词，取词根
    filtered_sentence = [ps.stem(w)
                         for w in word_tokens if not w.lower() in stop_words]
    return ' '.join(filtered_sentence)


def search(query_string, top_n=3):
    # ES 的查询语言
    search_query = {
        "match": {
            "keywords": to_keywords_chinese(query_string)
        }
    }
    res = es.search(index=index_name, query=search_query, size=top_n)
    return [hit["_source"]["text"] for hit in res["hits"]["hits"]]


def get_completion(prompt, model="gpt-3.5-turbo-1106"):
    """封装 openai 接口"""
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,  # 模型输出的随机性，0 表示随机性最小
    )
    return response.choices[0].message.content


def build_prompt(prompt_template, **kwargs):
    """将 Prompt 模板赋值"""
    inputs = {}
    for k, v in kwargs.items():
        if isinstance(v, list) and all(isinstance(elem, str) for elem in v):
            val = '\n\n'.join(v)
        else:
            val = v
        inputs[k] = val
    return prompt_template.format(**inputs)


# 1. 创建Elasticsearch连接
es = Elasticsearch(
    hosts=['http://127.0.0.1:9200'],  # 服务地址与端口
)

# 2. 定义索引名称
index_name = "teacher_demo_index_tmp_wwr"

# 3. 如果索引已存在，删除它（仅供演示，实际应用时不需要这步）
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)

# 4. 创建索引
es.indices.create(index=index_name)

# 5. 灌库指令
actions = [
    {
        "_index": index_name,
        "_source": {
            "keywords": to_keywords_chinese(para),
            "text": para
        }
    }
    for para in paragraphs
]

# 6. 文本灌库
helpers.bulk(es, actions)

# 程序执行太快，还没灌库完成就往下执行了，在这停会
time.sleep(10)

# print("*" * 20)
# results = search("进件接口地址?", 2)
# for r in results:
#     print(r + "\n")

_ = load_dotenv(find_dotenv())  # 读取本地 .env 文件，里面定义了 OPENAI_API_KEY
client = OpenAI()


prompt_template = """
你是一个问答机器人。
你的任务是根据下述给定的已知信息回答用户问题。

已知信息:
{context}

用户问：
{query}

如果已知信息不包含用户问题的答案，或者已知信息不足以回答用户的问题，请直接回复"我无法回答您的问题"。
请不要输出已知信息中不包含的信息或答案。
请用中文回答用户问题。
"""

# user_query = "易借是否参与贷中打标"
user_query = "准入条件是什么"

# 1. 检索
search_results = search(user_query, 2)

# 2. 构建 Prompt
prompt = build_prompt(prompt_template, context=search_results, query=user_query)
#print("===Prompt===")
#print(prompt)

# 3. 调用 LLM
response = get_completion(prompt)

#print("===回复===")
print(response)
