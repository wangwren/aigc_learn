"""
demo01 - 

Author: weiren
Date: 2024/5/11
"""

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

llm = ChatOpenAI(model="gpt-3.5-turbo")  # 默认是gpt-3.5-turbo
response = llm.invoke("你是谁")
print(response.content)
