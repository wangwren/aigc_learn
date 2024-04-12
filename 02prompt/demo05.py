"""
demo05 - 直接使用Open AI 处理

多轮对话就是把之前的消息也都放在prompt中，费钱！

我们发给大模型的 prompt，不会改变大模型的权重，但会影响大模型的输出。所以，我们可以把之前的消息也都放在 prompt 中，这样大模型就知道之前的对话内容，可以更好地回答问题。

Author: weiren
Date: 2024/4/12
"""

import json
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())


# 一个辅助函数，只为演示方便。不重要
def print_json(data):
    """
    打印参数。如果参数是有结构的（如字典或列表），则以格式化的 JSON 形式打印；
    否则，直接打印该值。
    """
    if hasattr(data, 'model_dump_json'):
        data = json.loads(data.model_dump_json())

    if (isinstance(data, (list, dict))):
        print(json.dumps(
            data,
            indent=4,
            ensure_ascii=False
        ))
    else:
        print(data)


client = OpenAI()

# 定义消息历史。先加入 system 消息，里面放入对话内容以外的 prompt
messages = [
    {
        "role": "system",
        "content": """
            你是一个手机流量套餐的客服代表，你叫小瓜。可以帮助用户选择最合适的流量套餐产品。可以选择的套餐包括：
            经济套餐，月费50元，10G流量；
            畅游套餐，月费180元，100G流量；
            无限套餐，月费300元，1000G流量；
            校园套餐，月费150元，200G流量，仅限在校生。
            """
    }
]


def get_completion(prompt, model="gpt-3.5-turbo"):

    # 把用户输入加入消息历史
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
    )
    msg = response.choices[0].message.content

    # 把模型生成的回复加入消息历史。很重要，否则下次调用模型时，模型不知道上下文
    messages.append({"role": "assistant", "content": msg})
    return msg


if __name__ == "__main__":
    get_completion("流量最大的套餐是什么？")
    get_completion("多少钱？")
    get_completion("给我办一个")
    print_json(messages)
