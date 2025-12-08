---
title: "\U0001F525 Day 7: PySpark Joins, Unions, and GroupBy Guide"
cover_image: 'https://raw.githubusercontent.com/sandeepk27/Spark/main/cover_images/Day%207.png'
published: true
description: Essential of Pysaprk
tags: 'dataengineering, python, spark, bigdata'
linkedin_image: 'yes'
id: 3091975
date: '2025-12-08T10:46:18Z'
---

Welcome to Day 7 of your Spark Mastery journey!

Today is one of the most practical days because joins, unions, and aggregations are used in almost every pipeline you will ever build — be it feature engineering, building fact tables, or aggregating transactional data.

Let’s master the fundamentals with clarity and real-world examples.


🌟 **1. Joins in PySpark — The Heart of ETL Pipelines**

A join merges two DataFrames based on keys, similar to SQL.

Basic join:

```
df.join(df2, df.id == df2.id, "inner")
```

Join on same column name:

```
df.join(df2, ["id"], "left")
```

🔹 **Types of Joins in Spark**
Join Type  -	Meaning
inner      -	Matching rows
left	   -    All rows from left, match from right
right	   -    All rows from right
full	   -    All rows from both
left_anti  -	Rows in left NOT in right
left_semi  -	Rows in left WHERE match exists in right
cross	Cartesian product

**Important**
`left_semi = existence check
left_anti = anti-join / unmatched rows
`

🌟 **2. Union — Stack DataFrames Vertically**

Union (same schema, same order)

```
df.union(df2)
```

Union by column names:

```
df.unionByName(df2)
```

Why important?
Because in real projects you combine:
- monthly files
- daily ingestion datasets
- partitions

🌟 **3. GroupBy + Aggregation — Business Logic Layer**

This is how reports, fact tables, metrics are built.

Example:

```
df.groupBy("dept").agg(
sum("salary").alias("total_salary"),
avg("age").alias("avg_age")
)
```

🔹 count vs countDistinct
```
df.select(count("id"))
df.select(countDistinct("id"))
```

🔹 approx_count_distinct (faster!)
```
df.select(approx_count_distinct("id"))
```

🌟 **4. Real ETL Example — Sales Aggregation**

Suppose you have:
- sales table
- product table

Join them:
```
df_joined = sales.join(products, "product_id", "left")
```

Aggregate revenue:

```
df_agg = df_joined.groupBy("category").agg(
 sum("amount").alias("total_revenue"),
    count("*").alias("transactions")
)
```

This is EXACTLY how business dashboards are built.


🌟 **5. Join Performance Optimization**

Use Broadcast Join for small lookup tables:

```
df.join(broadcast(df_small), "id")
```

Why?
`Avoids shuffle → runs much faster.`

🚀 **Summary of Day 7**

Today we learnt:
- Joins
- Union / UnionByName
- GroupBy
- Aggregations
- broadcast join optimization

Follow for more such content. Let me know if I missed anything in comments. Thank you!!


![Day 7](https://raw.githubusercontent.com/sandeepk27/Spark/main/images/Day%207.png)
