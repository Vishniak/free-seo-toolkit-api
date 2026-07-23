import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestSEOToolkitAPI(unittest.TestCase):

    # ------------------------------------------------------------------
    # Test 1: Slugify Endpoint
    # ------------------------------------------------------------------
    def test_slugify_english(self):
        response = client.post("/v1/seo/slugify", json={
            "text": "10 Best AI & Python Tools for Translators in 2026!",
            "language": "en",
            "remove_stopwords": True
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue("slug" in data)
        self.assertNotIn("for", data["slug"])  # Stop word 'for' removed
        self.assertIn("python", data["slug"])

    def test_slugify_cyrillic(self):
        response = client.post("/v1/seo/slugify", json={
            "text": "10 Кращих Інструментів для Перекладача в 2026 році!",
            "language": "uk",
            "remove_stopwords": True
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(len(data["slug"]) > 0)
        self.assertIn("instrum", data["slug"])  # Transliterated

    def test_slugify_only_stopwords(self):
        # Edge case: text contains only stop words
        response = client.post("/v1/seo/slugify", json={
            "text": "the for and in",
            "remove_stopwords": True
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(len(data["slug"]) > 0)  # Fallback handles empty string

    # ------------------------------------------------------------------
    # Test 2: Keyword Extraction Endpoint
    # ------------------------------------------------------------------
    def test_extract_keywords(self):
        text = "FastAPI is a fast web framework. Python FastAPI is great for AI developers. FastAPI is fast."
        response = client.post("/v1/seo/extract-keywords", json={
            "text": text,
            "top_n": 3
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertGreater(data["total_words"], 0)
        top_keyword = data["top_keywords"][0]["keyword"]
        self.assertEqual(top_keyword.lower(), "fastapi")

    # ------------------------------------------------------------------
    # Test 3: Meta Inspection Endpoint
    # ------------------------------------------------------------------
    def test_inspect_meta_valid(self):
        # Exactly 155 characters description (optimal range: 150-160)
        desc = "This is an optimal description text that reaches the recommended character limit for search engines to display properly in search snippets worldwide today."
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Optimal Length Title Example for Testing SEO Meta Analyzer</title>
            <meta name="description" content="{desc}">
            <link rel="canonical" href="https://example.com/test" />
            <meta property="og:image" content="https://example.com/image.jpg" />
        </head>
        <body>
            <h1>Main Page Title</h1>
        </body>
        </html>
        """
        response = client.post("/v1/seo/meta-inspect", json={"html_content": html})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["description_status"], "optimal")
        self.assertEqual(data["h1_count"], 1)
        self.assertTrue(data["has_canonical"])
        self.assertTrue(data["has_og_image"])

    # ------------------------------------------------------------------
    # Test 4: Readability Endpoint
    # ------------------------------------------------------------------
    def test_readability(self):
        text = "FastAPI is an asynchronous web framework built on top of Starlette and Pydantic."
        response = client.post("/v1/seo/readability", json={"text": text})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertGreater(data["word_count"], 0)
        self.assertGreater(data["character_count"], 0)
        self.assertTrue("reading_difficulty" in data)

if __name__ == "__main__":
    unittest.main()
