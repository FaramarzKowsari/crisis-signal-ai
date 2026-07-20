"""Generate a small synthetic dataset for smoke tests and demonstrations."""

from crisis_signal.demo import write_demo_data


if __name__ == "__main__":
    write_demo_data("data/demo.csv")
