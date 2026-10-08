# Metric Dictionary

## 1. 交易金额

**Metric Name:** transaction_amount

**Business Definition:**  
统计周期内成功交易的交易金额合计。

**Calculation:**  
SUM(transactions.amount)

**Filter:**  
transactions.status = 'SUCCESS'

**Source Table:**  
transactions

---

## 2. 交易客户数

**Metric Name:** transaction_customer_count

**Business Definition:**  
统计周期内至少发生一笔成功交易的去重客户数。

**Calculation:**  
COUNT(DISTINCT transactions.customer_id)

**Filter:**  
transactions.status = 'SUCCESS'

**Source Table:**  
transactions

---

## 3. 客均交易金额

**Metric Name:** avg_amount_per_customer

**Business Definition:**  
统计周期内成功交易金额除以成功交易客户数。

**Calculation:**  
SUM(transactions.amount) / COUNT(DISTINCT transactions.customer_id)

**Filter:**  
transactions.status = 'SUCCESS'

**Source Table:**  
transactions

---

## 4. 营销触达客户数

**Metric Name:** campaign_customer_count

**Business Definition:**  
统计周期内接受过营销触达的去重客户数。

**Calculation:**  
COUNT(DISTINCT campaigns.customer_id)

**Source Table:**  
campaigns

---

## 5. 营销转化客户数

**Metric Name:** converted_customer_count

**Business Definition:**  
统计周期内营销触达后发生转化的去重客户数。

**Calculation:**  
COUNT(DISTINCT CASE WHEN converted = 1 THEN customer_id END)

**Source Table:**  
campaigns

---

## 6. 营销转化率

**Metric Name:** campaign_conversion_rate

**Business Definition:**  
发生转化的营销触达次数占全部营销触达次数的比例。

**Calculation:**  
SUM(campaigns.converted) / COUNT(*)

**Source Table:**  
campaigns