# 🚀 All-in-One SEO & Web Micro-Services API (v1.1.0)

A fast, serverless Python FastAPI micro-service suite for SEO automation, JSON-LD Schema generation, LSI keyword extraction, content auditing, and web parsing. Hosted on Vercel Serverless Edge Infrastructure.

[![RapidAPI](https://img.shields.io/badge/RapidAPI-Subscribe%20Now-blue?style=for-the-badge&logo=rapid)](https://rapidapi.com/feanor547/api/all-in-one-seo-toolkit-api)
[![Status](https://img.shields.io/badge/Status-Live%20%26%20Operational-brightgreen?style=for-the-badge)]()
[![Python](https://img.shields.io/badge/FastAPI-v1.1.0-3776AB?style=for-the-badge&logo=python)]()

---

## ⚡ Features & 9 Endpoints

### 🟢 Basic Utilities
1. **`POST /v1/seo/slugify`** — Convert titles into clean, SEO-friendly, stop-word-free URL slugs.
2. **`POST /v1/seo/extract-keywords`** — Extract top keywords and keyword density percentage.
3. **`POST /v1/seo/readability`** — Calculate word count, reading time, and difficulty level.
4. **`POST /v1/seo/robots-generator`** — Generate clean `robots.txt` directives and Sitemap declarations.

### 🔵 Advanced SEO Tools
5. **`POST /v1/seo/schema-generate`** — Generate valid JSON-LD Structured Data (Article, Product, FAQ).
6. **`POST /v1/seo/lsi-keywords`** — Extract 2-word and 3-word N-gram co-occurrences for LSI keyword analysis.
7. **`POST /v1/seo/content-audit`** — Perform a heuristic Google Helpful Content audit (score 0-100 & recommendations).
8. **`POST /v1/seo/link-check`** — Extract internal vs external links, anchor text, and nofollow attributes.
9. **`POST /v1/seo/meta-inspect`** — Inspect HTML Meta Title, Meta Description, H1 tags, Canonical, and OG tags.

---

## 💳 Pricing Tiers (RapidAPI Marketplace)

| Plan | Price | Monthly Quota | Features |
| :--- | :--- | :--- | :--- |
| **BASIC** | **$0.00** | 25 requests / mo | Access to 4 Basic Endpoints |
| **PRO** | **$7.00** | 1,500 requests / mo | Access to 4 Basic Endpoints |
| **ULTRA** | **$25.00** | 5,000 requests / mo | **ALL 9 Endpoints** (Including Schema, LSI & Content Audit) |
| **MEGA** | **$90.00** | 150,000 requests / mo | **ALL 9 Endpoints** + High-Volume Agency & AI Agent Access |

---

## 🛠️ Quick Start (Python Example)

```python
import requests

url = "https://seotoolkitapi.vercel.app/v1/seo/schema-generate"

payload = {
    "schema_type": "article",
    "title": "How to Build a High Performance Python API in 2026!",
    "description": "A comprehensive guide for developers.",
    "author_name": "John Doe"
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

---

## 📜 Specification & License
- OpenAPI 3.0 Spec: [openapi.json](./openapi.json)
- License: MIT License. Free to use for personal & commercial projects via RapidAPI.
