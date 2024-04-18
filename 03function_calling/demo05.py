"""
demo05 - 写一个查询花鸭数据库的demo，数据库先用内存实现

Author: weiren
Date: 2024/4/18
"""

import json

from utils.print_json import print_json
from openai import OpenAI

# 加载 .env 文件到环境变量
from dotenv import load_dotenv, find_dotenv

import sqlite3

#  描述数据库表结构
database_schema_string = """
create table config_partner
(
    id           int auto_increment comment '主键id'
        primary key,
    api_channel  int           not null, -- 'api渠道'
    channel_code int default 0 not null, -- '标渠对应渠道号'
    channel_name varchar(64)   not null, -- '渠道名称'
    create_time  int           not null, -- '创建时间'
    update_time  int           not null -- '更新时间'
);
"""

def ask_database(query):
    cursor.execute(query)
    records = cursor.fetchall()
    return records

def get_sql_completion(messages, model="gpt-3.5-turbo"):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
        tools=[{
            "type": "function",
            "function": {
                "name": "ask_database",
                "description": "Use this function to answer user questions about business. \
                            Output should be a fully formed SQL query.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": f"""
                            SQL query extracting info to answer the user's question.
                            SQL should be written using this database schema:
                            {database_schema_string}
                            The query should be returned in plain text, not in JSON.
                            The query should only contain grammars supported by SQLite.
                            """,
                        }
                    },
                    "required": ["query"],
                }
            }
        }],
    )
    return response.choices[0].message

if __name__ == "__main__":
    _ = load_dotenv(find_dotenv())
    client = OpenAI()

    # 创建数据库连接
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # 创建orders表
    cursor.execute(database_schema_string)

    # 插入5条明确的模拟记录
    mock_data = [
        (1, 50001, 45, '桔子分期', 1659003927, 1659003927),
        (2, 50002, 46, '小赢', 1659003927, 1659003927),
        (3, 50003, 48, '你我贷', 1659003927, 1659003927),
        (4, 50004, 49, '信用飞', 1659003927, 1659003927),
        (5, 50005, 50, '乐卡借钱', 1659003927, 1659003927)
    ]

    for record in mock_data:
        cursor.execute('''
        INSERT INTO config_partner (id, api_channel, channel_code, channel_name, create_time, update_time)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', record)

    # 提交事务
    conn.commit()

    prompt = "api渠道是50004是哪个渠道"

    messages = [
        {"role": "system", "content": "你是一个数据分析师，基于数据库的数据回答问题"},
        {"role": "user", "content": prompt}
    ]
    response = get_sql_completion(messages, model="gpt-4-turbo-preview")
    if response.content is None:
        response.content = ""
    messages.append(response)
    print("====Function Calling====")
    print_json(response)

    if response.tool_calls is not None:
        tool_call = response.tool_calls[0]
        if tool_call.function.name == "ask_database":
            arguments = tool_call.function.arguments
            args = json.loads(arguments)
            print("====SQL====")
            print(args["query"])
            result = ask_database(args["query"])
            print("====DB Records====")
            print(result)

            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": "ask_database",
                "content": str(result)
            })
            response = get_sql_completion(messages)
            print("====最终回复====")
            print(response.content)

