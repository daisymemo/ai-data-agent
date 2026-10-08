import duckdb


# 连接刚刚创建的数据库
conn = duckdb.connect("database.duckdb")


# 写一条 SQL
sql = """
SELECT
    customer_level,
    COUNT(*) AS customer_count
FROM customers
GROUP BY customer_level
ORDER BY customer_count DESC
"""


# 执行 SQL，并把结果转换成 DataFrame
result = conn.execute(sql).df()


# 打印查询结果
print(result)


# 关闭数据库连接
conn.close()