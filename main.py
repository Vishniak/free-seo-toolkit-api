import re
import json
import math
from collections import Counter
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from slugify import slugify
from bs4 import BeautifulSoup

# Initialize FastAPI App (v1.1.0)
app = FastAPI(
    title="SEO Matrix - All-in-One SEO & Schema API",
    description="Ultra-fast micro-services for JSON-LD Schema generation, LSI keywords, Helpful Content audits, URL slugifying, readability, and meta inspection.",
    version="1.1.0",
    servers=[
        {"url": "https://seotoolkitapi.vercel.app", "description": "Production Server (Vercel)"}
    ]
)

# Enable CORS for cross-origin access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------
# Stop-words helper dictionary (EN/RU/UK)
# ------------------------------------------------------------------
STOP_WORDS = {
    "a", "an", "the", "and", "or", "but", "is", "are", "in", "on", "at", "to", "for", "with", "by", "of",
    "в", "на", "и", "или", "но", "с", "по", "для", "из", "за", "от", "до", "как", "та", "що", "це"
}

# ------------------------------------------------------------------
# Request / Response Schemas
# ------------------------------------------------------------------

class SlugifyRequest(BaseModel):
    text: str = Field(..., example="10 Best AI & Python Tools for Translators in 2026!")
    language: Optional[str] = Field("en", example="en")
    remove_stopwords: Optional[bool] = Field(True, example=True)

class SlugifyResponse(BaseModel):
    original_text: str
    slug: str
    word_count: int

class KeywordRequest(BaseModel):
    text: str = Field(..., example="FastAPI is a modern, fast Web framework for Python. Python is great for AI.")
    top_n: Optional[int] = Field(5, example=5)

class KeywordItem(BaseModel):
    keyword: str
    count: int
    density_percent: float

class KeywordResponse(BaseModel):
    total_words: int
    top_keywords: List[KeywordItem]

class MetaInspectRequest(BaseModel):
    html_content: str = Field(..., example="<html><head><title>My Great Article Page</title><meta name='description' content='A short description here.'></head><body><h1>Main Title</h1></body></html>")

class MetaInspectResponse(BaseModel):
    title: Optional[str]
    title_length: int
    title_status: str
    description: Optional[str]
    description_length: int
    description_status: str
    h1_count: int
    has_canonical: bool
    has_og_image: bool

class ReadabilityRequest(BaseModel):
    text: str = Field(..., example="FastAPI is an asynchronous web framework built on top of Starlette and Pydantic.")

class ReadabilityResponse(BaseModel):
    word_count: int
    character_count: int
    estimated_reading_time_minutes: float
    reading_difficulty: str

class FAQItem(BaseModel):
    question: str = Field(..., example="What is FastAPI?")
    answer: str = Field(..., example="FastAPI is a high-performance Python web framework.")

class SchemaGenerateRequest(BaseModel):
    schema_type: str = Field(..., example="article", description="Supported types: 'article', 'product', 'faq'")
    title: str = Field(..., example="How to Build Ultra-Fast APIs with Python")
    description: Optional[str] = Field(None, example="Learn how to build production-ready APIs.")
    url: Optional[str] = Field(None, example="https://example.com/fastapi-guide")
    author_name: Optional[str] = Field("Editorial Team", example="John Doe")
    image_url: Optional[str] = Field(None, example="https://example.com/banner.jpg")
    price: Optional[float] = Field(None, example=29.99)
    currency: Optional[str] = Field("USD", example="USD")
    faq_items: Optional[List[FAQItem]] = Field(None)

class SchemaGenerateResponse(BaseModel):
    schema_type: str
    json_ld: str
    is_valid: bool

class NgramItem(BaseModel):
    phrase: str
    count: int

class LsiKeywordsRequest(BaseModel):
    text: str = Field(..., example="FastAPI is great for building high performance web APIs. High performance web applications use FastAPI.")
    min_words: Optional[int] = Field(2, ge=2, le=3, example=2)
    max_words: Optional[int] = Field(3, ge=2, le=4, example=3)
    top_n: Optional[int] = Field(10, ge=1, le=50, example=10)

