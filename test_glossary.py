import unittest

from glossary import ENTRIES, browse, categories, format_entry, get, related_entries, search


class SearchTests(unittest.TestCase):
    def test_empty_search_returns_alphabetical_entries(self) -> None:
        results = search()
        self.assertEqual(len(results), len(ENTRIES))
        self.assertEqual([entry.term for entry in results], sorted(entry.term for entry in ENTRIES))

    def test_term_match_ranks_above_definition_match(self) -> None:
        results = search("model")
        self.assertEqual(results[0].term, "Model")

    def test_search_matches_meaning(self) -> None:
        self.assertIn("Embedding", [entry.term for entry in search("numeric vector")])

    def test_multiple_words_must_all_match(self) -> None:
        results = search("model noise")
        self.assertEqual([entry.term for entry in results], ["Diffusion Model"])

    def test_category_filter(self) -> None:
        results = search(category="Security")
        self.assertTrue(results)
        self.assertTrue(all(entry.category == "Security" for entry in results))

    def test_categories_are_unique_and_sorted(self) -> None:
        values = categories()
        self.assertEqual(values[0], "All")
        self.assertEqual(values[1:], tuple(sorted(set(values[1:]))))

    def test_alias_search_and_lookup(self) -> None:
        self.assertEqual(search("VLM")[0].term, "Vision-Language Model")
        self.assertEqual(get("Model Context Protocol").term, "MCP")

    def test_related_entries_resolve_known_terms(self) -> None:
        grounding = get("Grounding")
        self.assertIsNotNone(grounding)
        self.assertIn(get("RAG"), related_entries(grounding))

    def test_format_includes_why_it_matters(self) -> None:
        formatted = format_entry(get("MCP"))
        self.assertIn("Why it matters:", formatted)

    def test_browse_allows_zero_results(self) -> None:
        self.assertEqual(list(browse(limit=0)), [])

    def test_terms_are_unique(self) -> None:
        terms = [entry.term for entry in ENTRIES]
        self.assertEqual(len(terms), len(set(terms)))


if __name__ == "__main__":
    unittest.main()