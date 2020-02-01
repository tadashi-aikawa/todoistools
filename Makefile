MAKEFLAGS += --warn-undefined-variables
SHELL := /bin/bash
ARGS :=
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help

.PHONY: $(shell egrep -oh ^[a-zA-Z0-9][a-zA-Z0-9_-]+: $(MAKEFILE_LIST) | sed 's/://')

help: ## Print this help
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9][a-zA-Z0-9_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

#------

init: ## Init
	@echo Start $@
	@pipenv install
	@echo End $@

sort: ## Sort
	@echo Start $@
	@pipenv run python todoistools/main.py sort
	@echo End $@

dry_sort: ## Show tasks sorted but not sort in actual
	@echo Start $@
	@pipenv run python todoistools/main.py sort --dry
	@echo End $@
