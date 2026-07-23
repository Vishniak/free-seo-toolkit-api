import re
import math
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from slugify import slugify
from bs4 import BeautifulSoup

# Initialize FastAPI App
app = FastAPI(
    title="All-in-One SEO Toolkit API",
    description="Ultra-fast micro-services for SEO slugification, keyword extraction, meta inspection, and readability analysis.",
    version="1.0.0"
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
# Request / Response Schemas (Pydantic Models for strict validation)
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

# ------------------------------------------------------------------
# Stop-words helper dictionary (EN/RU/UK)
# ------------------------------------------------------------------
STOP_WORDS = {
    "a", "an", "the", "and", "or", "but", "is", "are", "in", "on", "at", "to", "for", "with", "by", "of",
    "в", "на", "и", "или", "но", "с", "по", "для", "из", "за", "от", "до", "как", "та", "що", "це"
}

# ------------------------------------------------------------------
# Endpoints
# ------------------------------------------------------------------

@app.get("/")
def root():
    return {
        "status": "online",
        "service": "All-in-One SEO Toolkit API",
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
            clean_text = raw_text  # Fallback to raw_text if all words were stop-words
            
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
    Extract top keywords and calculate keyword density percentage (supports hyphenated words e.g. e-commerce).
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
    Protects memory by capping HTML inspection at 500 KB.
    """
    content = payload.html_content.strip()
    if not content:
        raise HTTPException(status_code=400, detail="HTML content cannot be empty.")
        
    # Cap HTML size at 500 KB to protect serverless memory limits
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
    
    # Average reading speed: 200 words per minute
    reading_time = round(word_cnt / 200.0, 2)
    
    # Difficulty heuristic based on average word length
    avg_word_len = char_cnt / word_cnt if word_cnt > 0 else 0
    difficulty = "Easy" if avg_word_len < 5 else ("Medium" if avg_word_len < 7 else "Hard / Technical")
    
    return ReadabilityResponse(
        word_count=word_cnt,
        character_count=char_cnt,
        estimated_reading_time_minutes=reading_time,
        reading_difficulty=difficulty
    )
