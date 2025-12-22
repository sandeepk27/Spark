---
title: 'Day 22: Spark Shuffle Deep Dive'
cover_image: 'https://raw.githubusercontent.com/sandeepk27/Spark/main/cover-images/Day%2022.jpg'
published: true
description: Why Your Jobs Are Slow And How to Fix Them
tags: 'dataengineering, spark, bigdata, python'
linkedin_image: 'no'
devto_cover: 'yes'
---

Welcome to Day 22 of the Spark Mastery Series.
Today we open the black box that most Spark developers fear — Shuffles.

If your Spark job is slow, unstable, or expensive, shuffle is the reason 90% of the time.

Let’s understand why.

🌟 **What Exactly Is a Shuffle?**
A shuffle happens when Spark must repartition data across executors based on a key.

This is required for:
- joins
- aggregations
- sorting
- ranking
But it comes at a huge cost.


🌟 **Why Shuffles Are Expensive**
During shuffle Spark:
- Writes intermediate data to disk
- Sends data over the network
- Sorts large datasets
- Creates new execution stages
This makes shuffle the slowest operation in Spark.


🌟 **Reading Shuffle in Explain Plan**

```
df.explain(True)
```

Look for:
- Exchange
- SortMergeJoin
- HashAggregate
These indicate shuffle boundaries.


🌟 **Shuffle in Spark UI**

Key metrics:
- Shuffle Read (bytes)
- Shuffle Write (bytes)
- Spill (memory/disk)
- Task skew (long tail tasks)

If you see:
- One task running much longer → skew
- High shuffle read/write → optimization needed

🌟 **Real Example**

Bad pipeline
```
df.join(df2, "id").groupBy("id").count()
```
Optimised

```
df2_small = broadcast(df2)
df.join(df2_small, "id").groupBy("id").count()
```

Result:
- Shuffle reduced
- Runtime improved drastically

🌟 **How Senior Engineers Think**
They ask:
- Is this shuffle necessary?
- Can I broadcast?
- Can I aggregate earlier?
- Can I reduce data before shuffle?


🚀 **Summary**
We learned:
- What shuffle is
- What causes shuffle
- Why shuffle is slow
- How to identify shuffle
- How skew affects shuffle
- How to think like a senior engineer

Follow for more such content. Let me know if I missed anything. Thank you!!
