import pandas as pd

from crisis_signal.data import grouped_train_test_split


def test_duplicate_groups_do_not_cross_split() -> None:
    frame = pd.DataFrame(
        {
            "normalized_text": ["flood", "flood", "concert", "earthquake", "movie"],
            "group_key": ["flood", "flood", "concert", "earthquake", "movie"],
            "target": [1, 1, 0, 1, 0],
        }
    )
    split = grouped_train_test_split(frame, test_size=0.4, random_state=2)
    assert not (set(split.train.group_key) & set(split.test.group_key))