class LsiKeywordsResponse(BaseModel):
    total_phrases_extracted: int
    top_ngrams: List[NgramItem]

class ContentAuditRequest(BaseModel):
    text_or_html: str = Field(..., example="<h1>Title</h1><p>First long paragraph about SEO optimization and best practices for developers.</p><p>Second paragraph providing actionable tips.</p>")

class ContentAuditResponse(BaseModel):
    word_count: int
    paragraph_count: int
    avg_words_per_sentence: float
    helpful_content_score: int
    thin_content_warning: bool
    recommendations: List[str]

class LinkItem(BaseModel):
    href: str
    anchor_text: str
    is_internal: bool
    is_nofollow: bool

class LinkCheckRequest(BaseModel):
    html_content: str = Field(..., example="<html><body><a href='/about'>About Us</a><a href='https://google.com' rel='nofollow'>Google</a></body></html>")
    base_domain: str = Field("example.com", example="example.com")

class LinkCheckResponse(BaseModel):
    total_links: int
    internal_links_count: int
    external_links_count: int
    nofollow_links_count: int
    links: List[LinkItem]

class RobotsGeneratorRequest(BaseModel):
    site_url: str = Field("https://example.com", example="https://example.com")
    disallow_paths: Optional[List[str]] = Field(["/admin/", "/private/"], example=["/admin/", "/private/"])
    allow_paths: Optional[List[str]] = Field(["/"], example=["/"])
    sitemap_url: Optional[str] = Field("https://example.com/sitemap.xml", example="https://example.com/sitemap.xml")
    user_agents: Optional[List[str]] = Field(["*"], example=["*"])

class RobotsGeneratorResponse(BaseModel):
    robots_txt: str
    rules_count: int


# ------------------------------------------------------------------
# Endpoints
# ------------------------------------------------------------------

@app.get("/")
def root():
    return {
        "status": "online",
        "service": "All-in-One SEO Toolkit API",
        "version": "1.1.0",
        "documentation": "/docs"
    }

@app.post("/v1/seo/slugify", response_model=SlugifyResponse)
def generate_slug(payload: SlugifyRequest):
    """
    Generate clean, SEO-friendly, stop-word-free URL slug.
    """
    raw_text = payload.text
    if not raw_text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
    
    clean_text = raw_text
    if payload.remove_stopwords:
        words = re.findall(r'\b[a-zA-Zа-яА-ЯіІїЇєЄ0-9]+\b', raw_text)
        filtered_words = [w for w in words if w.lower() not in STOP_WORDS]
        if filtered_words:
            clean_text = " ".join(filtered_words)
        else:
            clean_text = raw_text
            
    generated_slug = slugify(clean_text, lowercase=True)
    if not generated_slug:
        generated_slug = slugify(raw_text, lowercase=True) or "default-slug"
        
    words_total = len(re.findall(r'\b[a-zA-Zа-яА-ЯіІїЇєЄ0-9]+\b', raw_text))
    
    return SlugifyResponse(
        original_text=raw_text,
        slug=generated_slug,
        word_count=words_total
    )

@app.post("/v1/seo/extract-keywords", response_model=KeywordResponse)
def extract_keywords(payload: KeywordRequest):
    """
    Extract top keywords and calculate keyword density percentage.
    """
    if not payload.text.strip():
        return KeywordResponse(total_words=0, top_keywords=[])
        
    words = [w.lower() for w in re.findall(r'\b[a-zA-Zа-яА-ЯіІїЇєЄ0-9]+(?:-[a-zA-Zа-яА-ЯіІїЇєЄ0-9]+)*\b', payload.text) if len(w) > 2]
    filtered_words = [w for w in words if w not in STOP_WORDS]
    
    total_words_count = len(words)
    if total_words_count == 0:
        return KeywordResponse(total_words=0, top_keywords=[])
        
    counts = {}
    for word in filtered_words:
        counts[word] = counts.get(word, 0) + 1
        
    sorted_keywords = sorted(counts.items(), key=lambda item: item[1], reverse=True)[:payload.top_n]
    
    keyword_items = [
        KeywordItem(
            keyword=k,
            count=v,
            density_percent=round((v / total_words_count) * 100, 2)
        )
        for k, v in sorted_keywords
    ]
    
    return KeywordResponse(
        total_words=total_words_count,
        top_keywords=keyword_items
    )

