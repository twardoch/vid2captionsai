import unittest
from pathlib import Path

from vid2captionsai import PrepAudioVideo


class TestPrepAudioVideo(unittest.TestCase):
    def setUp(self):
        self.prep = PrepAudioVideo()
        self.input_path = "input_video.mp4"

    def test_blank(self):
        prep = PrepAudioVideo()
        input_path = "input_video.mp4"
        output_path = prep.blank(input_path)
        self.assertTrue(output_path.exists())

    def test_mask(self):
        prep = PrepAudioVideo()
        input_path = "input_video.mp4"
        output_path = prep.mask(input_path)
        self.assertTrue(output_path.exists())

    def test_blank_default_params(self):
        output_path = self.prep.blank(self.input_path)
        self.assertTrue(output_path.exists())
        self.assertEqual(output_path.suffix, ".mp4")

    def test_blank_custom_params(self):
        output_path = self.prep.blank(
            self.input_path, color="FFFFFF", width=1080, height=720
        )
        self.assertTrue(output_path.exists())
        self.assertEqual(output_path.suffix, ".mp4")

    def test_mask_default_params(self):
        output_path = self.prep.mask(self.input_path)
        self.assertTrue(output_path.exists())
        self.assertEqual(output_path.suffix, ".mp4")

    def test_mask_custom_params(self):
        output_path = self.prep.mask(
            self.input_path, color="FFFFFF", tolerance=0.05, fps=30
        )
        self.assertTrue(output_path.exists())
        self.assertEqual(output_path.suffix, ".mp4")

    def test_prep_paths(self):
        input_path, output_path = self.prep._prep_paths(
            self.input_path, suffix="_masked"
        )
        self.assertEqual(input_path, Path(self.input_path))
        self.assertEqual(
            output_path,
            Path(self.input_path).with_stem(Path(self.input_path).stem + "_masked"),
        )


if __name__ == "__main__":
    unittest.main()
