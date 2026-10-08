import json
from pathlib import Path

from src.sql_validator import validate_sql


TEST_FILE = Path("evaluation/safety_test_cases.json")


with open(TEST_FILE, "r", encoding="utf-8") as f:
    test_cases = json.load(f)


results = []

for item in test_cases:
    sql = item["sql"]
    should_pass = item["should_pass"]

    is_valid, message = validate_sql(sql)

    # validator 的实际判断是否符合预期
    correct = is_valid == should_pass

    results.append({
        "id": item["id"],
        "sql": sql,
        "should_pass": should_pass,
        "actual_pass": is_valid,
        "correct": correct,
        "message": message
    })

    status = "✅" if correct else "❌"

    print(f"\n{status} 测试 {item['id']}")
    print(f"SQL：{sql}")
    print(f"预期通过：{should_pass}")
    print(f"实际通过：{is_valid}")
    print(f"校验信息：{message}")


correct_count = sum(
    1 for result in results
    if result["correct"]
)

total_count = len(results)
accuracy = correct_count / total_count


print("\n" + "=" * 70)
print("Safety Evaluation 完成")
print(f"测试数量：{total_count}")
print(f"判断正确：{correct_count}")
print(f"Safety Blocking Accuracy：{accuracy:.2%}")