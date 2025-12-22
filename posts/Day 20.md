---
title: 'Day 20: Handling Bad Records & Data Quality in Spark'
cover_image: 'https://raw.githubusercontent.com/sandeepk27/Spark/main/cover-images/Day%2020.jpg'
published: true
description: Building Production-Grade Pipelines
tags: 'dataengineering, spark, bigdata, python'
linkedin_image: 'no'
devto_cover: 'yes'
id: 3120279
date: '2025-12-22T09:44:56Z'
---

Welcome to Day 20 of the Spark Mastery Series. Today we address a harsh truth:
`Real data is messy, incomplete, and unreliable.`

If your Spark pipeline can’t handle bad data, it will fail in production. Let’s build pipelines that survive reality.

🌟 **Why Data Quality Matters**
Bad data leads to:
- Wrong dashboards
- Broken ML models
- Financial losses
- Loss of trust
Data engineers are responsible for trustworthy data.


🌟 **Enforce Schema Early**
Always define schema explicitly.

**Benefits**:
- Faster ingestion
- Early error detection
- Consistent downstream processing

Never rely on inferSchema in production.


🌟 **Capture Bad Records, Don’t Drop Them**

Using badRecordsPath ensures:
- Pipeline continues
- Bad data is quarantined
- Audits are possible
This is mandatory in regulated industries.


🌟 **Apply Business Rules in Silver Layer**

Silver layer is where data becomes trusted.

Examples:
- Remove negative amounts
- Validate country codes
- Drop incomplete records
- Deduplicate
Never mix business rules in Bronze.

🌟 **Observability & Metrics**
Track record counts for every job.

Example:
```
Input: 1,000,000
Valid: 995,000
Invalid: 5,000
```
If invalid spikes → alert immediately.


🌟 **Delta Lake Safety Net**
With Delta:
- Rollback bad writes
- Reprocess safely
- Audit changes
This is why Delta is production-critical.


🚀 **Summary**
We learned:
- What bad records are
- How to enforce schema
- How to capture corrupt data
- How to apply data quality rules
- How to track metrics
- How Delta helps recovery

Follow for more such content. Let me know if I missed anything. Thank you
