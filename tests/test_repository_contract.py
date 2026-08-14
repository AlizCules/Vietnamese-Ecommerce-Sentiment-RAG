import csv
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RepositoryContractTests(unittest.TestCase):
    def test_summary_counts_and_labels(self):
        summary = json.loads((ROOT / "data" / "reports" / "data_summary.json").read_text(encoding="utf-8"))
        self.assertEqual(summary["sentiment_raw_rows"], 5971)
        self.assertEqual(summary["sentiment_after_dedup_rows"], 5162)
        self.assertEqual(summary["sentiment_removed_conflict_duplicates"], 46)
        self.assertEqual(summary["sentiment_3class_distribution"], {"positive": 2217, "negative": 2074, "neutral": 871})
        self.assertEqual(summary["rag_total_documents"], 82677)

    def test_model_metrics_schema_and_values(self):
        path = ROOT / "results" / "module2" / "metrics_summary.csv"
        with path.open(newline="", encoding="utf-8-sig") as handle:
            rows = list(csv.DictReader(handle))
        test_rows = {row["model_name"]: row for row in rows if row["split"] == "test"}
        self.assertAlmostEqual(float(test_rows["majority_class"]["macro_f1"]), 0.2003610108, places=8)
        self.assertAlmostEqual(float(test_rows["logistic_regression"]["macro_f1"]), 0.8940276252, places=8)
        self.assertAlmostEqual(float(test_rows["linear_svm"]["macro_f1"]), 0.9098090499, places=8)
        self.assertAlmostEqual(float(test_rows["linear_svm"]["accuracy"]), 0.9329032258, places=8)

    def test_retrieval_config_and_manual_eval(self):
        config = json.loads((ROOT / "models" / "module4" / "module4_index_config.json").read_text(encoding="utf-8"))
        self.assertEqual(config["embedding_dim"], 384)
        self.assertEqual(config["num_documents"], 82677)
        self.assertEqual(config["index_type"], "IndexFlatIP")
        with (ROOT / "results" / "module5" / "manual_precision_overall.csv").open(newline="", encoding="utf-8-sig") as handle:
            rows = {int(row["k"]): row for row in csv.DictReader(handle)}
        self.assertAlmostEqual(float(rows[5]["average_precision_at_k"]), 0.5066666667, places=8)
        self.assertEqual(int(rows[5]["num_queries"]), 15)

    def test_documentation_contract(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for relative in (
            "docs/data_sources.md",
            "docs/data_pipeline.md",
            "docs/review_analytics.md",
            "docs/sentiment_model.md",
            "docs/retrieval_system.md",
            "docs/retrieval_evaluation.md",
            "docs/hybrid_retrieval.md",
            "docs/web_demo.md",
        ):
            self.assertTrue((ROOT / relative).exists(), relative)
            self.assertIn(relative, readme)
        self.assertIn("rating-derived", readme)
        self.assertNotRegex(readme, re.compile(r"C:\\\\Users|PycharmProjects|AlizCuli", re.IGNORECASE))


if __name__ == "__main__":
    unittest.main()
