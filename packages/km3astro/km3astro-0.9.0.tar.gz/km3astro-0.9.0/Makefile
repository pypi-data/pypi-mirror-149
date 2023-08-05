PKGNAME=km3astro

default: build

all: install

install:
	python3 -m pip install .

install-dev:
	python3 -m pip install -e ".[dev]"
	python3 -m pip install -e ".[extras]"

clean:
	python setup.py clean --all

test:
	py.test --junitxml=./reports/junit.xml -o junit_suite_name=$(PKGNAME) tests

benchmark:
	scripts/run_tests.py benchmarks

test-cov:
	py.test --cov ./$(PKGNAME) --cov-report term-missing --cov-report xml:reports/coverage.xml --cov-report html:reports/coverage tests

test-loop: 
	py.test $(ALLNAMES)
	ptw --ext=.py,.pyx --ignore=doc $(ALLNAMES)

.PHONY: black
black:
	black $(PKGNAME)
	black tests
	black examples
	black doc/conf.py
	black setup.py

.PHONY: black-check
black-check:
	black --check $(PKGNAME)
	black --check tests
	black --check examples
	black --check doc/conf.py
	black --check setup.py

.PHONY: all black black-check clean install install-dev test test-cov test-loop benchmark
