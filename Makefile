SRC_DIR = pilgram

all: check clean build;

sync:
	uv sync --all-extras --dev

lint:
	uv run ruff check ${SRC_DIR}

lint-fix:
	uv run ruff check --fix ${SRC_DIR}

format:
	uv run ruff format ${SRC_DIR}

format-check:
	uv run ruff check ${SRC_DIR} && uv run ruff format --check ${SRC_DIR}

type-check:
	uv run mypy ${SRC_DIR}

test:
	uv run pytest

check: lint format-check type-check test

test-benchmark:
	uv run pytest --benchmark-only --benchmark-max-time=5 --benchmark-columns="mean,stddev,min,max"

clean:
	find . -type f -name "*.pyc" -delete
	rm -rf dist build *.egg-info

build:
	uv build

test-upload: clean build
	uv publish --repository testpypi dist/*

upload: clean build
	uv publish dist/*

.PHONY: all sync lint lint-fix format format-check type-check test check test-benchmark benchmark clean build test-upload upload
