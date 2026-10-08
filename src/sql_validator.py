import duckdb 



ALLOWED_TABLES = {
    "customers",
    "products",
    "transactions",
    "campaigns",
}

import sqlglot
from sqlglot import exp


def validate_sql(sql,db_path="database.duckdb"):
    """
    校验 SQL 是否为安全的只读查询。
    """

    try:
        parsed = sqlglot.parse_one(sql, dialect="duckdb")
    except Exception as e:
        return False, f"SQL 解析失败：{e}"

    # 最外层必须是查询语句
    if not isinstance(parsed, exp.Query):
        return False, "只允许执行查询语句"

    # 禁止任何数据修改或数据库结构修改操作
    forbidden_types = (
        exp.Insert,
        exp.Update,
        exp.Delete,
        exp.Drop,
        exp.Create,
        exp.Alter,
    )

    for node in parsed.walk():
        if isinstance(node, forbidden_types):
            return False, f"检测到危险操作：{type(node).__name__}"

    # 获取 CTE 名称，避免把 WITH 中定义的临时表误判为非法表
    cte_names = {
        cte.alias_or_name
        for cte in parsed.find_all(exp.CTE)
    }

    # 检查 SQL 实际访问的数据库表
    for table in parsed.find_all(exp.Table):
        table_name = table.name

        if table_name not in ALLOWED_TABLES and table_name not in cte_names:
            return False, f"不允许访问表：{table_name}"

 # 使用 DuckDB 检查表、字段及 SQL 语义是否合法
    try:
        conn = duckdb.connect(db_path, read_only=True)
        conn.execute(f"EXPLAIN {sql}")
        conn.close()
    except Exception as e:
        return False, f"SQL 语义校验失败：{e}"

    
    return True, "SQL 校验通过"


if __name__ == "__main__":

    test_cases = [
        "SELECT * FROM customers",

        "DELETE FROM customers WHERE customer_id = 'C001'",

        "DROP TABLE customers",

        """
        WITH high_value AS (
            SELECT customer_id
            FROM transactions
            WHERE amount > 1000
        )
        SELECT * FROM high_value
        """,

        "SELECT customer_name FROM customers"
    ]

    for sql in test_cases:
        is_valid, message = validate_sql(sql)

        print("SQL:")
        print(sql.strip())
        print("校验结果:", is_valid, message)
        print("-" * 50)