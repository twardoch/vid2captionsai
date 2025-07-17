#!/bin/bash
# this_file: scripts/test.sh
# Test script for vid2captionsai

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[TEST]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    print_error "Must be run from the project root directory"
    exit 1
fi

print_status "Starting test suite for vid2captionsai..."

# Install test dependencies
print_status "Installing test dependencies..."
python -m pip install --upgrade pip
python -m pip install -e .[testing]

# Run linting
print_status "Running code linting..."
python -m flake8 src/ tests/ || print_warning "Linting issues found"

# Run tests with coverage
print_status "Running tests with coverage..."
python -m pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html

# Test CLI functionality
print_status "Testing CLI functionality..."
python -m vid2captionsai --help || print_warning "CLI help test failed"

# Test package import
print_status "Testing package import..."
python -c "import vid2captionsai; print(f'Successfully imported vid2captionsai version {vid2captionsai.__version__}')"

# Test console script
print_status "Testing console script..."
which vid2captionsai >/dev/null 2>&1 && vid2captionsai --help || print_warning "Console script not in PATH"

print_status "All tests completed!"
print_status "Coverage report generated in htmlcov/ directory"