# Contributing to vid2captionsai

Thank you for your interest in contributing to vid2captionsai! This document provides guidelines for contributing to the project.

## Development Setup

### Prerequisites

- Python 3.10 or higher
- Git
- Make (optional, for convenient commands)

### Quick Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/twardoch/vid2captionsai.git
   cd vid2captionsai
   ```

2. Set up the development environment:
   ```bash
   ./scripts/dev-setup.sh
   # or
   make dev-setup
   ```

This will:
- Install the package in development mode
- Install all development dependencies
- Set up pre-commit hooks
- Run initial tests

## Development Workflow

### Running Tests

```bash
# Run all tests
./scripts/test.sh
# or
make test

# Run tests with coverage
python -m pytest tests/ -v --cov=src --cov-report=html

# Run linting
make lint
```

### Building the Package

```bash
# Build Python package
./scripts/build.sh
# or
make build

# Build binary executable
make binary
```

### Code Style

We use several tools to maintain code quality:

- **flake8**: For linting
- **black**: For code formatting
- **isort**: For import sorting
- **pre-commit**: For running checks before commits

Format your code:
```bash
make format
```

### Testing

Write tests for new features and bug fixes. Tests should:
- Use Python's unittest framework
- Mock external dependencies (like subprocess calls)
- Cover both success and failure cases
- Be placed in the `tests/` directory

## Release Process

### Semantic Versioning

We use semantic versioning (semver) for releases:
- **Major** (x.0.0): Breaking changes
- **Minor** (x.y.0): New features, backward compatible
- **Patch** (x.y.z): Bug fixes, backward compatible

### Creating a Release

1. Ensure all tests pass:
   ```bash
   make test
   ```

2. Update version and create release:
   ```bash
   ./scripts/release.sh 1.2.3
   # or
   make release VERSION=1.2.3
   ```

This will:
- Run tests to ensure quality
- Create a git tag (e.g., `v1.2.3`)
- Push the tag to GitHub
- Trigger GitHub Actions for:
  - Multi-platform testing
  - Binary compilation
  - PyPI publication
  - GitHub release creation

### What Happens During Release

1. **GitHub Actions CI/CD**:
   - Tests run on Ubuntu, Windows, and macOS
   - Python 3.10, 3.11, and 3.12 are tested
   - Binaries are built for all platforms
   - Package is published to PyPI
   - GitHub release is created with artifacts

2. **Artifacts Created**:
   - Python wheel for PyPI
   - Linux binary (`vid2captionsai-linux-x64`)
   - Windows binary (`vid2captionsai-windows-x64.exe`)
   - macOS binary (`vid2captionsai-macos-x64`)

## Git Tag-Based Versioning

The project uses `setuptools-scm` for automatic versioning based on git tags:

- **Tagged commits**: Use the tag as version (e.g., `v1.2.3` → `1.2.3`)
- **Between tags**: Use development version (e.g., `1.2.3.dev5+g1234567`)
- **Dirty working tree**: Appends `.dirty` to version

### Version Information

Check the current version:
```bash
python -c "import vid2captionsai; print(vid2captionsai.__version__)"
```

## Continuous Integration

### GitHub Actions

We use GitHub Actions for CI/CD with multiple workflows:

1. **Testing**: Runs on every push and PR
2. **Building**: Creates packages and binaries
3. **Release**: Publishes on git tags

### Local Testing

Before pushing, run:
```bash
make test
make lint
make build
```

## Binary Distribution

### PyInstaller

We use PyInstaller to create standalone binaries:

```bash
# Build binary
make binary

# Test binary
./dist/vid2captionsai --help
```

### Cross-Platform Builds

GitHub Actions automatically builds binaries for:
- Linux (x86_64)
- Windows (x86_64)
- macOS (x86_64)

## Project Structure

```
vid2captionsai/
├── src/vid2captionsai/          # Source code
│   ├── __init__.py              # Package initialization
│   ├── __main__.py              # CLI entry point
│   └── vid2captionsai.py        # Main implementation
├── tests/                       # Test files
├── scripts/                     # Build/release scripts
├── .github/workflows/           # GitHub Actions
├── pyproject.toml              # Build configuration
├── setup.cfg                   # Package metadata
├── vid2captionsai.spec         # PyInstaller spec
└── Makefile                    # Development commands
```

## Code Guidelines

### Python Style

- Follow PEP 8
- Use type hints where appropriate
- Write docstrings for public functions
- Keep functions focused and small

### Testing

- Write tests for new functionality
- Mock external dependencies
- Test both success and failure cases
- Maintain high test coverage

### Documentation

- Update README.md for user-facing changes
- Add docstrings to new functions
- Update this file for contributor-facing changes

## Getting Help

- **Issues**: Report bugs or request features on GitHub Issues
- **Discussions**: Use GitHub Discussions for questions
- **Code Review**: All changes go through pull request review

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.