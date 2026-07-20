# Model card: TF-IDF logistic-regression baseline

## Intended use

Research baseline for binary disaster-message classification and demonstration of reproducible, risk-aware inference.

## Not intended for

Autonomous dispatch, medical triage, evacuation orders, policing, immigration enforcement or identifying individuals.

## Training data

User-supplied CSV with `text` and binary `target`. No training dataset is bundled.

## Model

Word and bigram TF-IDF features with class-balanced logistic regression.

## Outputs

Probability of the disaster class and one of three decisions: `disaster`, `not_disaster`, `review`.

## Evaluation

Accuracy, precision, recall, F1, macro F1, Brier score, ECE, coverage, selective accuracy and weighted error cost.

## Limitations

Vocabulary drift, multilingual performance, sarcasm, event shift and intentional misinformation require separate evaluation.
