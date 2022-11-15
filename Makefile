SRC_DIR = pilgram

all: test clean build;

test:
	poetry run pytest && poetry run flake8 ${SRC_DIR}

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

.PHONY: all test test-benchmark benchmark clean build test-upload upload
