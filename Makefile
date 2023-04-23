SRC_DIR = pilgram

all: test clean build;

lint:
	poetry run flake8 ${SRC_DIR}

format:
	poetry run black ${SRC_DIR} && poetry run isort ${SRC_DIR}

format-check:
	poetry run black --check ${SRC_DIR} && poetry run isort -c ${SRC_DIR}

test: lint format-check
	poetry run pytest --cov-report=xml:coverage.xml

test-benchmark:
	poetry run pytest --benchmark-only --benchmark-max-time=5 --benchmark-columns="mean,stddev,min,max"

clean:
	find . -type f -name "*.pyc" -delete
	rm -rf dist build *.egg-info

build:
	poetry run python setup.py sdist bdist_wheel

test-upload: clean build
	poetry run twine upload -s -r test dist/*

upload: clean build
	poetry run twine upload -s -r pypi dist/*

.PHONY: all lint format format-check test test-benchmark benchmark clean build test-upload upload
