.PHONY: all clean lint test
.DEFAULT_GOAL := all

# Boiler plate for bulding Docker containers.
# All this must go at top of file I'm afraid.
IMAGE_PREFIX := weaveworks
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

images:
	$(info $(IMAGE_NAMES))

all: $(UPTODATE_FILES) test lint

gfdatasource/$(UPTODATE): gfdatasource/*

lint:
	flake8 grafanalib

test:

clean:
	$(SUDO) docker rmi $(IMAGE_NAMES) >/dev/null 2>&1 || true
	rm -rf $(UPTODATE_FILES)
	rm -rf grafanalib.egg-info
	find . -name '*.pyc' | xargs rm
