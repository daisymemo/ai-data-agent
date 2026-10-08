import duckdb
from pathlib import Path


DB_PATH = "database.duckdb"
KNOWLEDGE_DIR = Path("knowledge")


def get_database_schema():
    """读取 DuckDB 中所有业务表及字段信息。"""

    conn = duckdb.connect(DB_PATH)

    tables = conn.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'main'
        ORDER BY table_name
    """).fetchall()

    schema_parts = []

    for (table_name,) in tables:

        columns = conn.execute(
            f"DESCRIBE {table_name}"
        ).fetchall()

        schema_parts.append(
            f"TABLE: {table_name}"
        )

        for column in columns:
            column_name = column[0]
            column_type = column[1]

            schema_parts.append(
                f"  - {column_name}: {column_type}"
            )

        schema_parts.append("")

    conn.close()

    return "\n".join(schema_parts)


def read_knowledge_file(filename):
    """读取 knowledge 文件夹中的业务知识文件。"""

    file_path = KNOWLEDGE_DIR / filename

    return file_path.read_text(
        encoding="utf-8"
    )

def build_context():
    """构建提供给 LLM 的完整数据上下文。"""

    schema = get_database_schema()
    data_dictionary = read_knowledge_file("data_dictionary.md")
    metrics = read_knowledge_file("metrics.md")

    context = f"""
# Database Schema
{schema}

# Data Dictionary
{data_dictionary}

# Metric Dictionary
{metrics}
"""

    return context

if __name__ == "__main__":

    schema = get_database_schema()

    data_dictionary = read_knowledge_file(
        "data_dictionary.md"
    )

    metrics = read_knowledge_file(
        "metrics.md"
    )

    print("===== DATABASE SCHEMA =====")
    print(schema)

    print("\n===== DATA DICTIONARY =====")
    print(data_dictionary)

    print("\n===== METRIC DICTIONARY =====")
    print(metrics)