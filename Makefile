SRC_DIR = pilgram

all: test clean build;

test:
	pipenv run pytest && pipenv run flake8 ${SRC_DIR}

test-tox:
	pipenv run tox && pipenv run flake8 ${SRC_DIR}

test-benchmark:
	pipenv run pytest --benchmark-only --benchmark-max-time=5 --benchmark-columns="mean,stddev,min,max"

clean:
	find . -type f -name "*.pyc" -delete
	rm -rf dist build *.egg-info

build:
	pipenv run python setup.py sdist bdist_wheel

test-upload: clean build
	pipenv run twine upload -s -r test dist/*

upload: clean build
	pipenv run twine upload -s -r pypi dist/*

.PHONY: all test test-tox test-benchmark benchmark clean build test-upload upload
