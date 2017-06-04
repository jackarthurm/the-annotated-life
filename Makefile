SHELL := /bin/bash

ENV_BIN = talenv/bin
PYTHON_EXE = python3.4

init:
	$(ENV_BIN)/pip install -r requirements.txt

dev:
	$(ENV_BIN)/$(PYTHON_EXE) setup.py install

dist:
	$(ENV_BIN)/$(PYTHON_EXE) setup.py sdist --formats=tar,zip

run:
	$(ENV_BIN)/flask run

test: dev
	$(ENV_BIN)/$(PYTHON_EXE) taltest/test_app.py

.PHONY: init dev test dist run