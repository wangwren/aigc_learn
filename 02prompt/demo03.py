"""
demo03 - 基于前两个demo，把输出格式定义的精细
以下代码示例输出结果
{
    "name": null,
    "data": {
        "operator": ">=",
        "value": 100
    }
}

至于为什么这样做，输出json格式，对于结果可以更好的处理，比如将结果接入别的程序代码中
这只是演示，后续的demo中我们可以直接给gpt说

Author: weiren
Date: 2024/4/12
"""
# 导入依赖库
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

# 加载 .env 文件中定义的环境变量
_ = load_dotenv(find_dotenv())

# 初始化 OpenAI 客户端
client = OpenAI()  # 默认使用环境变量中的 OPENAI_API_KEY 和 OPENAI_BASE_URL


# 基于 prompt 生成文本
# 默认使用 gpt-3.5-turbo 模型
def get_completion(prompt, response_format="text", model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]  # 将 prompt 作为用户输入
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,  # 模型输出的随机性，0 表示随机性最小
        # 返回消息的格式，text 或 json_object
        response_format={"type": response_format},
    )
    return response.choices[0].message.content  # 返回模型生成的文本


if __name__ == "__main__":
    # 任务描述增加了字段的英文标识符
    instruction = """
        你的任务是识别用户对手机流量套餐产品的选择条件。
        每种流量套餐产品包含三个属性：名称(name)，月费价格(price)，月流量(data)。
        根据用户输入，识别用户在上述三种属性上的需求是什么。
        """

    # 输出格式增加了各种定义、约束
    output_format = """
        以JSON格式输出。
        1. name字段的取值为string类型，取值必须为以下之一：经济套餐、畅游套餐、无限套餐、校园套餐 或 null；
    
        2. price字段的取值为一个结构体 或 null，包含两个字段：
        (1) operator, string类型，取值范围：'<='（小于等于）, '>=' (大于等于), '=='（等于）
        (2) value, int类型
    
        3. data字段的取值为取值为一个结构体 或 null，包含两个字段：
        (1) operator, string类型，取值范围：'<='（小于等于）, '>=' (大于等于), '=='（等于）
        (2) value, int类型或string类型，string类型只能是'无上限'
    
        4. 用户的意图可以包含按price或data排序，以sort字段标识，取值为一个结构体：
        (1) 结构体中以"ordering"="descend"表示按降序排序，以"value"字段存储待排序的字段
        (2) 结构体中以"ordering"="ascend"表示按升序排序，以"value"字段存储待排序的字段
    
        只输出中只包含用户提及的字段，不要猜测任何用户未直接提及的字段，不输出值为null的字段。
        """

    input_text = "办个100G以上的套餐"
    #input_text = "有没有便宜的套餐"

    # 这条不尽如人意，因为我们没有说什么是土豪
    # input_text = "有没有土豪套餐"

    prompt = f"""
    {instruction}

    {output_format}

    用户输入：
    {input_text}
    """

    response = get_completion(prompt, response_format="json_object")
    print(response)
