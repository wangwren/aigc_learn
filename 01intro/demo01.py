from openai import OpenAI

"""
加载环境变量
首先使用find_dotenv()找到.env文件的路径，然后使用load_dotenv()加载这个文件。
这个过程中，.env文件内的键值对会被设置为环境变量，可以在Python代码中通过os.environ.get('KEY')来访问。这里使用_作为变量名，表示这个操作的结果不会被后续代码使用。
"""
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

# 通过环境变量获取API_KEY和BASE_URL，如果没有指定参数，源码中会判断，默认取环境变量中的值，os.environ.get("OPENAI_API_KEY")，os.environ.get("OPENAI_BASE_URL")
client = OpenAI()

#prompt = "今天我很"  # 改我试试
prompt = "下班了，今天我很"
# prompt = "放学了，今天我很"
# prompt = "AGI 实现了，今天我很"
response = client.completions.create(
    # 非交互式任务，不需要考虑上下文连续性的单次文本生成
    model="gpt-3.5-turbo-instruct",
    prompt=prompt,
    max_tokens=512,
    stream=True  # 以流的方式返回数据，这意味着响应可能会分多个部分返回，而不是一次性返回整个响应
)

print(type(response))
for chunk in response:
    print(chunk.choices[0].text, end='')
