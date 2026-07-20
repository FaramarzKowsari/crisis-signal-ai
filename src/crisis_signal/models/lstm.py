"""Optional TensorFlow BiLSTM reference model.

This module is intentionally isolated so the core package does not require TensorFlow.
"""

from __future__ import annotations

from typing import Any


def build_bilstm_model(
    vocabulary_size: int,
    sequence_length: int,
    embedding_dim: int = 128,
    recurrent_units: int = 64,
    dropout: float = 0.25,
) -> Any:
    try:
        import tensorflow as tf
    except ImportError as exc:
        raise RuntimeError(
            "Install the optional TensorFlow dependencies: pip install -e '.[tensorflow]'"
        ) from exc

    inputs = tf.keras.Input(shape=(sequence_length,), dtype="int32", name="tokens")
    x = tf.keras.layers.Embedding(
        input_dim=vocabulary_size,
        output_dim=embedding_dim,
        mask_zero=True,
        name="embedding",
    )(inputs)
    x = tf.keras.layers.Bidirectional(
        tf.keras.layers.LSTM(recurrent_units, dropout=dropout),
        name="bidirectional_lstm",
    )(x)
    x = tf.keras.layers.Dropout(dropout)(x)
    outputs = tf.keras.layers.Dense(1, activation="sigmoid", name="probability")(x)
    model = tf.keras.Model(inputs=inputs, outputs=outputs, name="crisis_signal_bilstm")
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=2e-3),
        loss="binary_crossentropy",
        metrics=[
            tf.keras.metrics.BinaryAccuracy(name="accuracy"),
            tf.keras.metrics.Precision(name="precision"),
            tf.keras.metrics.Recall(name="recall"),
        ],
    )
    return model


def default_callbacks(output_path: str) -> list[Any]:
    try:
        import tensorflow as tf
    except ImportError as exc:
        raise RuntimeError("TensorFlow is required for LSTM callbacks") from exc
    return [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss", patience=3, restore_best_weights=True
        ),
        tf.keras.callbacks.ModelCheckpoint(
            output_path, monitor="val_loss", save_best_only=True
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss", factor=0.5, patience=1, min_lr=1e-6
        ),
    ]
