SRC_DIR = pilgram

all: test clean build;

test:
	pipenv run pytest && pipenv run flake8 ${SRC_DIR}

clean:
	rm -rf dist build *.egg-info

build:
	pipenv run python setup.py sdist bdist_wheel

test-upload: clean build
	pipenv run twine upload -s -r test dist/*

upload: clean build
	pipenv run twine upload -s -r pypi dist/*

.PHONY: all clean test build test-upload upload
