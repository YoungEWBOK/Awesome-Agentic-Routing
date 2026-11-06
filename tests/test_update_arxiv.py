import importlib.util
import unittest
from datetime import datetime, timezone
from pathlib import Path

spec = importlib.util.spec_from_file_location("updater", Path(__file__).resolve().parents[1] / "scripts/update_arxiv.py")
u = importlib.util.module_from_spec(spec)
spec.loader.exec_module(u)


def paper(identifier="2611.12345", version="v1"):
    return dict(arxiv_id=identifier, version=version, title="Budget-aware LLM routing for agents",
                authors=["Example Author"], published="2026-11-01T00:00:00Z",
                updated="2026-11-02T00:00:00Z" if version == "v1" else "2026-11-03T00:00:00Z",
                url="https://arxiv.org/abs/" + identifier,
                abstract="Select a language model at each step of an agent workflow.", journal_ref="", comment="")


class UpdateTests(unittest.TestCase):
    def test_biweekly_across_year_boundary(self):
        state = {"last_success": "2026-12-25T01:20:00+00:00"}
        self.assertFalse(u.due(datetime(2027, 1, 1, 1, 17, tzinfo=timezone.utc), state, 14))
        self.assertTrue(u.due(datetime(2027, 1, 8, 1, 17, tzinfo=timezone.utc), state, 14))

    def test_revision_updates_without_duplicate(self):
        old, _, _ = u.merge_candidates([], [paper()], [], "2026-11-02")
        result, added, revised = u.merge_candidates(old, [paper(version="v2")], [], "2026-11-04")
        self.assertEqual((len(result), added, revised), (1, 0, 1))
        self.assertEqual(result[0]["first_seen"], "2026-11-02")
        self.assertEqual(result[0]["version"], "v2")

    def test_older_record_cannot_overwrite_revision(self):
        old, _, _ = u.merge_candidates([], [paper(version="v2")], [], "2026-11-03")
        result, _, _ = u.merge_candidates(old, [paper()], [], "2026-11-04")
        self.assertEqual(result[0]["version"], "v2")

    def test_curated_excluded_by_title_or_id(self):
        curated = [{"arxiv_id": "9999.99999", "title": "Budget aware LLM routing for agents"}]
        self.assertEqual(u.merge_candidates([], [paper()], curated, "2026-11-04")[0], [])

    def test_unrelated_network_routing_excluded(self):
        p = paper()
        p.update(title="Routing in optical networks", abstract="Shortest paths for packets")
        self.assertIsNone(u.relevance(p))

    def test_internal_token_routing_excluded(self):
        p = paper()
        p.update(title="Visual Token Routing for LLM Agents", abstract="Token routing inside language models for agent tasks.")
        self.assertIsNone(u.relevance(p))

    def test_model_selection_without_agent_is_in_scope(self):
        p = paper()
        p.update(title="Cost-aware Model Selection", abstract="Choose between large language models to balance cost and quality.")
        self.assertEqual(u.relevance(p), "Model / LLM routing and cascading")

    def test_reclassified_candidate_removed(self):
        old, _, _ = u.merge_candidates([], [paper()], [], "2026-11-02")
        unrelated = paper(version="v2")
        unrelated.update(title="Visual Token Routing", abstract="Token routing in language models.")
        self.assertEqual(u.merge_candidates(old, [unrelated], [], "2026-11-04")[0], [])

    def test_feed_error_is_not_empty_success(self):
        with self.assertRaises(ValueError):
            u.parse_feed(b'<feed xmlns="http://www.w3.org/2005/Atom"><entry><id>http://arxiv.org/api/errors#bad</id></entry></feed>')

    def test_valid_atom_normalizes_version(self):
        raw = b'''<feed xmlns="http://www.w3.org/2005/Atom" xmlns:o="http://a9.com/-/spec/opensearch/1.1/"><o:totalResults>1</o:totalResults><entry><id>http://arxiv.org/abs/2611.12345v2</id><title>Example</title><published>2026-11-01T00:00:00Z</published><updated>2026-11-02T00:00:00Z</updated><author><name>A</name></author><summary>Example abstract</summary></entry></feed>'''
        total, rows = u.parse_feed(raw)
        self.assertEqual((total, rows[0]["arxiv_id"], rows[0]["version"]), (1, "2611.12345", "v2"))

    def test_missing_page_fails(self):
        class Client:
            def fetch(self, params):
                return 10, []
        with self.assertRaises(RuntimeError):
            u.search(Client(), "query", {"page_size": 100, "max_results": 2000})

    def test_result_cap_fails_instead_of_truncating(self):
        class Client:
            def fetch(self, params):
                return 2001, [paper()]
        with self.assertRaises(RuntimeError):
            u.search(Client(), "query", {"page_size": 100, "max_results": 2000})


if __name__ == "__main__":
    unittest.main()
