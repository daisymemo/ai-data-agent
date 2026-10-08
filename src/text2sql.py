from src.sql_validator import validate_sql
import duckdb
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
from src.context_builder import get_database_schema
from src.retriever import retrieve


client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)


def generate_sql(question, retrieved_chunks=None):
    schema = get_database_schema()

    if retrieved_chunks is None:
        retrieved_chunks = retrieve(question, top_k=3)
    print("\nRAG 检索结果：")

    for i, chunk in enumerate(retrieved_chunks, start=1):
        print(
            f"Top {i} | "
            f"score={chunk['score']:.4f} | "
            f"source={chunk['source']}"
        )

        # 只打印知识块第一行，也就是标题
        print(chunk["content"].splitlines()[0])
    retrieved_context = "\n\n".join(
        chunk["content"]
        for chunk in retrieved_chunks
    )

    # 最终提供给 LLM 的上下文
    context = f"""
    # Database Schema
    {schema}

    # Retrieved Business Knowledge
    {retrieved_context}
    """

    system_prompt = f"""
你是一名专业的数据分析助手。

你的任务是根据用户的自然语言问题，生成可以在 DuckDB 中执行的 SQL。

以下是数据库相关信息：

{context}

要求：
1. 只能使用上述数据库中真实存在的表和字段。
2. 必须遵守 Metric Dictionary 中定义的业务口径。
3. SQL 方言使用 DuckDB。
4. 只生成查询语句，不允许 INSERT、UPDATE、DELETE、DROP 等操作。
5. 只返回 SQL，不要解释，不要使用 Markdown 代码块。
"""

    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return response.choices[0].message.content.strip()

def explain_result(question, result):
    result_text = result.to_string(index=False)

    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=[
            {
                "role": "system",
                "content": """
你是一名数据分析助手。

请根据用户的问题和查询结果进行简洁、准确的业务解释。

要求：
1. 只能根据查询结果回答，不要编造原因。
2. 总结最重要的数据特征。
3. 如果只能看到现象，不能判断原因，要明确说明。
4. 使用自然、简洁的中文回答。
"""
            },
            {
                "role": "user",
                "content": f"""
用户问题：
{question}

查询结果：
{result_text}
"""
            }
        ]
    )

    return response.choices[0].message.content

def ask(question):
    """
    Data Agent 主入口：
    用户问题 → RAG → Text2SQL → SQL校验 → 执行 → 结果解释
    """

    # 1. 生成 SQL
    retrieved_chunks = retrieve(question, top_k=3)
    sql = generate_sql(question, retrieved_chunks=retrieved_chunks)

    print("\n生成 SQL：")
    print(sql)

    # 2. SQL 安全校验
    is_valid, message = validate_sql(sql)

    print("\nSQL 安全校验：")
    print(message)

    if not is_valid:
        raise ValueError(f"SQL 未通过安全校验：{message}")

    # 3. 执行 SQL
    conn = duckdb.connect("database.duckdb", read_only=True)

    try:
        result = conn.execute(sql).df()
    finally:
        conn.close()

    print("\n查询结果：")
    print(result)

    # 4. AI 解释结果
    answer = explain_result(question, result)

    print("\nAI 分析：")
    print(answer)

    return {
        "question": question,
        "sql": sql,
        "result": result,
        "answer": answer,
        "validation_message": message,
        "retrieved_chunks":retrieved_chunks
    }

if __name__ == "__main__":
    ask("不同营销渠道的转化率是多少？")





