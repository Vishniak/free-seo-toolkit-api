import time
import requests

BASE_URL = "https://seotoolkitapi.vercel.app"

endpoints = [
    (f"{BASE_URL}/v1/seo/slugify", {"text": "How to Build a High Performance Python API in 2026!"}),
    (f"{BASE_URL}/v1/seo/extract-keywords", {"text": "FastAPI Vercel Python SEO Keyword Extractor Microservice API", "top_n": 5}),
    (f"{BASE_URL}/v1/seo/readability", {"text": "This is a clean, simple text payload to test the readability score endpoint of our API."})
]

print("[START] Starting API Warmup & Usage Generation...")

success_count = 0
for i in range(15):  # 15 iterations x 3 endpoints = 45 requests
    for url, body in endpoints:
        try:
            res = requests.post(url, json=body, timeout=5)
            if res.status_code == 200:
                success_count += 1
                print(f"[{success_count}/45] {url.split('/')[-1]} -> Status: 200 OK")
            else:
                print(f"Failed: {res.status_code}")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(0.3)

print(f"\n[DONE] Warmup Completed! Successfully generated {success_count} clean 200 OK requests.")
