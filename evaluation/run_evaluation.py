import json
import duckdb
from pathlib import Path

from src.text2sql import generate_sql
from src.sql_validator import validate_sql


TEST_FILE = Path("evaluation/test_questions.json")
RESULT_FILE = Path("evaluation/evaluation_results.json")
DB_PATH = "database.duckdb"
GOLD_FILE = Path("evaluation/gold_queries.json")

# 读取测试题
with open(TEST_FILE, "r", encoding="utf-8") as f:
    questions = json.load(f)
with open(GOLD_FILE, "r", encoding="utf-8") as f:
    gold_queries = json.load(f)

gold_sql_map = {
    item["id"]: item["gold_sql"]
    for item in gold_queries
}

results = []

def compare_results(agent_df, gold_df):
    """
    比较 Agent SQL 和 Gold SQL 的查询结果。
    忽略列名、行顺序和轻微浮点误差。
    """

    # 行列数量不同，直接判错
    if agent_df.shape != gold_df.shape:
        return False

    # 忽略列名，只比较值
    agent = agent_df.copy()
    gold = gold_df.copy()

    agent.columns = range(agent.shape[1])
    gold.columns = range(gold.shape[1])

    # 排序，避免 ORDER BY 写法不同导致误判
    try:
        agent = agent.sort_values(
            by=list(agent.columns)
        ).reset_index(drop=True)

        gold = gold.sort_values(
            by=list(gold.columns)
        ).reset_index(drop=True)
    except Exception:
        agent = agent.reset_index(drop=True)
        gold = gold.reset_index(drop=True)

    # 比较结果，允许轻微浮点误差
    try:
        import pandas as pd

        pd.testing.assert_frame_equal(
            agent,
            gold,
            check_dtype=False,
            check_exact=False,
            rtol=1e-5,
            atol=1e-8
        )

        return True

    except AssertionError:
        return False

for item in questions:

    question = item["question"]

    print("\n" + "=" * 70)
    print(f"测试 {item['id']}: {question}")

    try:
        # 1. Text2SQL
        sql = generate_sql(question)

        print("\n生成 SQL：")
        print(sql)

        # 2. 安全 + 语义校验
        is_valid, validation_message = validate_sql(sql)

        executable = False
        error = None

        # 3. 实际执行
        result_correct = None

        if is_valid:
            try:
                conn = duckdb.connect(DB_PATH, read_only=True)

                # 执行 Agent SQL
                agent_df = conn.execute(sql).df()
                executable = True

                # 如果这道题有 Gold SQL，则比较查询结果
                if item["id"] in gold_sql_map:
                    gold_sql = gold_sql_map[item["id"]]
                    gold_df = conn.execute(gold_sql).df()

                    result_correct = compare_results(
                        agent_df,
                        gold_df
                    )

                conn.close()

            except Exception as e:
                error = str(e)

        else:
            error = validation_message

        print(f"\n是否可执行：{executable}")

        results.append({
            "id": item["id"],
            "question": question,
            "type": item["type"],
            "sql": sql,
            "executable": executable,
            "result_correct":result_correct,
            "error": error
        })

    except Exception as e:

        print(f"\n运行失败：{e}")

        results.append({
            "id": item["id"],
            "question": question,
            "type": item["type"],
            "sql": None,
            "executable": False,
            "error": str(e)
        })

with open(GOLD_FILE, "r", encoding="utf-8") as f:
    gold_queries = json.load(f)

gold_sql_map = {
    item["id"]: item["gold_sql"]
    for item in gold_queries
}

# 计算 SQL 可执行率
success_count = sum(
    1 for result in results
    if result["executable"]
)

total_count = len(results)

execution_rate = success_count / total_count
# 计算 Execution Accuracy
gold_results = [
    result for result in results
    if result["id"] in gold_sql_map
]

correct_count = sum(
    1 for result in gold_results
    if result.get("result_correct") is True
)

accuracy = correct_count / len(gold_results)

print("\n" + "=" * 70)
print("评测完成")
print(f"测试题数量：{total_count}")
print(f"可执行 SQL：{success_count}")
print(f"SQL 可执行率：{execution_rate:.2%}")
print(f"结果正确 SQL：{correct_count}/{len(gold_results)}")
print(f"Execution Accuracy：{accuracy:.2%}")

# 保存详细结果
with open(RESULT_FILE, "w", encoding="utf-8") as f:
    json.dump(
        results,
        f,
        ensure_ascii=False,
        indent=2
    )

print(f"\n详细结果已保存到：{RESULT_FILE}")
