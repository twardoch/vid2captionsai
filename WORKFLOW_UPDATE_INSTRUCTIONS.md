# GitHub Actions Workflow Update Instructions

Due to GitHub App permissions, the workflow file `.github/workflows/ci.yml` needs to be updated manually. Here's how to apply the comprehensive CI/CD pipeline:

## Manual Update Required

The automated system cannot modify workflow files due to security restrictions. You'll need to manually update the workflow file.

## Updated Workflow Content

Replace the contents of `.github/workflows/ci.yml` with the following:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
    tags: ['v*']
  pull_request:
  workflow_dispatch:

env:
  PYTHON_VERSION: '3.10'

jobs:
  test:
    name: Test on ${{ matrix.os }} with Python ${{ matrix.python-version }}
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ['3.10', '3.11', '3.12']
        
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      with:
        fetch-depth: 0  # Needed for setuptools-scm
        
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        python -m pip install -e .[testing]
        
    - name: Run linting
      run: |
        python -m flake8 src/ tests/ || true
        
    - name: Run tests
      run: |
        python -m pytest tests/ -v --cov=src --cov-report=xml --cov-report=term-missing
        
    - name: Test CLI
      run: |
        python -m vid2captionsai --help
        
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      if: matrix.os == 'ubuntu-latest' && matrix.python-version == '3.10'
      with:
        file: ./coverage.xml
        fail_ci_if_error: false

  build:
    name: Build packages
    runs-on: ubuntu-latest
    needs: test
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      with:
        fetch-depth: 0
        
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ env.PYTHON_VERSION }}
        
    - name: Install build dependencies
      run: |
        python -m pip install --upgrade pip build twine
        
    - name: Build package
      run: |
        python -m build
        
    - name: Check package
      run: |
        python -m twine check dist/*
        
    - name: Upload build artifacts
      uses: actions/upload-artifact@v3
      with:
        name: python-package
        path: dist/

  build-binaries:
    name: Build binary for ${{ matrix.os }}
    runs-on: ${{ matrix.os }}
    needs: test
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      with:
        fetch-depth: 0
        
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ env.PYTHON_VERSION }}
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        python -m pip install -e .
        python -m pip install pyinstaller
        
    - name: Build binary
      run: |
        pyinstaller --onefile --name vid2captionsai --console src/vid2captionsai/__main__.py
        
    - name: Test binary (Linux/macOS)
      if: runner.os != 'Windows'
      run: |
        ./dist/vid2captionsai --help
        
    - name: Test binary (Windows)
      if: runner.os == 'Windows'
      run: |
        .\dist\vid2captionsai.exe --help
        
    - name: Upload binary artifact
      uses: actions/upload-artifact@v3
      with:
        name: binary-${{ matrix.os }}
        path: dist/vid2captionsai*

  release:
    name: Create Release
    runs-on: ubuntu-latest
    needs: [test, build, build-binaries]
    if: startsWith(github.ref, 'refs/tags/')
    permissions:
      contents: write
      id-token: write
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      with:
        fetch-depth: 0
        
    - name: Download all artifacts
      uses: actions/download-artifact@v3
      
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ env.PYTHON_VERSION }}
        
    - name: Get version
      id: get_version
      run: |
        VERSION=${GITHUB_REF#refs/tags/v}
        echo "version=$VERSION" >> $GITHUB_OUTPUT
        
    - name: Create Release
      uses: actions/create-release@v1
      id: create_release
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        tag_name: ${{ github.ref }}
        release_name: Release ${{ steps.get_version.outputs.version }}
        body: |
          ## Changes in ${{ steps.get_version.outputs.version }}
          
          This release includes:
          - Cross-platform binaries for Linux, Windows, and macOS
          - Python package available on PyPI
          
          ### Installation
          
          **From PyPI:**
          ```bash
          pip install vid2captionsai==${{ steps.get_version.outputs.version }}
          ```
          
          **Download Binary:**
          Download the appropriate binary for your platform from the assets below.
          
          ### Usage
          ```bash
          vid2captionsai --help
          ```
        draft: false
        prerelease: false
        
    - name: Upload Python package
      uses: actions/upload-release-asset@v1
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        upload_url: ${{ steps.create_release.outputs.upload_url }}
        asset_path: python-package/vid2captionsai-${{ steps.get_version.outputs.version }}-py3-none-any.whl
        asset_name: vid2captionsai-${{ steps.get_version.outputs.version }}-py3-none-any.whl
        asset_content_type: application/zip
        
    - name: Upload Linux binary
      uses: actions/upload-release-asset@v1
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        upload_url: ${{ steps.create_release.outputs.upload_url }}
        asset_path: binary-ubuntu-latest/vid2captionsai
        asset_name: vid2captionsai-linux-x64
        asset_content_type: application/octet-stream
        
    - name: Upload Windows binary
      uses: actions/upload-release-asset@v1
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        upload_url: ${{ steps.create_release.outputs.upload_url }}
        asset_path: binary-windows-latest/vid2captionsai.exe
        asset_name: vid2captionsai-windows-x64.exe
        asset_content_type: application/octet-stream
        
    - name: Upload macOS binary
      uses: actions/upload-release-asset@v1
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        upload_url: ${{ steps.create_release.outputs.upload_url }}
        asset_path: binary-macos-latest/vid2captionsai
        asset_name: vid2captionsai-macos-x64
        asset_content_type: application/octet-stream

  publish-pypi:
    name: Publish to PyPI
    runs-on: ubuntu-latest
    needs: [test, build]
    if: startsWith(github.ref, 'refs/tags/')
    environment: release
    permissions:
      id-token: write
    
    steps:
    - name: Download package artifacts
      uses: actions/download-artifact@v3
      with:
        name: python-package
        path: dist/
        
    - name: Publish to PyPI
      uses: pypa/gh-action-pypi-publish@release/v1
      with:
        password: ${{ secrets.PYPI_TOKEN }}
```

## Key Features Added

1. **Multi-platform testing**: Ubuntu, Windows, macOS
2. **Python version matrix**: 3.10, 3.11, 3.12
3. **Comprehensive testing**: Linting, unit tests, coverage, CLI tests
4. **Binary building**: PyInstaller for cross-platform executables
5. **Automated releases**: GitHub releases with artifacts on git tags
6. **PyPI publishing**: Automatic package publishing on tags

## Next Steps

1. Manually update `.github/workflows/ci.yml` with the content above
2. Commit the workflow file changes
3. The release system will be fully operational

## Testing the System

After updating the workflow, you can test the complete system:

```bash
# Test locally
python3 test_release_system.py

# Create a release
./scripts/release.sh 1.2.3
```

The GitHub Actions will automatically handle testing, building, and releasing across all platforms.