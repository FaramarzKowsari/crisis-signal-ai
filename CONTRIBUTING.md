# Contributing

Thank you for helping improve CrisisSignal AI.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,api]"
pre-commit install
pytest
```

## Contribution standards

- Open an issue before substantial architectural changes.
- Do not commit private, scraped or license-restricted crisis data.
- Add tests for new behavior and document assumptions.
- Distinguish reproduced measurements from copied or historical metrics.
- Avoid claims of operational readiness without external validation.
- Use synthetic or properly licensed examples in tests.

## Pull requests

A pull request should explain the problem, method, evidence, risks and documentation changes. Model changes must include a comparison report and error analysis, not only a headline metric.