@app.post("/v1/seo/meta-inspect", response_model=MetaInspectResponse)
def inspect_meta(payload: MetaInspectRequest):
    """
    Inspect HTML Meta Title, Meta Description, H1 tags, Canonical & OG tags.
    """
    content = payload.html_content.strip()
    if not content:
        raise HTTPException(status_code=400, detail="HTML content cannot be empty.")
        
    if len(content) > 500_000:
        content = content[:500_000]
        
    soup = BeautifulSoup(content, "html.parser")
    
    title_tag = soup.find("title")
    title_text = title_tag.get_text().strip() if title_tag else None
    title_len = len(title_text) if title_text else 0
    title_status = "optimal" if 50 <= title_len <= 60 else ("too_short" if title_len < 50 else "too_long")
    
    desc_tag = soup.find("meta", attrs={"name": re.compile(r"^description$", re.I)})
    desc_text = desc_tag["content"].strip() if desc_tag and desc_tag.has_attr("content") else None
    desc_len = len(desc_text) if desc_text else 0
    desc_status = "optimal" if 150 <= desc_len <= 160 else ("too_short" if desc_len < 150 else "too_long")
    
    h1_tags = soup.find_all("h1")
    canonical = soup.find("link", attrs={"rel": re.compile(r"^canonical$", re.I)}) is not None
    og_image = soup.find("meta", attrs={"property": re.compile(r"^og:image$", re.I)}) is not None
    
    return MetaInspectResponse(
        title=title_text,
        title_length=title_len,
        title_status=title_status,
        description=desc_text,
        description_length=desc_len,
        description_status=desc_status,
        h1_count=len(h1_tags),
        has_canonical=canonical,
        has_og_image=og_image
    )

@app.post("/v1/seo/readability", response_model=ReadabilityResponse)
def calculate_readability(payload: ReadabilityRequest):
    """
    Calculate Word Count, Character Count, Estimated Reading Time, and Difficulty Level.
    """
    text = payload.text.strip()
    if not text:
        return ReadabilityResponse(
            word_count=0,
            character_count=0,
            estimated_reading_time_minutes=0.0,
            reading_difficulty="Empty"
        )
        
    words = re.findall(r'\S+', text)
    word_cnt = len(words)
    char_cnt = len(text)
    
    reading_time = round(word_cnt / 200.0, 2)
    avg_word_len = char_cnt / word_cnt if word_cnt > 0 else 0
    difficulty = "Easy" if avg_word_len < 5 else ("Medium" if avg_word_len < 7 else "Hard / Technical")
    
    return ReadabilityResponse(
        word_count=word_cnt,
        character_count=char_cnt,
        estimated_reading_time_minutes=reading_time,
        reading_difficulty=difficulty
    )

