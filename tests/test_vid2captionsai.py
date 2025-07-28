import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
import tempfile
import os

from vid2captionsai import PrepAudioVideo, __version__


class TestPrepAudioVideo(unittest.TestCase):
    def setUp(self):
        self.prep = PrepAudioVideo()
        self.test_dir = tempfile.mkdtemp()
        self.input_path = Path(self.test_dir) / "input_video.mp4"
        # Create a dummy video file for testing
        self.input_path.write_text("dummy video content")

    def tearDown(self):
        # Clean up test directory
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_version_import(self):
        """Test that version is properly imported and not 'unknown'"""
        self.assertIsNotNone(__version__)
        self.assertNotEqual(__version__, "unknown")
        self.assertIsInstance(__version__, str)

    @patch('subprocess.run')
    def test_blank_with_mock(self, mock_run):
        """Test blank method with mocked subprocess calls"""
        mock_run.return_value = MagicMock(returncode=0)
        
        # Mock ffprobe calls
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout="30.0"),  # duration
            MagicMock(returncode=0, stdout="30/1"),  # fps
            MagicMock(returncode=0)  # ffmpeg
        ]
        
        output_path = self.prep.blank(str(self.input_path))
        self.assertTrue(isinstance(output_path, Path))
        self.assertEqual(output_path.suffix, ".mp4")
        self.assertIn("blank", output_path.stem)

    @patch('subprocess.run')
    def test_mask_with_mock(self, mock_run):
        """Test mask method with mocked subprocess calls"""
        mock_run.return_value = MagicMock(returncode=0)
        
        output_path = self.prep.mask(str(self.input_path))
        self.assertTrue(isinstance(output_path, Path))
        self.assertEqual(output_path.suffix, ".mov")
        self.assertIn("mask", output_path.stem)

    def test_blank_default_params(self):
        """Test blank method with default parameters"""
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = [
                MagicMock(returncode=0, stdout="30.0"),
                MagicMock(returncode=0, stdout="30/1"),
                MagicMock(returncode=0)
            ]
            
            output_path = self.prep.blank(str(self.input_path))
            self.assertTrue(isinstance(output_path, Path))
            self.assertEqual(output_path.suffix, ".mp4")

    def test_blank_custom_params(self):
        """Test blank method with custom parameters"""
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = [
                MagicMock(returncode=0, stdout="30.0"),
                MagicMock(returncode=0, stdout="30/1"),
                MagicMock(returncode=0)
            ]
            
            output_path = self.prep.blank(
                str(self.input_path), color="FFFFFF", width=1080, height=720
            )
            self.assertTrue(isinstance(output_path, Path))
            self.assertEqual(output_path.suffix, ".mp4")

    def test_mask_default_params(self):
        """Test mask method with default parameters"""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            
            output_path = self.prep.mask(str(self.input_path))
            self.assertTrue(isinstance(output_path, Path))
            self.assertEqual(output_path.suffix, ".mov")

    def test_mask_custom_params(self):
        """Test mask method with custom parameters"""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            
            output_path = self.prep.mask(
                str(self.input_path), color="FFFFFF", tolerance=0.05, fps=30
            )
            self.assertTrue(isinstance(output_path, Path))
            self.assertEqual(output_path.suffix, ".mov")

    def test_prep_paths(self):
        """Test path preparation utility method"""
        input_path, output_path = self.prep._prep_paths(
            str(self.input_path), suffix="_masked"
        )
        self.assertEqual(input_path, Path(self.input_path))
        self.assertEqual(
            output_path,
            Path(self.input_path).with_stem(Path(self.input_path).stem + "_masked"),
        )

    def test_prep_paths_with_output_path(self):
        """Test path preparation with custom output path"""
        custom_output = Path(self.test_dir) / "custom_output.mov"
        input_path, output_path = self.prep._prep_paths(
            str(self.input_path), suffix="_masked", output_path=str(custom_output)
        )
        self.assertEqual(input_path, Path(self.input_path))
        self.assertEqual(output_path, custom_output)

    def test_invalid_input_path(self):
        """Test behavior with non-existent input file"""
        non_existent = Path(self.test_dir) / "non_existent.mp4"
        
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = [
                MagicMock(returncode=1, stderr="No such file"),  # ffprobe fails
            ]
            
            with self.assertRaises(Exception):
                self.prep.blank(str(non_existent))

    @patch('subprocess.run')
    def test_verbose_mode(self, mock_run):
        """Test verbose mode functionality"""
        mock_run.return_value = MagicMock(returncode=0)
        
        prep_verbose = PrepAudioVideo(verbose=True)
        
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout="30.0"),
            MagicMock(returncode=0, stdout="30/1"),
            MagicMock(returncode=0)
        ]
        
        output_path = prep_verbose.blank(str(self.input_path))
        self.assertTrue(isinstance(output_path, Path))

    def test_color_validation(self):
        """Test color parameter validation"""
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = [
                MagicMock(returncode=0, stdout="30.0"),
                MagicMock(returncode=0, stdout="30/1"),
                MagicMock(returncode=0)
            ]
            
            # Test valid hex colors
            valid_colors = ["000000", "FFFFFF", "FF0000", "00FF00", "0000FF"]
            for color in valid_colors:
                output_path = self.prep.blank(str(self.input_path), color=color)
                self.assertTrue(isinstance(output_path, Path))


class TestCLI(unittest.TestCase):
    """Test CLI functionality"""
    
    def test_cli_import(self):
        """Test that CLI module can be imported"""
        from vid2captionsai.__main__ import cli
        self.assertIsNotNone(cli)

    def test_entry_point_exists(self):
        """Test that the console script entry point is properly configured"""
        import pkg_resources
        
        # This test ensures the entry point is configured correctly
        entry_points = pkg_resources.get_entry_map('vid2captionsai')
        self.assertIn('console_scripts', entry_points)
        self.assertIn('vid2captionsai', entry_points['console_scripts'])


if __name__ == "__main__":
    unittest.main()
