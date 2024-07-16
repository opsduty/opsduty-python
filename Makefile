PACKAGE      	= opsduty_client
BASE  	     	= $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
POETRY      	= poetry

V = 0
Q = $(if $(filter 1,$V),,@)
M = $(shell printf "\033[34;1m▶\033[0m")

.PHONY: all
all: lint test ; @ ## Lint and test project
	$Q

$(POETRY): ; $(info $(M) checking POETRY…)
	$Q

$(BASE): | $(POETRY) ; $(info $(M) checking PROJECT…)
	$Q

.PHONY: fix
fix: fix-ruff fix-black | $(BASE) ; @ ## Run all fixers
	$Q

.PHONY: lint
lint: lint-ruff lint-black lint-dmypy | $(BASE) ; @ ## Run all linters
	$Q

.PHONY: test
test: test-pytest | $(BASE) ; @ ## Run pytest
	$Q

# Tests
.PHONY: test-pytest
test-pytest: .venv | $(BASE) ; $(info $(M) running backend tests…) @ ## Run pytest
	$Q cd $(BASE) && PYTHONHASHSEED=0 $(POETRY) run pytest

# Linters

.PHONY: lint-black
lint-black: .venv | $(BASE) ; $(info $(M) running black…) @ ## Run black linter
	$Q cd $(BASE) && $(POETRY) run black --check tests src

.PHONY: lint-ruff
lint-ruff: .venv | $(BASE) ; $(info $(M) running ruff…) @ ## Run ruff linter
	$Q cd $(BASE) && $(POETRY) run ruff check tests src

.PHONY: lint-mypy
lint-mypy: .venv | $(BASE) ; $(info $(M) running mypy…) @ ## Run mypy linter
	$Q cd $(BASE) && $(POETRY) run mypy --show-error-codes --show-column-numbers tests src

.PHONY: lint-dmypy
lint-dmypy: .venv | $(BASE) ; $(info $(M) running mypy…) @ ## Run dmypy linter
	$Q cd $(BASE) && $(POETRY) run -- dmypy run tests src -- --show-error-codes

# Fixers

.PHONY: fix-black
fix-black: .venv | $(BASE) ; $(info $(M) running black…) @ ## Run black fixer
	$Q cd $(BASE) && $(POETRY) run black tests src

.PHONY: fix-ruff
fix-ruff: .venv | $(BASE) ; $(info $(M) running ruff…) @ ## Run ruff fixer
	$Q cd $(BASE) && $(POETRY) run ruff check --fix tests src

# Release
.PHONY: release
release: all ; $(info $(M) running release…) @ ## Run poetry release
	$Q cd $(BASE) && $(POETRY) publish --build --username=__token__ --password=$(PYPI_TOKEN)

# Dependency management

.venv: pyproject.toml poetry.lock | $(BASE) ; $(info $(M) retrieving dependencies…) @ ## Install python dependencies
	$Q cd $(BASE) && $(POETRY) run pip install -U pip
	$Q cd $(BASE) && $(POETRY) install
	@touch $@

# Misc

.PHONY: clean
clean: ; $(info $(M) cleaning…) @ ## Cleanup caches and virtual environment
	@rm -rf .eggs *.egg-info .venv test-reports
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type d -name '*pytest_cache*' -exec rm -rf {} +

.PHONY: help
help: ## This help message
	@grep -E '^[ a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' | sort
