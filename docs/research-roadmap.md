# Research roadmap

## Phase 1 — Reproducible foundations

- Reproduce the original LSTM result.
- Establish classical baselines on a fixed split.
- Add data cards and event-aware splits.

## Phase 2 — Modern encoders

- Benchmark DistilBERT, RoBERTa, DeBERTa and XLM-R.
- Compare full fine-tuning with LoRA/QLoRA where appropriate.
- Publish ablation and calibration studies.

## Phase 3 — Multilingual crisis intelligence

- Evaluate English, Turkish, Persian, Arabic and Spanish.
- Measure cross-lingual transfer and code-switching robustness.
- Separate translated, synthetic and human-authored examples.

## Phase 4 — Multimodal and evidence-aware systems

- Add CrisisMMD-compatible text-image pipelines.
- Detect duplicate and recycled imagery.
- Evaluate evidence retrieval only where retrieval is task-relevant.

## Phase 5 — Human-in-the-loop operations

- Build a review queue and annotation interface.
- Measure reviewer workload, coverage and error cost.
- Add drift alerts, incident playbooks and external validation.
