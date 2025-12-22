---
title: 'Day 19: Spark Broadcasting & Caching '
cover_image: https://raw.githubusercontent.com/sandeepk27/Spark/main/cover-images/Day%2019.jpg
published: true
description: How to Avoid OOM Errors and Speed Up ETL Jobs using spark
tags: 'dataengineering, spark, bigdata, python'
linkedin_image: 'no'
devto_cover: 'yes'
id: 3120052
date: '2025-12-22T08:06:01Z'
---

Welcome to Day 19 of the Spark Mastery Series.
Today we focus on memory, the most common reason Spark jobs fail in production.

`Most Spark failures are not logic bugs - they are memory mistakes.`

🌟 **Broadcasting — The Right Way to Join Small Tables**

Broadcast joins avoid shuffle and are extremely fast.
But misuse leads to executor crashes.

Golden rule:
-> Broadcast only when the table is small and stable.

Spark automatically decides broadcast sometimes, but explicit broadcast gives you control.

🌟 **Caching — Powerful but Dangerous**
Caching improves performance only when:
- The same DataFrame is reused
- Computation before cache is heavy

Bad caching causes:

- Executor OOM
- GC thrashing
- Cluster instability

Always ask:
-> Will this DataFrame be reused?

🌟 **Persist vs Cache — What to Use?**

- cache() → simple, MEMORY_ONLY
- persist(MEMORY_AND_DISK) → production-safe

Use persist() for ETL pipelines.

🌟 **Spark Memory Internals**
Spark prioritizes execution memory over cached data.

If Spark needs memory for shuffle:
- It evicts cached blocks
- Recomputes them later

This is why caching doesn’t guarantee data stays in memory forever.

🌟 **Real-World Example**
Bad practice

```
df1.cache()
df2.cache()
df3.cache()
```

Good practice
```
df_silver.persist(StorageLevel.MEMORY_AND_DISK)
df_silver.count()
# use df_silver multiple times
df_silver.unpersist()
```

🚀 **Summary**
We learned:
- How broadcast joins work internally
- When to use and avoid broadcast
- Cache vs persist
- Storage levels
- Spark memory model
- How to avoid OOM errors

Follow for more such content. Let me know if I missed anything. Thank you!!
