.PHONY: install run test lint format

install:
	uv pip install -e .

run:
	uvicorn src.api.main:app --reload

test:
	pytest tests/

lint:
	flake8 src/ tests/

format:
	black src/ tests/
