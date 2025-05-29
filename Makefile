.PHONY: help clean test build release-patch release-minor release-major release-test install dev-install lint

help:
	@echo "Available commands:"
	@echo "  clean         - Clean build artifacts"
	@echo "  test          - Run tests"
	@echo "  build         - Build the package"
	@echo "  release-patch - Release a patch version (0.2.1 -> 0.2.2)"
	@echo "  release-minor - Release a minor version (0.2.1 -> 0.3.0)"
	@echo "  release-major - Release a major version (0.2.1 -> 1.0.0)"
	@echo "  release-test  - Release to Test PyPI"
	@echo "  install       - Install package in development mode"
	@echo "  dev-install   - Install development dependencies"
	@echo "  lint          - Run linting tools"

clean:
	rm -rf build/ dist/ *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

test:
	python manage.py test mem0client

build: clean
	python setup.py sdist bdist_wheel

release-patch:
	python release.py patch

release-minor:
	python release.py minor

release-major:
	python release.py major

release-test: build
	python release.py patch --test

install:
	pip install -e .

dev-install:
	pip install -e .
	pip install twine build wheel

lint:
	python -m flake8 mem0client/ --max-line-length=100
	python -m pylint mem0client/
