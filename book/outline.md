# Detailed book outline and code map

## Part I — Crisis informatics and data

1. **When Social Streams Become Sensors** — scope, opportunities and failure modes. Code: `src/crisis_signal/schemas.py`.
2. **The Anatomy of a Crisis Message** — noise, metaphor, urgency and missing context. Code: `src/crisis_signal/text.py`.
3. **Datasets, Licenses and Human Consequences** — Kaggle, HumAID, TREC-IS and CrisisMMD. Docs: `data/README.md`.
4. **Annotation as Measurement** — taxonomies, disagreement and uncertainty. Docs: `docs/dataset-card.md`.
5. **Leakage, Duplicates and Event Shift** — why random splitting can mislead. Code: `src/crisis_signal/data.py`.

## Part II — Model evolution

6. **Classical NLP Is Not Obsolete** — TF-IDF, linear models and interpretability. Code: `models/classical.py`.
7. **Recurrent Memory** — embeddings, LSTM, GRU and the historical notebook. Code: `models/lstm.py`; `legacy/`.
8. **Transformers for Crisis Classification** — encoder fine-tuning. Code: `models/transformer.py`.
9. **Multilingual Transfer** — XLM-R, language imbalance and code-switching. Roadmap: `docs/research-roadmap.md`.
10. **Parameter-Efficient Adaptation** — LoRA, QLoRA and deployment constraints.
11. **LLMs as Structured Classifiers** — prompts, schemas and failure containment. Code: `src/crisis_signal/llm.py`.

## Part III — Trustworthy decisions

12. **Accuracy Is Not Enough** — class imbalance and false-negative cost. Code: `evaluation.py`.
13. **Calibration** — Brier score, ECE and reliability.
14. **The Right to Abstain** — selective prediction and review routing. Code: `predictor.py`.
15. **Robustness Under Noise** — typos, sarcasm, paraphrase and adversarial posts.
16. **Fairness Across Languages and Regions** — subgroup evaluation and access inequality.
17. **Explainability Without Theatre** — useful evidence, not decorative heatmaps.

## Part IV — Multimodal and evidence-aware intelligence

18. **Images as Evidence and Risk** — CrisisMMD and visual ambiguity.
19. **Duplicate and Recycled Images** — cryptographic and perceptual hashes. Code: `multimodal.py`.
20. **Location, Time and Event Clustering** — converting messages into incident structure.
21. **When Retrieval Helps and When It Pollutes** — task-specific RAG evaluation.

## Part V — Engineering, operations and research

22. **From Notebook to Package** — interfaces, tests and dependency isolation.
23. **Serving Models Responsibly** — FastAPI, Docker and health checks. Code: `api.py`.
24. **Streaming and Monitoring** — drift, auditability and replay. Code: `streaming.py`, `monitoring.py`.
25. **Human-in-the-Loop Operations** — review queues and accountability.
26. **Reproducible Research** — fingerprints, artifacts and evidence registries.
27. **Publishing Software, Data and Books** — GitHub releases, Zenodo and separate DOIs.
28. **A Research Agenda for Crisis AI** — open questions and external validation.
