# Variables
VENV := .venv
PYTHON := $(VENV)/bin/python

.PHONY: setup ensure-uv sync run-agent lint format fix test clean

# ---- Setup ----
setup: ensure-uv sync

# Ensure uv is installed
ensure-uv:
	@if ! command -v uv >/dev/null 2>&1; then \
		echo "Installing uv..."; \
		curl -Ls https://astral.sh/uv/install.sh | sh; \
	fi

# Install dependencies (creates venv automatically)
sync:
	uv sync

# ---- Code Quality ----
lint:
	uv run ruff check .

format:
	uv run ruff format .

fix:
	uv run ruff check --fix .

# ---- Testing ----
test:
	uv run pytest

# ---- Cleanup ----
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf $(VENV)
	