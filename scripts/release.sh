#!/bin/bash
# this_file: scripts/release.sh
# Release script for vid2captionsai

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[RELEASE]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    print_error "Must be run from the project root directory"
    exit 1
fi

# Check if git is clean
if [ -n "$(git status --porcelain)" ]; then
    print_error "Git working directory is not clean. Please commit or stash changes."
    exit 1
fi

# Get version to release
VERSION="${1:-}"
if [ -z "$VERSION" ]; then
    print_error "Usage: $0 <version>"
    print_error "Example: $0 1.0.0"
    exit 1
fi

# Validate version format (basic semver check)
if ! echo "$VERSION" | grep -E '^[0-9]+\.[0-9]+\.[0-9]+(-[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*)?(\+[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*)?$'; then
    print_error "Invalid version format. Please use semantic versioning (e.g., 1.0.0)"
    exit 1
fi

print_status "Starting release process for version $VERSION"

# Check if tag already exists
if git tag -l | grep -q "^v$VERSION$"; then
    print_error "Tag v$VERSION already exists"
    exit 1
fi

# Run tests first
print_status "Running tests before release..."
./scripts/test.sh

# Build the package
print_status "Building package..."
./scripts/build.sh

# Create and push tag
print_status "Creating git tag v$VERSION..."
git tag -a "v$VERSION" -m "Release version $VERSION"

print_status "Pushing tag to origin..."
git push origin "v$VERSION"

print_info "Release v$VERSION has been tagged and pushed!"
print_info "GitHub Actions will now:"
print_info "  1. Run tests"
print_info "  2. Build multiplatform binaries"
print_info "  3. Create GitHub release"
print_info "  4. Publish to PyPI"
print_info ""
print_info "Monitor the release at: https://github.com/twardoch/vid2captionsai/actions"