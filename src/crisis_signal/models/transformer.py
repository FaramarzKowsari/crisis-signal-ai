"""Optional Hugging Face transformer fine-tuning adapter."""

from __future__ import annotations

import inspect
from typing import Any


def fine_tune_sequence_classifier(
    train_dataset: Any,
    eval_dataset: Any,
    model_name: str = "distilbert-base-uncased",
    output_dir: str = "artifacts/transformer",
    num_train_epochs: float = 3.0,
    learning_rate: float = 2e-5,
) -> Any:
    try:
        from transformers import (
            AutoModelForSequenceClassification,
            AutoTokenizer,
            DataCollatorWithPadding,
            Trainer,
            TrainingArguments,
        )
    except ImportError as exc:
        raise RuntimeError(
            "Install transformer dependencies: pip install -e '.[transformers]'"
        ) from exc

    tokenizer = AutoTokenizer.from_pretrained(model_name)

    def tokenize(batch: dict[str, list[str]]) -> dict[str, Any]:
        return tokenizer(batch["text"], truncation=True, max_length=256)

    tokenized_train = train_dataset.map(tokenize, batched=True)
    tokenized_eval = eval_dataset.map(tokenize, batched=True)
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name, num_labels=2
    )

    kwargs: dict[str, Any] = {
        "output_dir": output_dir,
        "learning_rate": learning_rate,
        "per_device_train_batch_size": 16,
        "per_device_eval_batch_size": 32,
        "num_train_epochs": num_train_epochs,
        "weight_decay": 0.01,
        "save_strategy": "epoch",
        "load_best_model_at_end": True,
        "metric_for_best_model": "eval_loss",
        "report_to": [],
    }
    parameters = inspect.signature(TrainingArguments.__init__).parameters
    if "eval_strategy" in parameters:
        kwargs["eval_strategy"] = "epoch"
    else:
        kwargs["evaluation_strategy"] = "epoch"

    arguments = TrainingArguments(**kwargs)
    trainer = Trainer(
        model=model,
        args=arguments,
        train_dataset=tokenized_train,
        eval_dataset=tokenized_eval,
        processing_class=tokenizer,
        data_collator=DataCollatorWithPadding(tokenizer=tokenizer),
    )
    trainer.train()
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    return trainer
