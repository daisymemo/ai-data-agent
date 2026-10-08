import duckdb


# 数据库文件保存位置
DB_PATH = "database.duckdb"

# 连接数据库
# 如果数据库不存在，DuckDB 会自动创建
conn = duckdb.connect(DB_PATH)


# -----------------------------
# 1. Customers 客户表
# -----------------------------

conn.execute("""
CREATE OR REPLACE TABLE customers AS
SELECT *
FROM read_csv_auto('data/customers.csv');
""")


# -----------------------------
# 2. Products 产品表
# -----------------------------

conn.execute("""
CREATE OR REPLACE TABLE products AS
SELECT *
FROM read_csv_auto('data/products.csv');
""")


# -----------------------------
# 3. Transactions 交易表
# -----------------------------

conn.execute("""
CREATE OR REPLACE TABLE transactions AS
SELECT *
FROM read_csv_auto('data/transactions.csv');
""")


# -----------------------------
# 4. Campaigns 营销触达表
# -----------------------------

conn.execute("""
CREATE OR REPLACE TABLE campaigns AS
SELECT *
FROM read_csv_auto('data/campaigns.csv');
""")


# -----------------------------
# 检查每张表的数据量
# -----------------------------

tables = [
    "customers",
    "products",
    "transactions",
    "campaigns",
]

print("数据库创建完成：\n")

for table in tables:
    count = conn.execute(
        f"SELECT COUNT(*) FROM {table}"
    ).fetchone()[0]

    print(f"{table}: {count} rows")


conn.close()