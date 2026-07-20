# Data policy and schemas

This repository intentionally excludes raw crisis datasets.

## Supported baseline schema

```csv
id,text,target,event_id,language
1,"Bridge collapsed after the earthquake",1,event-001,en
```

Only `text` and `target` are required for the binary baseline. `target` must be `0` or `1`.

## Recommended datasets

- Kaggle NLP Getting Started / Real or Not? NLP with Disaster Tweets.
- HumAID for humanitarian-category classification.
- TREC Incident Streams for information type, actionability and priority.
- CrisisMMD for text-image experiments.

Always read the original license, terms of use and redistribution rules. Do not commit platform data merely because it can be downloaded.

## Acquisition

For Kaggle data, accept the competition rules and run:

```bash
pip install kaggle
python scripts/download_kaggle_data.py
```

## Privacy and safety

Remove or protect personally identifiable information, precise locations of vulnerable people, private communications and graphic content. Synthetic examples must be labeled as synthetic and must never be mixed silently with human-annotated data.
