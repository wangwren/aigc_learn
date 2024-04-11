"""
没有配置 .env 文件的情况下，可以直接在代码中配置

"""
from openai import OpenAI

if __name__ == "__main__":
    client = OpenAI(
        api_key = "your-api-key",
        base_url = "base url"
    )

    chat_completion = client.chat.completions.create(
        # 互动式对话、持续的会话、需要考虑上下文连续性的应用
        messages=[
            {
                "role": "user",
                "content": "讲个笑话",
            }
        ],
        model="gpt-3.5-turbo",  # 此处更换其它模型,请参考模型列表 eg: google/gemma-7b-it
    )
    print(chat_completion.choices[0].message.content)
