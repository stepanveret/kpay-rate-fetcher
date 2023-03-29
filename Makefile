.PHONY: help
help:              ## Show the help.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep

.PHONY: show
show:              ## Show the current environment.
	@echo "Current environment:"
	@python -V
	@python -m site

.PHONY: install-dev-tools
install-dev-tools: ## Install dev tools(linters, formatters etc.).
	@pip install isort black flake8

.PHONY: fmt
fmt:               ## Format code using black & isort.
	@isort .
	@black --experimental-string-processing --line-length=120 .

.PHONY: lint
lint:              ## Run flake8, black, isort checks.
	@flake8 --max-line-length 120 .
	@isort --check-only .
	@black --check --line-length=120 .