.PHONY: help check-uv serve build clean check-links sync
UV_CACHE_DIR ?= .uv-cache

help:
	@echo "Available commands:"
	@echo "  make serve        - Serve documentation locally with Zensical"
	@echo "  make build        - Build documentation with Zensical"
	@echo "  make clean        - Clean build artifacts"
	@echo "  make check-links  - Run Zensical-only docs validation build"
	@echo "  make sync         - Sync dependencies with pyproject.toml"

sync:
	@$(MAKE) check-uv
	UV_CACHE_DIR=$(UV_CACHE_DIR) uv sync --all-extras

serve:
	@$(MAKE) check-uv
	UV_CACHE_DIR=$(UV_CACHE_DIR) uv run zensical serve

build:
	@$(MAKE) check-uv
	UV_CACHE_DIR=$(UV_CACHE_DIR) uv run zensical build --clean

clean:
	rm -rf site/
	rm -rf .cache/
	find . -type d -name "__pycache__" -exec rm -rf {} +

check-links:
	@$(MAKE) check-uv
	@echo "Zensical does not yet expose dedicated link validation; running strict build check."
	UV_CACHE_DIR=$(UV_CACHE_DIR) uv run zensical build --clean --strict

check-uv:
	@command -v uv >/dev/null 2>&1 || { \
		echo "Error: 'uv' is required but was not found in PATH."; \
		echo "Install uv: https://astral.sh/uv/install.sh"; \
		exit 1; \
	}
