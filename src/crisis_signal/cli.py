"""Command-line interface."""

from __future__ import annotations

import json
from pathlib import Path

import typer

from crisis_signal.predictor import CrisisPredictor
from crisis_signal.training import train_baseline

app = typer.Typer(no_args_is_help=True, help="CrisisSignal AI command-line tools")


@app.command("train")
def train_command(
    data: Path = typer.Option(..., exists=True, readable=True),
    output: Path = typer.Option(Path("artifacts/baseline.joblib")),
    test_size: float = typer.Option(0.2, min=0.05, max=0.5),
    random_state: int = typer.Option(42),
    abstain_margin: float = typer.Option(0.1, min=0.0, max=0.49),
    min_df: int = typer.Option(2, min=1),
) -> None:
    metadata = train_baseline(
        data,
        output,
        test_size=test_size,
        random_state=random_state,
        abstain_margin=abstain_margin,
        min_df=min_df,
    )
    typer.echo(json.dumps(metadata, indent=2))


@app.command("predict")
def predict_command(
    text: str,
    model: Path = typer.Option(..., exists=True, readable=True),
    source_id: str | None = typer.Option(None),
) -> None:
    result = CrisisPredictor(model).predict(text, source_id=source_id)
    typer.echo(result.model_dump_json(indent=2))


@app.command("make-demo-data")
def make_demo_data_command(
    output: Path = typer.Option(Path("data/demo.csv")),
) -> None:
    from crisis_signal.demo import write_demo_data

    write_demo_data(output)
    typer.echo(f"wrote {output}")


if __name__ == "__main__":
    app()
