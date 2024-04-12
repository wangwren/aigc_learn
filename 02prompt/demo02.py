"""
demo02 - 针对demo01的改进，加上输出格式的限制

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
    # 任务描述
    instruction = """
        你的任务是识别用户对手机流量套餐产品的选择条件。
        每种流量套餐产品包含三个属性：名称，月费价格，月流量。
        根据用户输入，识别用户在上述三种属性上的需求是什么。
        """

    # 用户输入
    input_text = """
        办个100G的套餐。
        """

    # 输出格式
    output_format = """
        以 JSON 格式输出
        """

    # prompt 模版。instruction 和 input_text 会被替换为上面的内容
    # 稍微调整下咒语，加入输出格式
    prompt = f"""
        {instruction}
    
        {output_format}
    
        用户输入：
        {input_text}
        """

    print("打印一下prompt:", prompt)
    print("*" * 20)

    # 调用大模型
    response = get_completion(prompt, response_format="json_object")
    print(response)




