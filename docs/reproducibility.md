# Reproducibility protocol

1. Record the data source, license and download date.
2. Calculate a content fingerprint after validation.
3. Group exact and normalized duplicates before splitting.
4. Record random seeds and split policy.
5. Save configuration, package versions and artifact metadata.
6. Keep historical metrics separate from reproduced runs.
7. Report error analysis and limitations with every promoted model.
8. Prefer event-held-out evaluation when event identifiers exist.

The baseline trainer writes a sidecar `*.metadata.json` file so results can be inspected without deserializing the model.
