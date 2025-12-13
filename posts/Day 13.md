---
title: 'Day 13: Window Functions in PySpark'
cover_image: 'https://raw.githubusercontent.com/sandeepk27/Spark/main/cover-images/Day%2013.jpg'
published: true
description: Learn how UDF vs Pandas UDF — Why 80% of Spark Developers Use UDFs Wrong (And How to Fix It)
tags: 'python, dataengineering, spark, bigdata'
linkedin_image: 'no'
devto_cover: 'yes'
id: 3103540
date: '2025-12-13T14:05:23Z'
---

Welcome to Day 13 of the Spark Mastery Series.
Today we cover Window Functions - one of the most powerful and commonly asked topics in Spark interviews.

If you know window functions, you can:
- Deduplicate records
- Rank data
- Calculate running totals
- Compare current row with previous values
- Implement SCD logic

Let’s master them step by step.

🌟 **1. What are Window Functions?**

Window functions compute values across a set of rows related to the current row, while still returning one output row per input row.

Unlike groupBy, window functions do NOT reduce rows.


🌟 **2. Defining a Window**
```
from pyspark.sql.window import Window
window_spec = Window.partitionBy("dept").orderBy("salary")
```

This defines:
- A logical group (dept)
- Ordering inside each group


🌟 **3. Ranking Functions**

🔹 row_number()

Assigns a unique number per row.
```
df.withColumn("row_num", row_number().over(window_spec))
```

Use cases:
- Deduplication
- Latest record selection

🔹 rank()

Same rank for ties, but gaps appear.

🔹 dense_rank()

Same rank for ties, no gaps.

These are heavily used in top-N queries.


🌟 **4. lead() and lag() — Time Travel Across Rows**

Compare current row with previous/next rows.
```
df.withColumn("prev_salary", lag("salary").over(window_spec))
```

Use cases:
- Month-over-month comparison
- Trend analysis
- Change detection

🌟 **5. Running Totals & Cumulative Metrics**

```
window_run = Window.partitionBy("dept") \
                   .orderBy("date") \
                   .rowsBetween(Window.unboundedPreceding, Window.currentRow)

df.withColumn("running_sum", sum("amount").over(window_run))
```

Used in:
- Financial analytics
- KPI calculations
- Revenue accumulation

🌟 **6. Deduplication — Real-World Use Case**

Keep only the latest record per ID:

```
window_latest = Window.partitionBy("id").orderBy(col("updated_at").desc())

df_latest = df.filter(row_number().over(window_latest) == 1)
```

This pattern is extremely common in SCD pipelines.

🌟 **7. Window vs GroupBy**

groupBy          window

Aggregates rows	 Keeps all rows
Faster	         Slightly slower
Summarization	   Analytics & comparisons

Use window functions when you need row-level context.

🚀 **Summary**

We learned:
- What window functions are
- partitionBy & orderBy
- row_number, rank, dense_rank
- lead & lag
- Running totals
- Deduplication patterns

Follow for more such content. Let me know if I missed anything in comments. Thank you!!
