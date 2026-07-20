"""Streamlit demonstration dashboard."""

from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
import streamlit as st

from crisis_signal.predictor import CrisisPredictor

st.set_page_config(page_title="CrisisSignal AI", page_icon="⚠️", layout="wide")
st.title("CrisisSignal AI")
st.caption("Research demonstration — not an emergency dispatch system")

model_path = Path(os.getenv("CRISIS_SIGNAL_MODEL", "artifacts/baseline.joblib"))
if not model_path.exists():
    st.error("Model artifact not found. Train the baseline first.")
    st.stop()

predictor = CrisisPredictor(model_path)
text = st.text_area("Message", height=140)
if st.button("Analyze", type="primary") and text.strip():
    result = predictor.predict(text)
    left, middle, right = st.columns(3)
    left.metric("Decision", result.label)
    middle.metric("Disaster probability", f"{result.probability_disaster:.3f}")
    right.metric("Human review", "Required" if result.abstained else "Not required")
    st.json(result.model_dump())

uploaded = st.file_uploader("Optional CSV batch", type=["csv"])
if uploaded is not None:
    frame = pd.read_csv(uploaded)
    if "text" not in frame.columns:
        st.error("CSV must contain a text column")
    else:
        outputs = [predictor.predict(str(value)).model_dump() for value in frame["text"]]
        st.dataframe(pd.DataFrame(outputs), use_container_width=True)
