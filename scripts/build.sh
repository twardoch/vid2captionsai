#!/bin/bash
# this_file: scripts/build.sh
# Build script for vid2captionsai

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[BUILD]${NC} $1"
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

print_status "Starting build process for vid2captionsai..."

# Clean previous builds
print_status "Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info/

# Install build dependencies
print_status "Installing build dependencies..."
python -m pip install --upgrade pip build twine

# Generate version file
print_status "Generating version information..."
python -c "
import setuptools_scm
version = setuptools_scm.get_version()
print(f'Building version: {version}')
"

# Build the package
print_status "Building package..."
python -m build

# Check the built package
print_status "Checking built package..."
python -m twine check dist/*

# List built files
print_status "Built files:"
ls -la dist/

print_status "Build completed successfully!"
print_status "Files ready in dist/ directory"