@app.post("/v1/seo/schema-generate", response_model=SchemaGenerateResponse)
def generate_schema(payload: SchemaGenerateRequest):
    """
    Generate valid JSON-LD Structured Data (Schema.org) for Article, Product, or FAQ.
    """
    stype = payload.schema_type.lower().strip()
    
    if stype == "article":
        schema_dict = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": payload.title,
            "description": payload.description or "",
            "mainEntityOfPage": payload.url or "",
            "author": {
                "@type": "Person",
                "name": payload.author_name or "Editorial Team"
            }
        }
        if payload.image_url:
            schema_dict["image"] = payload.image_url
            
    elif stype == "product":
        schema_dict = {
            "@context": "https://schema.org",
            "@type": "Product",
            "name": payload.title,
            "description": payload.description or "",
        }
        if payload.image_url:
            schema_dict["image"] = payload.image_url
        if payload.price is not None:
            schema_dict["offers"] = {
                "@type": "Offer",
                "price": payload.price,
                "priceCurrency": payload.currency or "USD",
                "availability": "https://schema.org/InStock"
            }
            
    elif stype == "faq":
        faq_list = []
        if payload.faq_items:
            for item in payload.faq_items:
                faq_list.append({
                    "@type": "Question",
                    "name": item.question,
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": item.answer
                    }
                })
        schema_dict = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": faq_list
        }
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported schema_type: '{payload.schema_type}'. Use 'article', 'product', or 'faq'.")
        
    json_ld_str = json.dumps(schema_dict, indent=2, ensure_ascii=False)
    
    return SchemaGenerateResponse(
        schema_type=stype,
        json_ld=json_ld_str,
        is_valid=True
    )

@app.post("/v1/seo/lsi-keywords", response_model=LsiKeywordsResponse)
def extract_lsi_keywords(payload: LsiKeywordsRequest):
    """
    Extract N-gram phrases (2-word and 3-word co-occurrences) for LSI Keyword Analysis.
    """
    raw_text = payload.text.strip()
    if not raw_text:
        return LsiKeywordsResponse(total_phrases_extracted=0, top_ngrams=[])
        
    words = [w.lower() for w in re.findall(r'\b[a-zA-Zа-яА-ЯіІїЇєЄ0-9]+\b', raw_text)]
    if len(words) < payload.min_words:
        return LsiKeywordsResponse(total_phrases_extracted=0, top_ngrams=[])
        
    ngrams_list = []
    min_w = payload.min_words or 2
    max_w = payload.max_words or 3
    
    for n in range(min_w, max_w + 1):
        for i in range(len(words) - n + 1):
            slice_words = words[i:i+n]
            # Exclude if phrase is composed ENTIRELY of stop-words
            if not all(w in STOP_WORDS for w in slice_words):
                phrase = " ".join(slice_words)
                ngrams_list.append(phrase)
                
    counts = Counter(ngrams_list).most_common(payload.top_n)
    
    ngram_items = [NgramItem(phrase=phrase, count=cnt) for phrase, cnt in counts]
    
    return LsiKeywordsResponse(
        total_phrases_extracted=len(ngrams_list),
        top_ngrams=ngram_items
    )

@app.post("/v1/seo/content-audit", response_model=ContentAuditResponse)
def audit_content(payload: ContentAuditRequest):
    """
    Perform a heuristic Helpful Content audit (word count, paragraph structure, readability score).
    """
    raw = payload.text_or_html.strip()
    if not raw:
        return ContentAuditResponse(
            word_count=0,
            paragraph_count=0,
            avg_words_per_sentence=0.0,
            helpful_content_score=0,
            thin_content_warning=True,
            recommendations=["Text content cannot be empty."]
        )
        
    soup = BeautifulSoup(raw, "html.parser")
    plain_text = soup.get_text(separator=" ").strip()
    
    words = re.findall(r'\S+', plain_text)
    word_count = len(words)
    
    p_tags = soup.find_all("p")
    paragraph_count = len(p_tags) if p_tags else len([p for p in raw.split("\n\n") if p.strip()])
    if paragraph_count == 0 and word_count > 0:
        paragraph_count = 1
        
    sentences = [s.strip() for s in re.split(r'[.!?]+', plain_text) if s.strip()]
    sentence_count = len(sentences) or 1
    avg_words_per_sentence = round(word_count / sentence_count, 1)
    
    score = 100
    recommendations = []
    thin_warning = False
    
    if word_count < 300:
        score -= 30
        thin_warning = True
        recommendations.append("Word count is under 300 words. Expand content to avoid 'thin content' penalty.")
    elif word_count < 600:
        score -= 10
        recommendations.append("Consider adding more depth (target 800+ words for competitive SEO ranking).")
        
    if avg_words_per_sentence > 25:
        score -= 15
        recommendations.append("Sentences are too long on average (>25 words). Break them up to improve readability.")
        
    if paragraph_count < 2 and word_count > 150:
        score -= 15
        recommendations.append("Break content into multiple smaller paragraphs for better scannability.")
        
    h_tags = soup.find_all(re.compile(r"^h[1-6]$", re.I))
    if not h_tags and len(raw) > 500:
        score -= 10
        recommendations.append("Add subheadings (H2, H3) to structure your text logically.")
        
    if not recommendations:
        recommendations.append("Content structure is well-optimized!")
        
    final_score = max(0, min(100, score))
    
    return ContentAuditResponse(
        word_count=word_count,
        paragraph_count=paragraph_count,
        avg_words_per_sentence=avg_words_per_sentence,
        helpful_content_score=final_score,
        thin_content_warning=thin_warning,
        recommendations=recommendations
    )

