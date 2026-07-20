.PHONY: install test lint format demo train api docs docker

install:
	python -m pip install -e ".[dev,api]"

test:
	pytest --cov=crisis_signal --cov-report=term-missing

lint:
	ruff check .
	mypy src/crisis_signal

format:
	ruff format .
	ruff check --fix .

demo:
	crisis-signal make-demo-data --output data/demo.csv

train: demo
	crisis-signal train --data data/demo.csv --output artifacts/baseline.joblib

api:
	uvicorn crisis_signal.api:app --reload

docs:
	mkdocs serve

docker:
	docker compose up --build
