# Release System Documentation

This document describes the complete git-tag-based semversioning and release system implemented for vid2captionsai.

## Overview

The release system provides:
- ✅ **Git-tag-based semversioning** using setuptools-scm
- ✅ **Comprehensive test suite** with unit and integration tests
- ✅ **Convenient build and release scripts** for local development
- ✅ **GitHub Actions CI/CD** with multiplatform builds
- ✅ **Automated binary generation** for Linux, Windows, and macOS
- ✅ **Automatic PyPI publishing** on git tags
- ✅ **GitHub releases** with downloadable artifacts

## Components

### 1. Git-Tag-Based Versioning

**Technology**: setuptools-scm

**Configuration**:
- `pyproject.toml`: Configures setuptools-scm
- `src/vid2captionsai/_version.py`: Auto-generated version file
- `src/vid2captionsai/__init__.py`: Version import logic

**How it works**:
- Tagged commits use the tag as version (e.g., `v1.2.3` → `1.2.3`)
- Between tags: development version (e.g., `1.2.3.dev5+g1234567`)
- Dirty working tree: appends `.dirty` to version

### 2. Test Suite

**Location**: `tests/`

**Test Files**:
- `test_vid2captionsai.py`: Core functionality tests with mocking
- `test_integration.py`: Integration tests for CLI and package
- `test_release_system.py`: Release system verification

**Coverage**: Unit tests, integration tests, CLI testing, version validation

### 3. Build and Release Scripts

**Location**: `scripts/`

**Scripts**:
- `dev-setup.sh`: Set up development environment
- `test.sh`: Run complete test suite with coverage
- `build.sh`: Build Python packages
- `release.sh <version>`: Create git tag and trigger release

**Makefile**: Convenient targets for all common tasks

### 4. GitHub Actions CI/CD

**Location**: `.github/workflows/ci.yml`

**Workflow Jobs**:
1. **test**: Multi-platform testing (Ubuntu, Windows, macOS) with Python 3.10, 3.11, 3.12
2. **build**: Build Python packages
3. **build-binaries**: Create standalone executables using PyInstaller
4. **release**: Create GitHub release with artifacts (triggered by git tags)
5. **publish-pypi**: Publish to PyPI (triggered by git tags)

### 5. Binary Generation

**Technology**: PyInstaller

**Configuration**:
- `vid2captionsai.spec`: PyInstaller specification file
- GitHub Actions build matrix for cross-platform compilation

**Outputs**:
- `vid2captionsai-linux-x64`: Linux executable
- `vid2captionsai-windows-x64.exe`: Windows executable
- `vid2captionsai-macos-x64`: macOS executable

## Usage

### Development Workflow

```bash
# Set up development environment
./scripts/dev-setup.sh

# Run tests
./scripts/test.sh
# or
make test

# Build package
./scripts/build.sh
# or
make build

# Build binary
make binary
```

### Release Workflow

```bash
# Create a new release
./scripts/release.sh 1.2.3
# or
make release VERSION=1.2.3
```

**What happens**:
1. Tests are run locally
2. Git tag `v1.2.3` is created and pushed
3. GitHub Actions automatically:
   - Runs tests on all platforms
   - Builds Python packages
   - Creates binaries for Linux, Windows, macOS
   - Creates GitHub release with artifacts
   - Publishes to PyPI

### Installation Options

Users can install via:

1. **Pre-built binaries** (recommended):
   ```bash
   # Download from GitHub releases
   wget https://github.com/twardoch/vid2captionsai/releases/latest/download/vid2captionsai-linux-x64
   chmod +x vid2captionsai-linux-x64
   ./vid2captionsai-linux-x64 --help
   ```

2. **PyPI**:
   ```bash
   pip install vid2captionsai
   ```

3. **From source**:
   ```bash
   git clone https://github.com/twardoch/vid2captionsai.git
   cd vid2captionsai
   pip install -e .
   ```

## Testing the System

Run the comprehensive test:
```bash
python3 test_release_system.py
```

This validates:
- Git versioning
- Project structure
- Script permissions
- GitHub Actions configuration
- Package configuration

## Monitoring

- **GitHub Actions**: Monitor builds at `https://github.com/twardoch/vid2captionsai/actions`
- **PyPI**: Check releases at `https://pypi.org/project/vid2captionsai/`
- **GitHub Releases**: View releases at `https://github.com/twardoch/vid2captionsai/releases`

## Troubleshooting

### Common Issues

1. **Release script fails**: Ensure working directory is clean and tests pass
2. **GitHub Actions fail**: Check secrets (PYPI_TOKEN) and permissions
3. **Binary build fails**: Verify PyInstaller spec file and dependencies
4. **Version not detected**: Ensure git tags are properly formatted (vX.Y.Z)

### Debug Commands

```bash
# Check current version
python -c "import vid2captionsai; print(vid2captionsai.__version__)"

# Check git tags
git tag -l

# Check git describe
git describe --tags

# Test package build
python -m build

# Test binary build
pyinstaller vid2captionsai.spec
```

## Future Enhancements

Potential improvements:
- Code signing for binaries
- ARM64 builds for Apple Silicon
- Linux packages (deb, rpm)
- Homebrew formula
- Docker images
- Automated changelog generation

## Architecture

```
Release Trigger (git tag) → GitHub Actions → Multi-platform Build → Artifacts:
                                                                      ├── PyPI Package
                                                                      ├── GitHub Release
                                                                      ├── Linux Binary
                                                                      ├── Windows Binary
                                                                      └── macOS Binary
```

This system provides a complete, automated release pipeline that maintains high quality through testing while delivering convenient installation options for users.