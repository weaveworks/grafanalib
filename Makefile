.PHONY: all clean lint test
.DEFAULT_GOAL := all

all:

lint:
	flake8 grafanalib

test: lint

clean:
	rm -rf grafanalib.egg-info
	find . -name '*.pyc' | xargs rm
