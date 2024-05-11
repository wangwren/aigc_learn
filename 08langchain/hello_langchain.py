"""
hello_langchain - 

Author: weiren
Date: 2024/5/11
"""

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

chat = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
response = chat([HumanMessage(content="Hello Langchain!")])
print(response)