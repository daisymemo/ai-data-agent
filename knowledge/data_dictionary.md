# Data Dictionary

## customers
客户基础信息表，一行代表一名客户。

| Field | Type | Description |
|---|---|---|
| customer_id | VARCHAR | 客户唯一标识，主键 |
| registration_date | DATE | 客户注册日期 |
| channel | VARCHAR | 客户注册渠道，包括 APP、微信、线下网点、合作渠道 |
| region | VARCHAR | 客户所在地区 |
| customer_level | VARCHAR | 客户等级，包括 Normal、Silver、Gold、Platinum |
| birth_year | INTEGER | 客户出生年份 |

## products
产品基础信息表，一行代表一个产品。

| Field | Type | Description |
|---|---|---|
| product_id | VARCHAR | 产品唯一标识，主键 |
| product_name | VARCHAR | 产品名称 |
| product_type | VARCHAR | 产品类型，包括 Wealth、Payment、Membership、ValueAdded |
| unit_price | INTEGER | 产品基础价格 |

## transactions
交易明细表，一行代表一笔交易。

| Field | Type | Description |
|---|---|---|
| transaction_id | VARCHAR | 交易唯一标识，主键 |
| customer_id | VARCHAR | 客户标识，关联 customers.customer_id |
| product_id | VARCHAR | 产品标识，关联 products.product_id |
| transaction_date | DATE | 交易日期 |
| quantity | INTEGER | 交易数量 |
| amount | DECIMAL | 交易金额 |
| status | VARCHAR | 交易状态，包括 SUCCESS、FAILED |

## campaigns
营销触达明细表，一行代表一次对客户的营销触达。

| Field | Type | Description |
|---|---|---|
| campaign_id | VARCHAR | 营销触达唯一标识，主键 |
| customer_id | VARCHAR | 客户标识，关联 customers.customer_id |
| campaign_type | VARCHAR | 营销活动类型 |
| touch_date | DATE | 触达日期 |
| touch_channel | VARCHAR | 触达渠道，包括企业微信、APP Push、短信、客户经理 |
| converted | INTEGER | 是否转化，1=转化，0=未转化 |
| conversion_date | DATE | 转化日期；未转化时为空 |