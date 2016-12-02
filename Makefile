.PHONY: all clean lint test
.DEFAULT_GOAL := all

all: test lint

lint:
	flake8 grafanalib

test:

clean:
	rm -rf grafanalib.egg-info
	find . -name '*.pyc' | xargs rm
