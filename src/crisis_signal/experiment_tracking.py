"""Optional MLflow integration without coupling the core trainer to MLflow."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any


def log_training_run(
    metadata: Mapping[str, Any],
    artifact_path: str | Path,
    experiment_name: str = "crisis-signal-ai",
    run_name: str | None = None,
) -> str:
    """Log an existing training artifact and metadata to MLflow.

    Returns the MLflow run ID. The function imports MLflow lazily so the core
    package remains lightweight.
    """
    try:
        import mlflow
    except ImportError as exc:
        raise RuntimeError(
            "Install MLOps dependencies: pip install -e '.[mlops]'"
        ) from exc

    mlflow.set_experiment(experiment_name)
    with mlflow.start_run(run_name=run_name) as run:
        simple_params = {
            key: value
            for key, value in metadata.items()
            if isinstance(value, (str, int, float, bool))
        }
        mlflow.log_params(simple_params)
        evaluation = metadata.get("evaluation", {})
        if isinstance(evaluation, Mapping):
            metrics = {
                key: float(value)
                for key, value in evaluation.items()
                if isinstance(value, (int, float)) and value is not None
            }
            mlflow.log_metrics(metrics)
        path = Path(artifact_path)
        mlflow.log_artifact(str(path), artifact_path="model")
        sidecar = path.with_suffix(path.suffix + ".metadata.json")
        if sidecar.exists():
            mlflow.log_artifact(str(sidecar), artifact_path="model")
        return run.info.run_id
