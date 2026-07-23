import re
import unittest

STOP_WORDS = {
    "a", "an", "the", "and", "or", "but", "is", "are", "in", "on", "at", "to", "for", "with", "by", "of",
    "в", "на", "и", "или", "но", "с", "по", "для", "из", "за", "от", "до", "как", "та", "що", "це"
}

def pure_slugify_logic(raw_text: str, remove_stopwords: bool = True):
    if not raw_text.strip():
        return ""
    clean_text = raw_text
    if remove_stopwords:
        words = re.findall(r'\b[a-zA-Zа-яА-ЯіІїЇєЄ0-9]+\b', raw_text)
        filtered_words = [w for w in words if w.lower() not in STOP_WORDS]
        if filtered_words:
            clean_text = " ".join(filtered_words)
        else:
            clean_text = raw_text
    
    slug = re.sub(r'[^a-zA-Z0-9]+', '-', clean_text).strip('-').lower()
    return slug or "default-slug"

def pure_keyword_logic(text: str, top_n: int = 5):
    if not text.strip():
        return 0, []
    words = [w.lower() for w in re.findall(r'\b[a-zA-Zа-яА-ЯіІїЇєЄ0-9]+(?:-[a-zA-Zа-яА-ЯіІїЇєЄ0-9]+)*\b', text) if len(w) > 2]
    filtered_words = [w for w in words if w not in STOP_WORDS]
    total_count = len(words)
    if total_count == 0:
        return 0, []
    counts = {}
    for w in filtered_words:
        counts[w] = counts.get(w, 0) + 1
    sorted_items = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
    result = [(k, v, round((v/total_count)*100, 2)) for k, v in sorted_items]
    return total_count, result

def pure_readability_logic(text: str):
    text = text.strip()
    if not text:
        return 0, 0, 0.0, "Empty"
    words = re.findall(r'\S+', text)
    word_cnt = len(words)
    char_cnt = len(text)
    reading_time = round(word_cnt / 200.0, 2)
    avg_word_len = char_cnt / word_cnt if word_cnt > 0 else 0
    difficulty = "Easy" if avg_word_len < 5 else ("Medium" if avg_word_len < 7 else "Hard / Technical")
    return word_cnt, char_cnt, reading_time, difficulty

class TestPureLogic(unittest.TestCase):

    def test_slugify(self):
        slug = pure_slugify_logic("10 Best AI & Python Tools for Translators in 2026!")
        self.assertIn("python", slug)
        self.assertNotIn("for", slug)

    def test_slugify_fallback(self):
        slug = pure_slugify_logic("the for and in")
        self.assertTrue(len(slug) > 0)
        self.assertEqual(slug, "the-for-and-in")

    def test_keyword_hyphenated(self):
        total, keywords = pure_keyword_logic("FastAPI is e-commerce fast e-commerce framework.", top_n=3)
        self.assertGreater(total, 0)
        self.assertEqual(keywords[0][0], "e-commerce")

    def test_readability_math(self):
        words, chars, time_min, diff = pure_readability_logic("FastAPI is an asynchronous web framework.")
        self.assertEqual(words, 6)
        self.assertGreater(time_min, 0.0)
        self.assertTrue(diff in ["Easy", "Medium", "Hard / Technical"])

if __name__ == "__main__":
    unittest.main()
