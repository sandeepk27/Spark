---
title: 'Day 9: Spark SQL Deep Dive - Temp Views, Query Execution & Optimization Tips for Data Engineers'
published: true
description: 'Learn how to optimize Spark Joins using broadcast variables, skew handling, and strategic repartitioning.'
tags: 'python, dataengineering, spark, bigdata'
linkedin_image: 'no'
devto_cover: 'no'
---

Welcome to Day 9 of the Spark Mastery Series!
Today we explore one of the most widely used features in PySpark — Spark SQL.

Even if you're a Python engineer, SQL is STILL the easiest and fastest way to express business logic. Spark SQL allows you to use familiar SQL syntax while leveraging Spark’s distributed execution engine.

Let’s dive in.

🌟 **1. What is Spark SQL?**

Spark SQL enables:
- Writing SQL directly on DataFrames
- Querying structured + semi-structured data
- Using SQL to express ETL transformations
- Creating tables and views
- Integrating with BI tools

It is powered by Catalyst Optimizer, making SQL queries in Spark both expressive and fast.

🌟 **2. Creating Temporary Views — The Bridge Between SQL and DataFrames**

🟢 Local Temp View

Visible only inside current session:

```
df.createOrReplaceTempView("employees")
spark.sql("SELECT * FROM employees")
```

🔵 Global Temp View

Visible across sessions and Spark applications:

```
df.createOrReplaceGlobalTempView("employees")
spark.sql("SELECT * FROM global_temp.employees")
```

Useful in:
- Multi-session workloads
- Shared ETL pipelines


🌟 **3. Running SQL Queries**

```
spark.sql("""
SELECT dept, COUNT(*) AS total 
FROM employees 
GROUP BY dept
""").show()
```

You can do everything SQL supports:
- joins
- aggregations
- subqueries
- window functions
- CTEs

🌟 **4. Spark Catalog — Explore Your Data Environment**

Spark maintains metadata of:

- tables
- functions
- databases

Useful commands:

```
spark.catalog.listTables()
spark.catalog.listDatabases()
spark.catalog.listColumns("employees")
```
This helps engineers understand schema dependencies in pipelines.

🌟 **5. SQL Table Creation**

Spark SQL supports DDL statements:
```
CREATE TABLE sales 
USING parquet 
OPTIONS (path '/mnt/data/sales');
```

To insert:
```
INSERT INTO sales SELECT * FROM new_sales;
```

🌟 **6. Query Execution Explained**

Steps: 
1️⃣ Parse SQL query
2️⃣ Build Logical Plan
3️⃣ Optimize plan using Catalyst
4️⃣ Build Physical Plan
5️⃣ Execute using Tungsten engine

```
spark.sql("SELECT * FROM employees").explain(True)
```

This prints:
- Parsed logical plan
- Analyzed logical plan
- Optimized logical plan
- Physical plan

🌟 **7. SQL Performance Optimization Tips**
✔ Always filter on partition columns
✔ Use Parquet OR Delta instead of CSV
✔ Avoid UDFs — they break optimization
✔ Use broadcast on small tables
✔ Avoid unnecessary ORDER BY (shuffle-heavy)
✔ Avoid SELECT *

🌟 **8. Register UDFs in SQL**

Sometimes SQL needs Python logic.

```
spark.udf.register("upper_udf", lambda x: x.upper(), "string")

spark.sql("SELECT upper_udf(name) FROM employees")
```

But remember:

⚠ UDFs disable many Catalyst optimizations → try to avoid unless necessary.


🚀 **Summary**
Today we learned:
- Temp Views
- Global Temp Views
- Spark SQL
- Catalog functions
- SQL optimization
- Query execution plan
- SQL-UDF integration

Follow for more such content. Let me know if I missed anything in comments. Thank you!!
