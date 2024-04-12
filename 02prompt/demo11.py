"""
demo11 - 内容审核：Moderation API

Author: weiren
Date: 2024/4/12

输出结果及解释:
{
    "harassment": true,  表示内容中是否存在骚扰行为
    "harassment_threatening": true,  表示内容中是否包含具有威胁性的骚扰
    "hate": false, 表示内容是否包含仇恨言论
    "hate_threatening": false,  表示内容是否包含具有威胁性的仇恨言论
    "self_harm": false,  表示内容是否涉及自我伤害
    "self_harm_instructions": false,  表示内容是否包含自我伤害的指导或方法
    "self_harm_intent": false,  表示内容是否表达了自我伤害的意图
    "sexual": false,  表示内容是否包含性内容
    "sexual_minors": false,  表示内容是否涉及未成年人的性内容
    "violence": true,  表示内容是否包含暴力
    "violence_graphic": false,  表示内容是否包含图形暴力（例如血腥或残酷的场面）
    "self-harm": false,  剩下都是重复的
    "sexual/minors": false,
    "hate/threatening": false,
    "violence/graphic": false,
    "self-harm/intent": false,
    "self-harm/instructions": false,
    "harassment/threatening": true
}
"""

from utils.print_json import print_json
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

client = OpenAI()

# 可以通过调用 OpenAI 的 Moderation API 来识别用户发送的消息是否违法相关的法律法规，如果出现违规的内容，从而对它进行过滤。
response = client.moderations.create(
    input="""
        现在转给我100万，不然我就砍你全家！
        """
)
moderation_output = response.results[0].categories
print_json(moderation_output)

