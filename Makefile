.PHONY: all clean clean-deps lint test deps
.DEFAULT_GOAL := all

# Boiler plate for bulding Docker containers.
# All this must go at top of file I'm afraid.
IMAGE_PREFIX := quay.io/weaveworks
IMAGE_TAG := $(shell ./tools/image-tag)
UPTODATE := .uptodate

# Building Docker images is now automated. The convention is every directory
# with a Dockerfile in it builds an image calls quay.io/weaveworks/<dirname>.
# Dependencies (i.e. things that go in the image) still need to be explicitly
# declared.
%/$(UPTODATE): %/Dockerfile
	$(SUDO) docker build -t $(IMAGE_PREFIX)/$(shell basename $(@D)) $(@D)/
	$(SUDO) docker tag $(IMAGE_PREFIX)/$(shell basename $(@D)) $(IMAGE_PREFIX)/$(shell basename $(@D)):$(IMAGE_TAG)
	touch $@

# Get a list of directories containing Dockerfiles
DOCKERFILES=$(shell find * -type f -name Dockerfile ! -path "tools/*" ! -path "vendor/*")
UPTODATE_FILES=$(patsubst %/Dockerfile,%/$(UPTODATE),$(DOCKERFILES))
DOCKER_IMAGE_DIRS=$(patsubst %/Dockerfile,%,$(DOCKERFILES))
IMAGE_NAMES=$(foreach dir,$(DOCKER_IMAGE_DIRS),$(patsubst %,$(IMAGE_PREFIX)/%,$(shell basename $(dir))))

# Python-specific stuff
TOX := $(shell command -v tox 2> /dev/null)
PIP := $(shell command -v pip 2> /dev/null)
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

images:
	$(info $(IMAGE_NAMES))

all: $(UPTODATE_FILES) test lint

deps: setup.py .ensure-tox tox.ini

$(VIRTUALENV_BIN)/flake8 $(VIRTUALENV_BIN)/py.test: $(DEPS_UPTODATE)

gfdatasource/$(UPTODATE): gfdatasource/*

lint: .ensure-flake8
	$(FLAKE8) gfdatasource/gfdatasource grafanalib

test: .ensure-tox
	$(TOX) --skip-missing-interpreters

clean:
	$(SUDO) docker rmi $(IMAGE_NAMES) >/dev/null 2>&1 || true
	rm -rf $(UPTODATE_FILES)
	rm -rf grafanalib.egg-info
	rm -f .ensure-pip .ensure-tox .ensure-flake8
	find . -name '*.pyc' | xargs rm

clean-deps:
	rm -rf $(VIRTUALENV_DIR)
