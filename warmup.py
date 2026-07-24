import time
import requests

BASE_URL = "https://seotoolkitapi.vercel.app"

endpoints = [
    (f"{BASE_URL}/v1/seo/slugify", {"text": "How to Build a High Performance Python API in 2026!"}),
    (f"{BASE_URL}/v1/seo/extract-keywords", {"text": "FastAPI Vercel Python SEO Keyword Extractor Microservice API", "top_n": 5}),
    (f"{BASE_URL}/v1/seo/readability", {"text": "This is a clean, simple text payload to test the readability score endpoint of our API."}),
    (f"{BASE_URL}/v1/seo/schema-generate", {"schema_type": "article", "title": "Automated Schema Generator", "description": "Testing live JSON-LD schema generation"}),
    (f"{BASE_URL}/v1/seo/lsi-keywords", {"text": "High performance web APIs are built with FastAPI. High performance web applications use Python."}),
    (f"{BASE_URL}/v1/seo/content-audit", {"text_or_html": "<h1>Live Test</h1><p>First paragraph for helpful content audit.</p><p>Second paragraph testing live score.</p>"}),
    (f"{BASE_URL}/v1/seo/link-check", {"html_content": "<html><body><a href='/about'>About Us</a><a href='https://google.com' rel='nofollow'>Google</a></body></html>", "base_domain": "example.com"}),
    (f"{BASE_URL}/v1/seo/robots-generator", {"site_url": "https://example.com", "disallow_paths": ["/admin/"]}),
    (f"{BASE_URL}/v1/seo/meta-inspect", {"html_content": "<html><head><title>Meta Title Test</title></head><body><h1>H1</h1></body></html>"})
]

print("[START] Starting Live Vercel Production Warmup for All 9 Endpoints...")

success_count = 0
total_calls = len(endpoints) * 5  # 9 endpoints x 5 iterations = 45 requests

for i in range(5):
    for url, body in endpoints:
        try:
            res = requests.post(url, json=body, timeout=8)
            if res.status_code == 200:
                success_count += 1
                print(f"[{success_count}/{total_calls}] {url.split('/')[-1]} -> Status: 200 OK (Latency: {res.elapsed.microseconds / 1000:.1f}ms)")
            else:
                print(f"Failed: {url} -> {res.status_code}")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(0.2)

print(f"\n[DONE] Warmup Completed! Successfully generated {success_count}/{total_calls} clean 200 OK requests on live Vercel Production.")
