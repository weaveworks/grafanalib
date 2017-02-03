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
VIRTUALENV_DIR ?= .env
VIRTUALENV_BIN = $(VIRTUALENV_DIR)/bin
DEPS_UPTODATE = $(VIRTUALENV_DIR)/.deps-uptodate

VIRTUALENV := $(shell command -v virtualenv 2> /dev/null)
PIP := $(shell command -v pip 2> /dev/null)

.ensure-virtualenv: .ensure-pip
ifndef VIRTUALENV
	$(error "virtualenv is not installed. Install with `pip install [--user] virtualenv`.")
endif
	touch .ensure-virtualenv

.ensure-pip:
ifndef PIP
	$(error "pip is not installed. Install with `python -m [--user] ensurepip`.")
endif
	touch .ensure-pip

$(VIRTUALENV_BIN)/pip: .ensure-virtualenv
	virtualenv $(VIRTUALENV_DIR)

images:
	$(info $(IMAGE_NAMES))

all: $(UPTODATE_FILES) test lint

$(DEPS_UPTODATE): setup.py $(VIRTUALENV_BIN)/pip
	$(VIRTUALENV_BIN)/pip install -e .[dev]
	touch $(DEPS_UPTODATE)

deps: $(DEPS_UPTODATE)

$(VIRTUALENV_BIN)/flake8: $(DEPS_UPTODATE)

gfdatasource/$(UPTODATE): gfdatasource/*

lint: $(VIRTUALENV_BIN)/flake8
	$(VIRTUALENV_BIN)/flake8 gfdatasource/gfdatasource grafanalib

test:

clean:
	$(SUDO) docker rmi $(IMAGE_NAMES) >/dev/null 2>&1 || true
	rm -rf $(UPTODATE_FILES)
	rm -rf grafanalib.egg-info
	rm $(DEPS_UPTODATE)
	find . -name '*.pyc' | xargs rm

clean-deps:
	rm -rf $(VIRTUALENV_DIR)
