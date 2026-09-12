# Inference Cost Ledger

An offline ledger for normalized model-usage records. It aggregates requests, tokens, and estimated cost by model using pricing that **you** supply.

## Usage

```bash
python -m unittest discover -s tests -v
python -m pip install .
inference-cost-ledger records.json pricing.json
```

Pricing format:

```json
{"model-a":{"input_per_million":1.0,"output_per_million":2.0}}
```

The output is only as current as the supplied pricing. This project does not retrieve provider prices, billing records, or hidden-token usage.

## License

MIT.
