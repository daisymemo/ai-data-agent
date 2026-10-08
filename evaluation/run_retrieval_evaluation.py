import json
from pathlib import Path

from src.retriever import retrieve


TEST_FILE = Path("evaluation/retrieval_test_cases.json")


with open(TEST_FILE, "r", encoding="utf-8") as f:
    test_cases = json.load(f)


results = []

for item in test_cases:
    question = item["question"]
    expected_keyword = item["expected_keyword"]

    # 与 Text2SQL 保持一致：取 Top 3
    retrieved_chunks = retrieve(question, top_k=3)

    # 检查正确指标是否出现在 Top 3 中
    hit = any(
        expected_keyword in chunk["content"]
        for chunk in retrieved_chunks
    )

    results.append({
        "id": item["id"],
        "question": question,
        "expected_keyword": expected_keyword,
        "hit": hit
    })

    status = "✅" if hit else "❌"

    print(f"\n{status} 测试 {item['id']}")
    print(f"问题：{question}")
    print(f"目标知识：{expected_keyword}")

    print("Top 3 检索结果：")
    for rank, chunk in enumerate(retrieved_chunks, start=1):
        first_line = chunk["content"].splitlines()[0]
        print(
            f"  Top {rank} | "
            f"score={chunk['score']:.4f} | "
            f"{first_line}"
        )


hit_count = sum(
    1 for result in results
    if result["hit"]
)

total_count = len(results)
recall_at_3 = hit_count / total_count


print("\n" + "=" * 70)
print("Retrieval Evaluation 完成")
print(f"测试数量：{total_count}")
print(f"成功召回：{hit_count}")
print(f"Recall@3：{recall_at_3:.2%}")