from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.knowledge_chunker import load_knowledge_chunks


# 1. 加载知识块
chunks = load_knowledge_chunks()

texts = [
    chunk["content"]
    for chunk in chunks
]


# 2. 将知识块转换成 TF-IDF 向量
# 使用字符级 n-gram，对中文检索更友好
vectorizer = TfidfVectorizer(
    analyzer="char",
    ngram_range=(2, 4)
)

knowledge_vectors = vectorizer.fit_transform(texts)


def retrieve(question, top_k=3):
    """
    根据用户问题，召回最相关的 Top-K 个知识块。
    """

    # 把用户问题转换成同一套向量
    question_vector = vectorizer.transform([question])

    # 计算问题与所有知识块的相似度
    similarities = cosine_similarity(
        question_vector,
        knowledge_vectors
    )[0]

    # 按相似度从高到低排序
    top_indices = similarities.argsort()[::-1][:top_k]

    results = []

    for index in top_indices:
        results.append({
            "score": similarities[index],
            "source": chunks[index]["source"],
            "content": chunks[index]["content"]
        })

    return results


if __name__ == "__main__":

    question = "不同营销渠道的转化率怎么样？"

    results = retrieve(question)

    print(f"用户问题：{question}\n")

    for i, result in enumerate(results, start=1):
        print("=" * 60)
        print(f"Top {i}")
        print(f"相似度：{result['score']:.4f}")
        print(f"来源：{result['source']}")
        print(result["content"])
        print()