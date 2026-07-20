# Deployment

## Local API

```bash
crisis-signal train --data data/train.csv --output artifacts/baseline.joblib
export CRISIS_SIGNAL_MODEL=artifacts/baseline.joblib
uvicorn crisis_signal.api:app --host 0.0.0.0 --port 8000
```

## Docker

```bash
docker compose up --build
```

The container expects a read-only model artifact mounted at `/app/artifacts/baseline.joblib`.

## Production controls still required

- authenticated access and rate limiting;
- encrypted transport and secret management;
- immutable model and data version identifiers;
- audit logging with privacy controls;
- rollback and incident-response procedures;
- load, latency and failure-injection testing;
- domain-expert approval before high-impact use.
