---
title: "🔥 Day 6: Essential PySpark DataFrame Transformations"
published: false
description: Essential of Pysaprk
tags: 'dataengineering, python, spark, bigdata'
---

Welcome back to Day 6 of the Spark Mastery Series!
Today we dive into the most frequently used PySpark transformations that power real-world ETL pipelines.

If you master today’s concepts, you’ll be comfortable writing 80% of all PySpark ETL jobs.

Let’s begin.


🌟 1. Selecting Columns — The Most Basic Transformation

Just like SQL:

df.select("name", "salary").show()

You can modify columns inside select:

df.select(col("salary") * 2).show()



🌟 2. Adding / Modifying Columns with withColumn()

df = df.withColumn("salary_hike", col("salary") * 1.25)

Use withColumn for:

deriving new columns

replacing existing columns

applying functions

adding constants



🌟 3. Adding Constant Value with lit()

df = df.withColumn("country", lit("India"))

Use this when:

tagging data

adding metadata columns (pipeline_run_id, load_date)


🌟 4. Conditional Logic with when()

Equivalent to SQL CASE WHEN.

df = df.withColumn(
    "age_group",
    when(col("age") < 18, "Minor")
    .when(col("age") < 60, "Adult")
    .otherwise("Senior")
)


🌟 5. Filtering Rows

df.filter(col("age") > 25).show()
df.filter((col("age") > 25) & (col("city") == "Hyderabad"))

You can also use .where() which is same as filter.


🌟 6. Removing Columns

df = df.drop("middle_name")



🌟 7. Removing Duplicate Rows

df.dropDuplicates(["id"]).show()

For entire table:

df.distinct()


🌟 8. Sorting Rows

df.orderBy(col("salary").desc())

Sorting triggers shuffle → expensive!
Use only when necessary.


🌟 9. Transformations Chaining (Best Practice)

Good code:

df = (df
      .filter(col("salary") > 30000)
      .withColumn("bonus", col("salary") * 0.10)
      .select("name", "salary", "bonus"))

Bad code:

df = df.filter(...)
df = df.withColumn(...)
df = df.select(...)

Always chain transformations for readability.


🌟 10. Real Use Case Example (Retail ETL)

Given sales data, add GST and categorize purchase:

df = (df
     .withColumn("amount_gst", col("amount") * 1.18)
     .withColumn("category",
                 when(col("amount") > 1000, "Premium")
                 .otherwise("Regular"))
     .filter(col("amount_gst") > 500)
)

This is exactly how real-world ETL transformations look.


🚀 Summary

Today you learned:

select

filter

withColumn

lit

when

drop

distinct

orderBy

chaining


These are the building blocks of every PySpark pipeline.
