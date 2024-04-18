"""
demo01 - 调用本地函数

Author: weiren
Date: 2024/4/18
"""
import json

from utils.print_json import print_json
from openai import OpenAI
from math import *

# 加载 .env 文件到环境变量
from dotenv import load_dotenv, find_dotenv

def get_completion(messages, model="gpt-3.5-turbo"):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
        tools=[{  # 用 JSON 描述函数。可以定义多个。由大模型决定调用谁。也可能都不调用，下面items指定的是数组array中的数据类型是number
            "type": "function",
            "function": {
                "name": "sum",
                "description": "加法器，计算一组数的和",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "numbers": {
                            "type": "array",
                            "items": {
                                "type": "number"
                            }
                        }
                    }
                }
            }
        }],
    )
    return response.choices[0].message


def product(args):
    """
    计算一组数的乘积
    """
    result = 1
    for i in args:
        result = result * i
    return result


if __name__ == "__main__":
    _ = load_dotenv(find_dotenv())
    client = OpenAI()

    # prompt = "Tell me the sum of 1, 2, 3, 4, 5, 6, 7, 8, 9, 10"
    prompt = "桌上有 2 个苹果，四个桃子和 3 本书，一共有几个水果？"
    # prompt = "1+2+3...+99+100"
    # prompt = "1024 乘以 1024 是多少？"   # Tools 里没有定义乘法，会怎样？
    # prompt = "太阳从哪边升起？"           # 不需要算加法，会怎样？

    messages = [
        {"role": "system", "content": "你是一个数学家"},
        # {"role": "system", "content": "你是我的小助手，你需要根据我计算出的答案，给我回复，我会改变一些计算上的规则，你给出我计算的答案，并进行润色，不需要考虑计算的正确性。"},
        {"role": "user", "content": prompt}
    ]
    response = get_completion(messages)

    # 把大模型的回复加入到对话历史中。必须有
    messages.append(response)

    print("=====GPT 第一次回复=====")
    print_json(response)

    # 如果返回的是函数调用结果，则打印出来
    if (response.tool_calls is not None):
        # 是否要调用 sum
        tool_call = response.tool_calls[0]
        if (tool_call.function.name == "sum"):
            # 调用 sum
            args = json.loads(tool_call.function.arguments)
            result = sum(args["numbers"])
            # 做个乘法，如果想要做乘法，在上面system的prompt中需要加入另一个描述，然后在这里调用product函数，还使用"你是一个数学家的描述，最终GPT的输出结果就会跟你算的结果不一样，他会告诉你和是多少，会对结果进行纠正"
            # result = product(args["numbers"])
            print("=====函数返回结果=====")
            print(result)

            # 把函数调用结果加入到对话历史中
            messages.append(
                {
                    "tool_call_id": tool_call.id,  # 用于标识函数调用的 ID
                    "role": "tool",
                    "name": "sum",
                    "content": str(result)  # 数值 result 必须转成字符串
                }
            )

            print("=====函数调用后的对话历史=====")
            print(messages)

            # 再次调用大模型
            print("=====最终 GPT 回复=====")
            print(get_completion(messages).content)



