import pandas as pd

import os
import random
from datetime import datetime, timedelta

import pandas as pd


# 固定随机种子
# 这样每次运行程序，生成的数据都保持一致
random.seed(42)

# 数据保存目录
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)


# -----------------------------
# Customers 客户表
# -----------------------------

# 模拟 1000 名客户
n_customers = 1000

# 客户可能来自的地区
regions = ["深圳", "广州", "杭州", "武汉", "上海"]

# 客户注册渠道
channels = ["APP", "微信", "线下网点", "合作渠道"]

# 客户等级
customer_levels = ["Normal", "Silver", "Gold", "Platinum"]

# 数据截止日期
end_date = datetime(2026, 9, 18)

# 假设客户是在过去两年内注册的
start_date = end_date - timedelta(days=730)

customers = []

for i in range(1, n_customers + 1):

    # 随机生成注册日期
    registration_date = start_date + timedelta(
        days=random.randint(0, 730)
    )

    # 不同客户等级的人数并不是平均分布
    level = random.choices(
        customer_levels,
        weights=[50, 25, 18, 7],
        k=1
    )[0]

    customer = {
        "customer_id": f"C{i:06d}",
        "registration_date": registration_date.date(),
        "channel": random.choice(channels),
        "region": random.choice(regions),
        "customer_level": level,
        "birth_year": random.randint(1965, 2004),
    }

    customers.append(customer)


# 转换为 DataFrame
customers_df = pd.DataFrame(customers)

# 保存为 CSV
customers_df.to_csv(
    f"{DATA_DIR}/customers.csv",
    index=False
)

print(customers_df.head())

print(f"\n客户数据生成完成，共 {len(customers_df)} 行。")



# -----------------------------
# Products 产品表
# -----------------------------

products = [
    ["P001", "稳健产品A", "Wealth", 1000],
    ["P002", "稳健产品B", "Wealth", 2000],
    ["P003", "成长产品A", "Wealth", 3000],
    ["P004", "支付服务A", "Payment", 200],
    ["P005", "支付服务B", "Payment", 500],
    ["P006", "会员服务A", "Membership", 300],
    ["P007", "会员服务B", "Membership", 600],
    ["P008", "增值服务A", "ValueAdded", 800],
]

products_df = pd.DataFrame(
    products,
    columns=[
        "product_id",
        "product_name",
        "product_type",
        "unit_price",
    ]
)

products_df.to_csv(
    f"{DATA_DIR}/products.csv",
    index=False
)

print("\n产品数据预览：")
print(products_df)

print(f"\n产品数据生成完成，共 {len(products_df)} 行。")

# -----------------------------
# Transactions 交易表
# -----------------------------

transactions = []

# 取出已有的客户ID和产品ID
customer_ids = customers_df["customer_id"].tolist()
product_ids = products_df["product_id"].tolist()

# 不同客户等级设置不同的消费金额系数
# 这样模拟数据中会存在一些真实可分析的业务规律
level_multiplier = {
    "Normal": 0.7,
    "Silver": 1.0,
    "Gold": 1.5,
    "Platinum": 2.2,
}

# 建立 customer_id → customer_level 的对应关系
customer_level_map = dict(
    zip(
        customers_df["customer_id"],
        customers_df["customer_level"]
    )
)

# 模拟8000笔交易
n_transactions = 8000

# 交易发生在过去约18个月
transaction_start = end_date - timedelta(days=540)

for i in range(1, n_transactions + 1):

    # 随机选择一个客户
    customer_id = random.choice(customer_ids)

    # 随机选择一个产品
    product_id = random.choice(product_ids)

    # 找到该客户的等级
    level = customer_level_map[customer_id]

    # 找到对应产品的基础价格
    base_price = products_df.loc[
        products_df["product_id"] == product_id,
        "unit_price"
    ].iloc[0]

    # 每笔交易购买1～3个单位
    quantity = random.randint(1, 3)

    # 不同客户等级对应不同金额系数
    multiplier = level_multiplier[level]

    # 模拟实际交易金额
    amount = round(
        base_price
        * quantity
        * multiplier
        * random.uniform(0.8, 1.2),
        2
    )

    # 随机生成交易日期
    transaction_date = (
        transaction_start
        + timedelta(
            days=random.randint(
                0,
                (end_date - transaction_start).days
            )
        )
    )

    # 模拟交易状态：95%成功，5%失败
    status = random.choices(
        ["SUCCESS", "FAILED"],
        weights=[95, 5],
        k=1
    )[0]

    transactions.append(
        {
            "transaction_id": f"T{i:07d}",
            "customer_id": customer_id,
            "product_id": product_id,
            "transaction_date": transaction_date.date(),
            "quantity": quantity,
            "amount": amount,
            "status": status,
        }
    )


transactions_df = pd.DataFrame(transactions)

transactions_df.to_csv(
    f"{DATA_DIR}/transactions.csv",
    index=False
)

print("\n交易数据预览：")
print(transactions_df.head())

print(
    f"\n交易数据生成完成，共 {len(transactions_df)} 行。"
)


# -----------------------------
# Campaigns 营销触达表
# -----------------------------


# 营销活动类型
campaign_types = [
    "新客激活",
    "高价值客户提升",
    "沉默客户唤醒",
    "产品交叉销售",
]

# 营销触达渠道
touch_channels = [
    "企业微信",
    "APP Push",
    "短信",
    "客户经理",
]

campaigns = []

# 模拟3000次营销触达
n_campaigns = 3000

# 营销触达发生在过去一年
campaign_start = end_date - timedelta(days=365)

# 不同等级客户设置不同的转化概率
# 让模拟数据中存在可以被分析发现的业务规律
conversion_prob = {
    "Normal": 0.08,
    "Silver": 0.15,
    "Gold": 0.25,
    "Platinum": 0.35,
}

for i in range(1, n_campaigns + 1):

    # 随机选择一个客户
    customer_id = random.choice(customer_ids)

    # 获取客户等级
    level = customer_level_map[customer_id]

    # 随机生成触达日期
    touch_date = (
        campaign_start
        + timedelta(
            days=random.randint(
                0,
                (end_date - campaign_start).days
            )
        )
    )

    # 根据客户等级模拟是否转化
    converted = (
        1
        if random.random() < conversion_prob[level]
        else 0
    )

    # 默认没有转化日期
    conversion_date = None

    # 如果发生转化，假设在触达后0～14天内完成
    if converted == 1:
        conversion_date = (
            touch_date
            + timedelta(days=random.randint(0, 14))
        ).date()

    campaigns.append(
        {
            "campaign_id": f"M{i:06d}",
            "customer_id": customer_id,
            "campaign_type": random.choice(campaign_types),
            "touch_date": touch_date.date(),
            "touch_channel": random.choice(touch_channels),
            "converted": converted,
            "conversion_date": conversion_date,
        }
    )


campaigns_df = pd.DataFrame(campaigns)

campaigns_df.to_csv(
    f"{DATA_DIR}/campaigns.csv",
    index=False
)

print("\n营销触达数据预览：")
print(campaigns_df.head())

print(
    f"\n营销触达数据生成完成，共 {len(campaigns_df)} 行。"
)