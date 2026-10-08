import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-flash",
    messages=[
        {
            "role": "system",
            "content": "你是一名数据分析助手。"
        },
        {
            "role": "user",
            "content": "帮我写一段SQL查询线下网点客户数量。"
        }
    ]
)

print(response.choices[0].message.content)