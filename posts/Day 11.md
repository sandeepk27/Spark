---
title: 'Day 11: Choosing the Right File Format in Spark'
published: true
description: 'Learn how to optimize Spark Joins using broadcast variables, skew handling, and strategic repartitioning.'
tags: 'python, dataengineering, spark, bigdata'
linkedin_image: 'no'
devto_cover: 'yes'
---

Welcome to Day 11 of the Spark Mastery Series!
Today we discuss one of the most underrated but most impactful decisions in data engineering:

> Which file format should you use in Spark?

Choosing the wrong format can make your job 10x slower and 5x more expensive. Let's break down the formats clearly.


🌟 CSV - “Easy but Slow”

CSV is the simplest, but it is NOT optimized for big data.

Drawbacks:
- No schema
- No compression
- No pushdown
- No columnar storage
- Slow read performance

Example:

```
df = spark.read.csv("data.csv", header=True, inferSchema=True)

```

Use CSV only in:
- Raw ingestion (Bronze layer)
- External source feeds


🌟 **JSON — Great for Logs, Bad for Analytics**

**Pros:**
- Handles nested structures well
- Useful for logs, API events

**Cons:**
- Slow
- Not columnar
- Weak compression

```
df = spark.read.json("logs.json")
```


🌟 **Parquet — The King of Analytics**

Parquet is a columnar, compressed, optimized format.

Why it’s the industry standard:
- Reads are fast
- Supports predicate pushdown
- Supports column pruning
- Highly compressed
- Splittable

```
df.write.parquet("path")
```

If you're building analytics or ETL, Parquet is your default format.


🌟 **ORC — The Hadoop Favorite**

ORC is similar to Parquet:
- Columnar
- Compressed
- Pushdown support


ORC is heavily used in:
- Hadoop
- Hive

But Parquet is more popular in cloud platforms like:
- Databricks
- AWS
- GCP

🌟 **Delta Lake — The Modern Lakehouse Format**

`Delta = Parquet + ACID + Time Travel`

Benefits:
- Atomic writes
- Schema evolution
- MERGE INTO support
- Faster ingestion
- Faster updates
- Versioned tables


Perfect for:
- Bronze → Silver → Gold ETL pipelines
- ML feature store
- Time travel debugging

```
df.write.format("delta").save("path")
```


🌟 **How to Choose the Right Format?**

Use CSV
→ Only for ingestion/raw dumps

Use JSON
→ Only for logs, events, nested data

Use Parquet
→ For analytics, BI, aggregations

Use Delta
→ For ETL pipelines, updates, deletes, SCD2


🌟 Real-World Example

For a retail data system:

`
---
Layer              Format

Bronze (raw)	     CSV, JSON
Silver (cleaned)   Parquet
Gold (analytics)   Delta
`

This is exactly how modern Lakehouse systems are built.

🚀 **Summary**

We learned:
- Differences between file formats
- Why Parquet & Delta are fastest
- Why CSV & JSON hurt performance
- Pushdown & column pruning
- How file formats impact ETL pipelines

Follow for more such content. Let me know if I missed anything in comments. Thank you!!
