# 🚀 Free All-in-One SEO & Web Parsing Toolkit API

A fast, serverless Python REST API for SEO automation, text analysis, and web scraping metadata extraction. Hosted on Vercel Serverless Edge Infrastructure.

[![RapidAPI](https://img.shields.io/badge/RapidAPI-Subscribe%20Free-blue?style=for-the-badge&logo=rapid)](https://rapidapi.com/feanor547/api/all-in-one-seo-toolkit-api)
[![Status](https://img.shields.io/badge/Status-Live%20%26%20Operational-brightgreen?style=for-the-badge)]()

---

## ⚡ Features & Endpoints

1. **`POST /v1/seo/slugify`** — Convert string titles into clean, SEO-friendly URL slugs.
2. **`POST /v1/seo/extract-keywords`** — Extract top N most relevant keywords with frequency & score.
3. **`POST /v1/seo/parse-meta`** — Scrape title, meta description, OG tags, canonical URLs, and headers.
4. **`POST /v1/seo/readability`** — Calculate Flesch Reading Ease score & word stats.

---

## 🛠️ Quick Start (Python Example)

```python
import requests

url = "https://all-in-one-seo-toolkit-api.p.rapidapi.com/v1/seo/slugify"

payload = { "text": "How to Build a High Performance Python API in 2026!" }
headers = {
    "x-rapidapi-key": "YOUR_RAPIDAPI_KEY",
    "x-rapidapi-host": "all-in-one-seo-toolkit-api.p.rapidapi.com",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

## 📜 License
MIT License. Free to use for personal & commercial projects via RapidAPI.
