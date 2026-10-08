from pathlib import Path
import re

KNOWLEDGE_DIR = Path("knowledge")


def split_markdown_by_heading(text):
    """
    按 Markdown 的二级标题 ## 切分知识。
    每个标题及其下面的内容作为一个独立知识块。
    """
    sections = re.split(r"(?=^##\s+)", text, flags=re.MULTILINE)

    chunks = []

    for section in sections:
        section = section.strip()

        if section.startswith("## "):
            chunks.append(section)

    return chunks


def load_knowledge_chunks():
    chunks = []

    for filename in ["data_dictionary.md", "metrics.md"]:

        path = KNOWLEDGE_DIR / filename
        text = path.read_text(encoding="utf-8")

        sections = split_markdown_by_heading(text)

        for section in sections:
            chunks.append({
                "source": filename,
                "content": section
            })

    return chunks


if __name__ == "__main__":

    chunks = load_knowledge_chunks()

    print(f"共生成 {len(chunks)} 个知识块\n")

    for i, chunk in enumerate(chunks, start=1):

        print("=" * 60)
        print(f"Chunk {i}")
        print(f"来源：{chunk['source']}")
        print(chunk["content"])
        print()