"""
demo02 - 

Author: weiren
Date: 2024/4/11
"""

from openai import OpenAI

# 加载 .env 文件到环境变量
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

if __name__ == "__main__":
    # 初始化 OpenAI 服务。会自动从环境变量加载 OPENAI_API_KEY 和 OPENAI_BASE_URL
    client = OpenAI()

    # 消息
    messages = [
        {
            "role": "system",
            "content": "你是一个Java领域的专家"  # 注入新知识
        },
        {
            "role": "user",
            "content": "Java代码中，我有一个passList集合，这里面对象中有一个字段叫做expireTime额度有效期，是一个Integer类型的时间戳，我想获取这个集合中额度有效期最大的那个值，如果获取到最大的值为空或者为0，取当前日期30天的时间，如何计算 用中文"  # 问问题。可以改改试试
        },

    ]

    print(type(messages))
    print(type(messages[0]))

    # 调用 GPT-3.5
    chat_completion = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=messages
    )

    # 输出回复
    print(chat_completion.choices[0].message.content)
