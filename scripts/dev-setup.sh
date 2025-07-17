#!/bin/bash
# this_file: scripts/dev-setup.sh
# Development environment setup script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[SETUP]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_status "Setting up development environment for vid2captionsai..."

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    print_error "Must be run from the project root directory"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python --version | cut -d' ' -f2)
print_status "Using Python $PYTHON_VERSION"

# Install package in development mode
print_status "Installing package in development mode..."
python -m pip install --upgrade pip
python -m pip install -e .[testing]

# Install development tools
print_status "Installing development tools..."
python -m pip install pre-commit black isort flake8

# Set up pre-commit hooks
print_status "Setting up pre-commit hooks..."
pre-commit install

# Make scripts executable
print_status "Making scripts executable..."
chmod +x scripts/*.sh

# Run initial tests
print_status "Running initial tests..."
./scripts/test.sh

print_status "Development environment setup complete!"
print_status "You can now:"
print_status "  - Run tests: ./scripts/test.sh"
print_status "  - Build package: ./scripts/build.sh"
print_status "  - Make a release: ./scripts/release.sh <version>"