@app.post("/v1/seo/link-check", response_model=LinkCheckResponse)
def check_links(payload: LinkCheckRequest):
    """
    Extract and classify internal vs external links, anchor text, and nofollow attributes from HTML.
    """
    html = payload.html_content.strip()
    if not html:
        return LinkCheckResponse(
            total_links=0,
            internal_links_count=0,
            external_links_count=0,
            nofollow_links_count=0,
            links=[]
        )
        
    soup = BeautifulSoup(html, "html.parser")
    a_tags = soup.find_all("a", href=True)
    
    base_dom = payload.base_domain.lower().replace("https://", "").replace("http://", "").strip("/")
    
    link_items = []
    internal_cnt = 0
    external_cnt = 0
    nofollow_cnt = 0
    
    for tag in a_tags:
        href = tag["href"].strip()
        anchor = tag.get_text().strip() or "[Image / Empty Anchor]"
        
        rel_attr = tag.get("rel", [])
        if isinstance(rel_attr, str):
            rel_attr = [rel_attr]
        is_nofollow = "nofollow" in [r.lower() for r in rel_attr]
        if is_nofollow:
            nofollow_cnt += 1
            
        href_lower = href.lower()
        if href.startswith("/") or href.startswith("#") or base_dom in href_lower:
            is_internal = True
            internal_cnt += 1
        else:
            is_internal = False
            external_cnt += 1
            
        link_items.append(
            LinkItem(
                href=href,
                anchor_text=anchor,
                is_internal=is_internal,
                is_nofollow=is_nofollow
            )
        )
        
    return LinkCheckResponse(
        total_links=len(link_items),
        internal_links_count=internal_cnt,
        external_links_count=external_cnt,
        nofollow_links_count=nofollow_cnt,
        links=link_items
    )

@app.post("/v1/seo/robots-generator", response_model=RobotsGeneratorResponse)
def generate_robots(payload: RobotsGeneratorRequest):
    """
    Generate clean robots.txt directives and Sitemap declaration.
    """
    lines = []
    uas = payload.user_agents or ["*"]
    for ua in uas:
        lines.append(f"User-agent: {ua}")
        
    if payload.allow_paths:
        for allow in payload.allow_paths:
            lines.append(f"Allow: {allow}")
            
    if payload.disallow_paths:
        for disallow in payload.disallow_paths:
            lines.append(f"Disallow: {disallow}")
            
    if payload.sitemap_url:
        lines.append(f"\nSitemap: {payload.sitemap_url}")
        
    robots_content = "\n".join(lines)
    rules_total = (len(payload.allow_paths or []) + len(payload.disallow_paths or []))
    
    return RobotsGeneratorResponse(
        robots_txt=robots_content,
        rules_count=rules_total
    )
