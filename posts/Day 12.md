---
title: 'Day 12: UDF vs Pandas UDF'
cover_image: 'https://raw.githubusercontent.com/sandeepk27/Spark/main/cover-images/Day%2012.jpg'
published: true
description: Learn how UDF vs Pandas UDF — Why 80% of Spark Developers Use UDFs Wrong (And How to Fix It)
tags: 'python, dataengineering, spark, bigdata'
linkedin_image: 'no'
devto_cover: 'yes'
id: 3100498
date: '2025-12-11T19:44:38Z'
---

Welcome to Day 12 of the Spark Mastery Series!
Today we dissect a topic that has ruined the performance of countless ETL pipelines:

> UDFs (User Defined Functions)

A UDF seems innocent - but adding one UDF can slow your entire job by 10x.

Let’s understand why and how to avoid that with better alternatives.

🌟 **1. What is a UDF?**

A UDF (User Defined Function) is a Python function applied on Spark DataFrame.

Example:

```
from pyspark.sql.functions import udf

@udf("string")
def reverse_name(name):
    return name[::-1]
```

This works…
But it's slow, because Spark must:
- Ship each record to Python
- Execute Python code
- Convert result back to JVM
- Merge with DataFrame

`Every record goes through Python → JVM boundary → slow.`


🌟 **2. Built-in Functions — ALWAYS Preferred**

These are the functions Spark provides internally:
```
df.withColumn("upper_name", upper(col("name")))
```

Why they are fastest:
- Implemented in Scala (native)
- Vectorized
- Optimized by Catalyst
- Support predicate pushdown
- Support column pruning

Rule:
> If Spark has a built-in function → NEVER write a UDF.


🌟 **3. Pandas UDF — The Best Alternative to Normal UDFs**

> Regular UDF = row-by-row in Python.

> Pandas UDF = uses Apache Arrow for vectorized operations → much faster.

Example:

```
from pyspark.sql.functions import pandas_udf

@pandas_udf("double")
def multiply_by_two(col):
    return col * 2
```

Spark sends data in batches, not row-by-row → huge speed improvement.


🌟 **4. Types of Pandas UDFs**

🟢 Scalar Pandas UDF
Operates like built-in function.
```
@pandas_udf("double")
def add_one(col):
    return col + 1
```

🔵 Grouped Map UDF
Operates on a full pandas DataFrame for each group.

```
@pandas_udf(schema, PandasUDFType.GROUPED_MAP)
```
Example use cases:
- Time-series transformation
- Per-user model training
- Per-group cleaning

🔴 Grouped Aggregate UDF

```
@pandas_udf("double", PandasUDFType.GROUPED_AGG)
```

Good for:
- statistical aggregation
- ML metrics


🌟 **5. When Should You Use a Normal UDF?**

Only when:

- No built-in function
- Not vectorizable
- Lots of custom Python logic

Very rare in ETL pipelines.


🌟 **6. Real Example:** Performance Difference

Using UDF:
```
Time: 50 seconds
```

Using Pandas UDF:
```
Time: 8 seconds
```

Using built-in function:

```
Time: 1 second
```
This is the reason senior engineers avoid UDFs completely unless needed.


🌟 **7. Summary Guidelines**

✔ Use built-in functions whenever possible
✔ Use Pandas UDF when logic is vectorizable
✔ Use normal UDF rarely
✔ Avoid UDFs on large data
✔ Avoid using UDF inside joins or filters
✔ Evaluate execution plan using .explain()


🚀 **Summary**

We learned:
- Difference between UDF and Pandas UDF
- Why Python UDF is slow
- When to avoid UDFs
- When Pandas UDF is best
- Best practices for performance

Follow for more such content. Let me know if I missed anything in comments. Thank you!!
