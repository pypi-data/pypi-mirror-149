help:
	@echo   "usage: make <target>"
	@echo   "Targets:"
	@echo   "    lint    Reports all linter violations"
	@echo   "    test    Runs all tests"
	@echo   "    build    Builds the library"

lint:
	isort -rc eevend_libs/*
	flake8 eevend_libs

test:
	tox -r

build:
	python setup.py bdist_wheel --universal sdist
