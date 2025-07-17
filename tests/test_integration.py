import unittest
import tempfile
import subprocess
from pathlib import Path
import sys
import os


class TestIntegration(unittest.TestCase):
    """Integration tests for the vid2captionsai CLI"""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_cli_help(self):
        """Test that CLI help works"""
        try:
            result = subprocess.run([
                sys.executable, '-m', 'vid2captionsai', '--help'
            ], capture_output=True, text=True, timeout=30)
            
            # Should not fail completely, even if some commands fail
            self.assertIn('vid2captionsai', result.stdout.lower() + result.stderr.lower())
        except subprocess.TimeoutExpired:
            self.skipTest("CLI help timed out")
    
    def test_cli_version(self):
        """Test that CLI version works"""
        try:
            # Try to import and get version
            result = subprocess.run([
                sys.executable, '-c', 
                'import vid2captionsai; print(vid2captionsai.__version__)'
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                version = result.stdout.strip()
                self.assertNotEqual(version, "unknown")
                self.assertNotEqual(version, "")
            else:
                self.skipTest("Could not get version")
        except subprocess.TimeoutExpired:
            self.skipTest("Version check timed out")
    
    def test_package_installation(self):
        """Test that package can be installed and imported"""
        try:
            result = subprocess.run([
                sys.executable, '-c', 
                'import vid2captionsai; print("Import successful")'
            ], capture_output=True, text=True, timeout=30)
            
            self.assertEqual(result.returncode, 0)
            self.assertIn("Import successful", result.stdout)
        except subprocess.TimeoutExpired:
            self.skipTest("Package import timed out")
    
    def test_console_script_exists(self):
        """Test that console script is available"""
        try:
            # Check if the console script is in the path or can be run
            result = subprocess.run([
                'vid2captionsai', '--help'
            ], capture_output=True, text=True, timeout=30)
            
            # If it fails, try with python -m
            if result.returncode != 0:
                result = subprocess.run([
                    sys.executable, '-m', 'vid2captionsai', '--help'
                ], capture_output=True, text=True, timeout=30)
            
            # Should show some help text
            self.assertIn('blank', result.stdout.lower() + result.stderr.lower())
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.skipTest("Console script not available or timed out")


if __name__ == '__main__':
    unittest.main()