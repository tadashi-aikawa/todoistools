MAKEFLAGS += --warn-undefined-variables
SHELL := /bin/bash
ARGS :=
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help

#------

.PHONY: init
init: ## Init
	@echo Start $@
	@pipenv install
	@echo End $@

.PHONY: sort
sort: ## Sort
	@echo Start $@
	@pipenv run python todoistools/main.py sort
	@echo End $@

.PHONY: dry_sort
dry_sort: ## Show tasks sorted but not sort in actual
	@echo Start $@
	@pipenv run python todoistools/main.py sort --dry
	@echo End $@
