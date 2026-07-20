from pathlib import Path

from crisis_signal.demo import write_demo_data
from crisis_signal.predictor import CrisisPredictor
from crisis_signal.training import train_baseline


def test_end_to_end_training_and_prediction(tmp_path: Path) -> None:
    data_path = tmp_path / "demo.csv"
    model_path = tmp_path / "model.joblib"
    write_demo_data(data_path)
    metadata = train_baseline(data_path, model_path, min_df=1)
    assert model_path.exists()
    assert metadata["evaluation"]["accuracy"] >= 0.0
    result = CrisisPredictor(model_path).predict("Earthquake damaged the hospital")
    assert 0.0 <= result.probability_disaster <= 1.0
