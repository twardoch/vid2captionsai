# this_file: Makefile
# Makefile for vid2captionsai

.PHONY: help install test build clean dev-setup release lint format binary

help:
	@echo "Available targets:"
	@echo "  help      - Show this help message"
	@echo "  install   - Install package in development mode"
	@echo "  test      - Run tests with coverage"
	@echo "  lint      - Run linting"
	@echo "  format    - Format code"
	@echo "  build     - Build Python package"
	@echo "  binary    - Build binary executable"
	@echo "  clean     - Clean build artifacts"
	@echo "  dev-setup - Set up development environment"
	@echo "  release   - Create a new release (requires VERSION=x.y.z)"

install:
	python -m pip install -e .[testing]

test:
	./scripts/test.sh

lint:
	python -m flake8 src/ tests/

format:
	python -m black src/ tests/
	python -m isort src/ tests/

build:
	./scripts/build.sh

binary:
	python -m pip install pyinstaller
	pyinstaller vid2captionsai.spec

clean:
	rm -rf build/ dist/ *.egg-info/
	rm -rf .pytest_cache/ .coverage htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

dev-setup:
	./scripts/dev-setup.sh

release:
ifndef VERSION
	$(error VERSION is not set. Use: make release VERSION=1.0.0)
endif
	./scripts/release.sh $(VERSION)

# CI targets
ci-test:
	python -m pytest tests/ -v --cov=src --cov-report=xml --cov-report=term-missing

ci-build:
	python -m build

ci-binary:
	pyinstaller --onefile --name vid2captionsai --console src/vid2captionsai/__main__.py