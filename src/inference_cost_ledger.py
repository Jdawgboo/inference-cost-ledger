"""Aggregate normalized model-usage records using owner-supplied pricing."""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence


@dataclass(frozen=True)
class ModelTotal:
    requests: int
    input_tokens: int
    output_tokens: int
    cost_usd: float


def summarize(records: Sequence[Mapping[str, Any]], pricing: Mapping[str, Mapping[str, float]]) -> dict[str, ModelTotal]:
    totals: dict[str, dict[str, float]] = defaultdict(lambda: {"requests": 0, "input_tokens": 0, "output_tokens": 0, "cost_usd": 0.0})
    for record in records:
        model = str(record["model"])
        if model not in pricing:
            raise ValueError(f"missing pricing for model: {model}")
        input_tokens, output_tokens = int(record.get("input_tokens", 0)), int(record.get("output_tokens", 0))
        rates = pricing[model]
        cost = input_tokens * float(rates["input_per_million"]) / 1_000_000 + output_tokens * float(rates["output_per_million"]) / 1_000_000
        total = totals[model]
        total["requests"] += 1
        total["input_tokens"] += input_tokens
        total["output_tokens"] += output_tokens
        total["cost_usd"] += cost
    return {model: ModelTotal(int(value["requests"]), int(value["input_tokens"]), int(value["output_tokens"]), round(value["cost_usd"], 8)) for model, value in totals.items()}


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate local model usage costs")
    parser.add_argument("records", type=Path)
    parser.add_argument("pricing", type=Path)
    args = parser.parse_args()
    result = summarize(json.loads(args.records.read_text()), json.loads(args.pricing.read_text()))
    print(json.dumps({model: total.__dict__ for model, total in result.items()}, indent=2))


if __name__ == "__main__":
    main()
