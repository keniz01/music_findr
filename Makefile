# Variables
PYTHON = python
DATA_ACCESSOR_DIR = back-end/data_accessor
MCP_SERVER_DIR = back-end/mcp_server

.PHONY: install test lint format all clean

# Install all dependencies
install:
	cd $(DATA_ACCESSOR_DIR) && hatch env create
	cd $(MCP_SERVER_DIR) && hatch env create

# Run tests for both packages
test:
	cd $(DATA_ACCESSOR_DIR) && hatch run dev:test
	cd $(MCP_SERVER_DIR) && hatch run dev:test

# Run linting for both packages
lint:
	cd $(DATA_ACCESSOR_DIR) && hatch run dev:lint
	cd $(MCP_SERVER_DIR) && hatch run dev:lint

# Format code for both packages
format:
	cd $(DATA_ACCESSOR_DIR) && hatch run dev:format
	cd $(MCP_SERVER_DIR) && hatch run dev:format

# Type checking for both packages
typecheck:
	cd $(DATA_ACCESSOR_DIR) && hatch run dev:typecheck
	cd $(MCP_SERVER_DIR) && hatch run dev:typecheck

# Run all checks (format, lint, typecheck, test)
all:
	cd $(DATA_ACCESSOR_DIR) && hatch run dev:all
	cd $(MCP_SERVER_DIR) && hatch run dev:all

# Clean up generated files
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -r {} +
	find . -type d -name ".mypy_cache" -exec rm -r {} +
	find . -type d -name "dist" -exec rm -r {} +
	find . -type d -name "build" -exec rm -r {} +
	find . -type d -name "*.egg-info" -exec rm -r {} +

# Development setup (install and setup pre-commit)
setup: install
	pre-commit install

# Build packages
build:
	cd $(DATA_ACCESSOR_DIR) && hatch build
	cd $(MCP_SERVER_DIR) && hatch build

# Install packages in development mode
develop:
	cd $(DATA_ACCESSOR_DIR) && hatch run dev:pip install -e .
	cd $(MCP_SERVER_DIR) && hatch run dev:pip install -e .

# Help target
help:
	@echo "Available targets:"
	@echo "  install    - Install all dependencies"
	@echo "  test      - Run tests for both packages"
	@echo "  lint      - Run linting checks"
	@echo "  format    - Format code using black and isort"
	@echo "  typecheck - Run type checking with mypy"
	@echo "  all       - Run format, lint, typecheck, and tests"
	@echo "  clean     - Clean up generated files"
	@echo "  setup     - Full development setup including pre-commit"
	@echo "  build     - Build both packages"
	@echo "  develop   - Install packages in development mode"
