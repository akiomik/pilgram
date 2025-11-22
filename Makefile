SRC_DIR = pilgram

all: test clean build;

lint:
	uv run ruff check ${SRC_DIR}

format:
	uv run ruff format ${SRC_DIR}

format-check:
	uv run ruff check ${SRC_DIR} && uv run ruff format --check ${SRC_DIR}

typecheck:
	uv run mypy ${SRC_DIR}

test: lint format-check
	uv run pytest

test-benchmark:
	uv run pytest --benchmark-only --benchmark-max-time=5 --benchmark-columns="mean,stddev,min,max"

clean:
	find . -type f -name "*.pyc" -delete
	rm -rf dist build *.egg-info

build:
	uv build

test-upload: clean build
	uv run twine upload -s -r test dist/*

upload: clean build
	uv run twine upload -s -r pypi dist/*

.PHONY: all lint format format-check test test-benchmark benchmark clean build test-upload upload
