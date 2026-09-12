import unittest

from inference_cost_ledger import summarize


class LedgerTests(unittest.TestCase):
    def test_aggregates_per_model_costs(self) -> None:
        result = summarize([{"model": "m1", "input_tokens": 1000, "output_tokens": 2000}, {"model": "m1", "input_tokens": 1000, "output_tokens": 0}], {"m1": {"input_per_million": 1.0, "output_per_million": 2.0}})
        self.assertEqual(result["m1"].requests, 2)
        self.assertEqual(result["m1"].cost_usd, 0.006)

    def test_rejects_unpriced_models(self) -> None:
        with self.assertRaises(ValueError):
            summarize([{"model": "missing"}], {})


if __name__ == "__main__":
    unittest.main()
