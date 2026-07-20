# Architecture

```mermaid
flowchart TD
    S[Archived or licensed stream] --> V[Schema validation]
    V --> N[Unicode and social-text normalization]
    N --> D[Duplicate-aware grouping]
    D --> M[Model family]
    M --> P[Probability]
    P --> C[Calibration and abstention]
    C --> O[Prediction or human review]
    O --> A[API, batch reports, dashboard]
    A --> R[Audit metadata and drift monitoring]
```

## Boundaries

The package separates model code from data acquisition, API serving and user interfaces. Optional heavy dependencies are isolated. The default installation remains lightweight and testable on a CPU.

## Artifact contract

A serialized artifact contains:

```python
{"pipeline": fitted_sklearn_pipeline, "metadata": reproducibility_metadata}
```

Metadata includes the dataset fingerprint, split parameters, software versions and risk-aware evaluation report.
