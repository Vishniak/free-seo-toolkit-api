import unittest
import sys
import os

# Import main functions directly
from main import app, generate_slug, extract_keywords, inspect_meta, calculate_readability
from main import SlugifyRequest, KeywordRequest, MetaInspectRequest, ReadabilityRequest

class TestStandaloneSEOToolkit(unittest.TestCase):

    def test_slugify(self):
        req = SlugifyRequest(text="10 Best AI & Python Tools for Translators in 2026!", language="en", remove_stopwords=True)
        res = generate_slug(req)
        self.assertIn("python", res.slug)
        self.assertNotIn("for", res.slug)

    def test_slugify_stopwords_fallback(self):
        req = SlugifyRequest(text="the for and in", remove_stopwords=True)
        res = generate_slug(req)
        self.assertTrue(len(res.slug) > 0)

    def test_keyword_extraction(self):
        req = KeywordRequest(text="FastAPI is a fast web framework. Python FastAPI is great. FastAPI e-commerce.", top_n=3)
        res = extract_keywords(req)
        self.assertGreater(res.total_words, 0)
        self.assertEqual(res.top_keywords[0].keyword, "fastapi")

    def test_meta_inspect(self):
        html = """
        <html>
        <head>
            <title>Optimal Length Title Example for Testing SEO Meta Analyzer</title>
            <meta name="description" content="This is an optimal description text that reaches the recommended character limit for search engines to display properly in search snippets worldwide.">
            <link rel="canonical" href="https://example.com/test" />
            <meta property="og:image" content="https://example.com/image.jpg" />
        </head>
        <body>
            <h1>Main Page Title</h1>
        </body>
        </html>
        """
        req = MetaInspectRequest(html_content=html)
        res = inspect_meta(req)
        self.assertEqual(res.title_status, "optimal")
        self.assertEqual(res.description_status, "optimal")
        self.assertEqual(res.h1_count, 1)
        self.assertTrue(res.has_canonical)
        self.assertTrue(res.has_og_image)

    def test_readability(self):
        req = ReadabilityRequest(text="FastAPI is an asynchronous web framework built on top of Starlette and Pydantic.")
        res = calculate_readability(req)
        self.assertGreater(res.word_count, 0)
        self.assertGreater(res.estimated_reading_time_minutes, 0.0)

if __name__ == "__main__":
    unittest.main()
