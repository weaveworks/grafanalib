.PHONY: all clean clean-deps lint test deps coverage
.DEFAULT_GOAL := all

# Python-specific stuff
TOX := $(shell command -v tox 2> /dev/null)
PIP := $(shell command -v pip3 2> /dev/null)
FLAKE8 := $(shell command -v flake8 2> /dev/null)

.ensure-tox: .ensure-pip
ifndef TOX
	rm -f .ensure-tox
	$(error "tox is not installed. Install with `pip install [--user] tox`.")
endif
	touch .ensure-tox

.ensure-pip:
ifndef PIP
	rm -f .ensure-pip
	$(error "pip is not installed. Install with `python -m [--user] ensurepip`.")
endif
	touch .ensure-pip

.ensure-flake8: .ensure-pip
ifndef FLAKE8
	rm -f .ensure-flake8
	$(error "flake8 is not installed. Install with `pip install [--user] flake8`.")
endif
	touch .ensure-pip

all: test lint coverage

deps: setup.py .ensure-tox tox.ini

$(VIRTUALENV_BIN)/flake8 $(VIRTUALENV_BIN)/py.test: $(DEPS_UPTODATE)

lint: .ensure-flake8
	$(FLAKE8) grafanalib

test: .ensure-tox
	$(TOX) --skip-missing-interpreters

coverage:
	$(TOX) -e coverage

clean:
	rm -rf grafanalib.egg-info
	rm -f .ensure-pip .ensure-tox .ensure-flake8
	find . -name '*.pyc' | xargs rm

clean-deps:
	rm -rf $(VIRTUALENV_DIR)
