#!/usr/bin/env python3
"""
Test script to verify the release system is working correctly.
This script tests all the major components of the release system.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, check=True):
    """Run a command and return result"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"ERROR: {result.stderr}")
        return False
    return result

def test_git_versioning():
    """Test git-based versioning"""
    print("\n=== Testing Git-based Versioning ===")
    
    # Test git describe
    result = run_command("git describe --tags")
    if result:
        print(f"✓ Git describe: {result.stdout.strip()}")
        return True
    return False

def test_project_structure():
    """Test project structure"""
    print("\n=== Testing Project Structure ===")
    
    required_files = [
        "pyproject.toml",
        "setup.cfg", 
        "src/vid2captionsai/__init__.py",
        "src/vid2captionsai/__main__.py",
        "src/vid2captionsai/vid2captionsai.py",
        "tests/test_vid2captionsai.py",
        "tests/test_integration.py",
        "scripts/build.sh",
        "scripts/test.sh",
        "scripts/release.sh",
        "scripts/dev-setup.sh",
        ".github/workflows/ci.yml",
        "vid2captionsai.spec",
        "Makefile",
        "CONTRIBUTING.md"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
        else:
            print(f"✓ {file}")
    
    if missing_files:
        print(f"✗ Missing files: {missing_files}")
        return False
    
    return True

def test_scripts_executable():
    """Test that scripts are executable"""
    print("\n=== Testing Script Permissions ===")
    
    scripts = [
        "scripts/build.sh",
        "scripts/test.sh", 
        "scripts/release.sh",
        "scripts/dev-setup.sh"
    ]
    
    for script in scripts:
        if os.access(script, os.X_OK):
            print(f"✓ {script} is executable")
        else:
            print(f"✗ {script} is not executable")
            return False
    
    return True

def test_github_actions():
    """Test GitHub Actions configuration"""
    print("\n=== Testing GitHub Actions ===")
    
    ci_file = Path(".github/workflows/ci.yml")
    if not ci_file.exists():
        print("✗ CI workflow file missing")
        return False
    
    content = ci_file.read_text()
    
    required_sections = [
        "test:",
        "build:",
        "build-binaries:",
        "release:",
        "publish-pypi:",
        "startsWith(github.ref, 'refs/tags/')",
        "ubuntu-latest",
        "windows-latest", 
        "macos-latest",
        "python-version:",
        "pyinstaller"
    ]
    
    missing_sections = []
    for section in required_sections:
        if section not in content:
            missing_sections.append(section)
        else:
            print(f"✓ Found: {section}")
    
    if missing_sections:
        print(f"✗ Missing sections: {missing_sections}")
        return False
    
    return True

def test_package_config():
    """Test package configuration"""
    print("\n=== Testing Package Configuration ===")
    
    # Check pyproject.toml
    pyproject = Path("pyproject.toml")
    if not pyproject.exists():
        print("✗ pyproject.toml missing")
        return False
    
    content = pyproject.read_text()
    if "setuptools_scm" in content:
        print("✓ setuptools_scm configured")
    else:
        print("✗ setuptools_scm not configured")
        return False
    
    # Check setup.cfg
    setup_cfg = Path("setup.cfg")
    if not setup_cfg.exists():
        print("✗ setup.cfg missing")
        return False
    
    content = setup_cfg.read_text()
    required_sections = [
        "console_scripts",
        "vid2captionsai = vid2captionsai.__main__:cli",
        "testing =",
        "static-ffmpeg",
        "fire"
    ]
    
    for section in required_sections:
        if section in content:
            print(f"✓ Found: {section}")
        else:
            print(f"✗ Missing: {section}")
            return False
    
    return True

def main():
    """Run all tests"""
    print("Testing vid2captionsai release system...")
    
    tests = [
        test_git_versioning,
        test_project_structure,
        test_scripts_executable,
        test_github_actions,
        test_package_config
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        if test():
            passed += 1
            print("✓ PASSED")
        else:
            failed += 1
            print("✗ FAILED")
    
    print(f"\n=== Summary ===")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 All tests passed! Release system is ready.")
        print("\nTo create a release:")
        print("1. ./scripts/release.sh 1.2.3")
        print("2. GitHub Actions will handle the rest")
        return True
    else:
        print("\n❌ Some tests failed. Please fix the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)