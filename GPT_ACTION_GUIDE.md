# 🤖 Custom GPT & AI Agent Integration Guide for SEO Matrix API

Integrate **SEO Matrix API** into your Custom GPTs, Claude Projects, LangChain agents, or AutoGPT workflows in under 2 minutes.

---

## ⚡ Quick Setup for OpenAI Custom GPTs

1. Go to [ChatGPT Custom GPT Builder](https://chatgpt.com/gpts/editor).
2. Scroll down to **Actions** and click **Create new action**.
3. In the **Schema** box, choose **Import from URL** or paste the raw contents of:
   ```text
   https://raw.githubusercontent.com/Vishniak/free-seo-toolkit-api/main/openapi.json
   ```
4. Under **Authentication**:
   - **Authentication Type:** API Key
   - **Auth Type:** Custom
   - **Header Name:** `X-RapidAPI-Key` (if routing via RapidAPI) or leave unauthenticated for direct Vercel free usage.
   - **API Key:** Insert your RapidAPI key.

---

## 🚀 Available AI Tools (Actions)

| Endpoint | Action Summary | Use Case for AI |
| :--- | :--- | :--- |
| `POST /v1/seo/schema-generate` | Generate JSON-LD Schema | Generate 100% valid Article, Product, or FAQ Schema.org JSON without hallucinations. |
| `POST /v1/seo/lsi-keywords` | Extract LSI N-grams | Calculate 2-word & 3-word co-occurrence phrase frequencies for TF-IDF content optimization. |
| `POST /v1/seo/content-audit` | Helpful Content Audit | Perform Google Helpful Content heuristic scoring, paragraph distribution & thin-content checks. |
| `POST /v1/seo/extract-keywords` | Extract Top Keywords | Calculate word frequency and keyword density percentages. |
| `POST /v1/seo/meta-inspect` | Inspect HTML Meta Tags | Analyze Title length, Meta Description, H1 count, Canonical, and OG tags. |
| `POST /v1/seo/readability` | Readability & Reading Time | Compute Flesch readability, word count, character count, and estimated reading time. |
| `POST /v1/seo/link-check` | Audit Links | Extract internal vs external links, anchor texts, and nofollow flags. |
| `POST /v1/seo/slugify` | Generate URL Slug | Clean stop-words and convert titles into SEO-friendly URL slugs. |
| `POST /v1/seo/robots-generator` | Generate robots.txt | Create clean robots.txt rules and Sitemap declarations. |

---

## 💡 Example Prompt for Custom GPT Instructions

Copy & paste this snippet into your Custom GPT **Instructions**:

```text
You are an expert SEO Content Strategist. You have access to the SEO Matrix API.
- Whenever generating schema, ALWAYS call `POST /v1/seo/schema-generate` to return verified JSON-LD.
- Whenever analyzing article drafts, call `POST /v1/seo/content-audit` and `POST /v1/seo/lsi-keywords` to provide TF-IDF density recommendations.
- Keep responses structured, actionable, and data-driven.
```
