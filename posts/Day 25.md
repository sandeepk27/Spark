---
title: 'Day 25: Streaming Aggregations in Spark'
cover_image: 'https://raw.githubusercontent.com/sandeepk27/Spark/main/cover-images/Day%2025.jpg'
published: true
description: Windows & Watermarking
tags: 'dataengineering, spark, bigdata, python'
linkedin_image: 'no'
devto_cover: 'yes'
id: 3126996
date: '2025-12-25T17:18:07Z'
---

Welcome to Day 25 of the Spark Mastery Series. Today we move from “reading streams” to real-time analytics.
This is where most streaming pipelines fail - not because of code, but because of state mismanagement.

Let’s fix that.


🌟 **Why Streaming Aggregations Are Hard**

Streaming data never ends.
If you aggregate without limits, Spark keeps data forever.

Result:
- Growing state
- Memory pressure
- Job crashes


🌟 **Event Time Is Mandatory**
Always use event time, not processing time.

Why?
- Processing time depends on delays
- Event time reflects real business time
Correct analytics depend on event time.


🌟 **Windows - Turning Infinite into Finite**

Windows slice infinite streams into manageable chunks.

Example:
- Sales every 10 minutes
- Clicks per hour
- Orders per day


🌟 **Watermarking — Cleaning Old State**

Watermark tells Spark:
'You can forget data older than X minutes.'

This:
- Bounds memory usage
- Allows append mode
- Handles late data safely


🌟 **Real-World Example**
E-commerce

- Window: 5 minutes
- Watermark: 10 minutes

Meaning:
- Accept data late by 10 minutes
- Drop anything older
This balances accuracy and performance.


🚀 **Summary**

We learned:
- Streaming aggregations
- Event time vs processing time
- Windowed analytics
- Tumbling & sliding windows
- Late data handling
- Watermarking
- Output modes


Follow for more such content. Let me know if I missed anything. Thank you
