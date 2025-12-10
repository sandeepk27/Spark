---
title: 'Day 8: Accelerating Spark Joins - Broadcast, Shuffle Optimization & Skew Handling'
cover_image: https://raw.githubusercontent.com/sandeepk27/Spark/main/cover-images/Day%208.jpg
published: true
description: 'Learn how to optimize Spark Joins using broadcast variables, skew handling, and strategic repartitioning.'
tags: 'dataengineering, python, spark, bigdata'
linkedin_image: 'no'
devto_cover: 'yes'
id: 3094458
date: '2025-12-09T10:34:25Z'
---

Welcome to Day 8 of the Spark Mastery Series.
Today we deep-dive into the topic that makes or breaks ETL pipelines:

Joins and performance optimization.

'If you master today’s concepts, you can improve Spark jobs from 2 hours → 10 minutes.'
Let’s begin.


🌟 **1. Why Are Joins Slow in Spark?**

When Spark performs a join, it often must shuffle data across executors so rows with the same join key end up in the same partition.

Shuffle includes:
- Network transfer
- Disk writes
- Disk reads
- Sorting
- Stage creation

`Shuffles takes 80% of Spark’s execution time in badly optimized pipelines.
`

🌟 **2. Broadcast Joins — The Fastest Join Strategy**

If one dataset is small (< 50MB), broadcast join is the fastest possible way.
```
df_large.join(broadcast(df_small), "id")
```

Why it’s fast?
- Spark copies the small table to all executors
- Each executor performs join locally
- No shuffle required

This can turn a shuffle join into a map-side join — extremely fast.

🌟 **3. Repartitioning Before Join**
If two DataFrames have different partitioning strategies, Spark shuffles both.

Solution:
```
df1 = df1.repartition("id")
df2 = df2.repartition("id")

joined = df1.join(df2, "id")
```

Why this helps:

- Ensures partition-level alignment
- Reduces shuffle volume

🌟 **4. Handling Skew — The Most Important Real-World Skill**

Data skew happens when a handful of join keys contain most of the data.

Example:
```
"India" → 5 million records

"USA" → 200,000

"UK" → 10,000
```

This causes:
- long-running tasks
- straggler tasks
- memory overflow
- executor timeout


⭐ Solution 1: Salting Keys
```
df1 = df1.withColumn("salt", floor(rand() * 10))
df2 = df2.withColumn("salt", lit(0))
```
Now join on ["id", "salt"].

⭐ Solution 2: Broadcast the smaller table

⭐ Solution 3: Skew hint

```
df1.hint("skew").join(df2, "id")
```

🌟 **5. Join Strategy Selection (What Spark Uses Internally)**

**SortMergeJoin**
- Default strategy
- Good for large datasets
- Requires shuffle → expensive


**HashJoin**
- Faster
- Requires memory
- Used automatically if possible

🌟 **6. Real-World Example: Retail Sales ETL**
You have:
sales table → 200M records
product table → 50k records

The correct join:

```
df = sales.join(broadcast(products), "product_id")
```
This alone reduces runtime by 10 to 20x.


🚀 **Summary**
- Today you learned how to:
- Identify shuffle-heavy joins
- Remove unnecessary shuffles
- Use broadcast joins
- Fix skew
- Repartition strategically
- Apply join hints

Follow for more such content. Let me know if I missed anything in comments. Thank you!!
