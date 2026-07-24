from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_all_endpoints():
    print("--- TESTING ALL 9 ENDPOINTS ---")
    
    # 1. Root
    r = client.get("/")
    assert r.status_code == 200
    print("1. GET / -> OK", r.json()["service"])
    
    # 2. Slugify
    r = client.post("/v1/seo/slugify", json={"text": "Best AI & Python Tools 2026!"})
    assert r.status_code == 200
    assert "best-ai-python-tools-2026" in r.json()["slug"]
    print("2. POST /v1/seo/slugify -> OK", r.json()["slug"])
    
    # 3. Extract Keywords
    r = client.post("/v1/seo/extract-keywords", json={"text": "FastAPI is fast. Python FastAPI makes APIs fast."})
    assert r.status_code == 200
    print("3. POST /v1/seo/extract-keywords -> OK", [k["keyword"] for k in r.json()["top_keywords"]])
    
    # 4. Meta Inspect
    r = client.post("/v1/seo/meta-inspect", json={"html_content": "<html><head><title>Test Title</title></head><body><h1>H1 Title</h1></body></html>"})
    assert r.status_code == 200
    assert r.json()["h1_count"] == 1
    print("4. POST /v1/seo/meta-inspect -> OK", r.json()["title"])
    
    # 5. Readability
    r = client.post("/v1/seo/readability", json={"text": "FastAPI is an asynchronous web framework built on top of Starlette and Pydantic."})
    assert r.status_code == 200
    print("5. POST /v1/seo/readability -> OK", r.json()["reading_difficulty"])
    
    # 6. Schema Generate (NEW)
    r = client.post("/v1/seo/schema-generate", json={
        "schema_type": "article",
        "title": "Python SEO Automation",
        "description": "Learn how to automate SEO with FastAPI.",
        "author_name": "Antigravity Team"
    })
    assert r.status_code == 200
    assert "Article" in r.json()["json_ld"]
    print("6. POST /v1/seo/schema-generate -> OK", r.json()["schema_type"])
    
    # 7. LSI Keywords (NEW)
    r = client.post("/v1/seo/lsi-keywords", json={
        "text": "High performance web APIs are built with FastAPI. High performance web applications use Python."
    })
    assert r.status_code == 200
    print("7. POST /v1/seo/lsi-keywords -> OK", len(r.json()["top_ngrams"]), "phrases extracted")
    
    # 8. Content Audit (NEW)
    r = client.post("/v1/seo/content-audit", json={
        "text_or_html": "<h1>Great Guide</h1><p>First paragraph with enough words to test content structure.</p><p>Second paragraph with more helpful content for SEO optimization.</p>"
    })
    assert r.status_code == 200
    print("8. POST /v1/seo/content-audit -> OK Score:", r.json()["helpful_content_score"])
    
    # 9. Link Check (NEW)
    r = client.post("/v1/seo/link-check", json={
        "html_content": "<html><body><a href='/about'>About</a><a href='https://google.com' rel='nofollow'>Google</a></body></html>",
        "base_domain": "example.com"
    })
    assert r.status_code == 200
    assert r.json()["internal_links_count"] == 1
    assert r.json()["external_links_count"] == 1
    print("9. POST /v1/seo/link-check -> OK", r.json()["total_links"], "total links")
    
    # 10. Robots Generator (NEW)
    r = client.post("/v1/seo/robots-generator", json={
        "site_url": "https://mywebsite.com",
        "disallow_paths": ["/admin/", "/private/"],
        "sitemap_url": "https://mywebsite.com/sitemap.xml"
    })
    assert r.status_code == 200
    assert "Disallow: /admin/" in r.json()["robots_txt"]
    print("10. POST /v1/seo/robots-generator -> OK")

if __name__ == "__main__":
    test_all_endpoints()
