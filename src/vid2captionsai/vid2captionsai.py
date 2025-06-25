#!/usr/bin/env python3

import logging
import subprocess
from pathlib import Path

import static_ffmpeg


def setup_logging(verbose: bool = False):
    """
    Set up logging configuration based on the verbosity level.

    Args:
        verbose (bool, optional): Flag indicating whether to enable verbose logging. Defaults to False.

    Returns:
        str: The logging level for ffmpeg.

    """
    if verbose:
        logging_level = logging.INFO
        ffmpeg_level = "info"
    else:
        logging_level = logging.WARNING
        ffmpeg_level = "warning"
    logging.basicConfig(level=logging_level, format="\n>> %(message)s")
    return ffmpeg_level


class PrepAudioVideo:
    """
    A class for preparing audio and video files.

    Args:
        ffmpeg_path (str | Path | None): The path to the ffmpeg executable. If None, the default system path will be used.
        ffprobe_path (str | Path | None): The path to the ffprobe executable. If None, the default system path will be used.
        verbose (bool): Whether to enable verbose logging. Defaults to False.

    Attributes:
        _ffmpeg_options (list): Options to be passed to the ffmpeg command.
        _ffprobe_options (list): Options to be passed to the ffprobe command.
        _ffmpeg_path (Path): The resolved path to the ffmpeg executable.
        _ffprobe_path (Path): The resolved path to the ffprobe executable.
        _ffmpeg_run (list): The complete ffmpeg command to be executed.
        _ffprobe_run (list): The complete ffprobe command to be executed.
    """

    def __init__(
        self,
        ffmpeg_path: str | Path | None = None,
        ffprobe_path: str | Path | None = None,
        verbose: bool = False,
    ):
        """
        Initializes the Vid2CaptionsAI object.

        Args:
            ffmpeg_path (str | Path | None, optional): Path to the ffmpeg executable. Defaults to None.
            ffprobe_path (str | Path | None, optional): Path to the ffprobe executable. Defaults to None.
            verbose (bool, optional): Whether to enable verbose logging. Defaults to False.
        """
        ffmpeg_level = setup_logging(verbose)
        self._ffmpeg_options = [
            "-nostdin",
            "-nostats",
            "-v",
            ffmpeg_level,
            "-y",
        ]
        self._ffprobe_options = [
            "-v",
            ffmpeg_level,
        ]
        if ffmpeg_path:
            self._ffmpeg_path = Path(ffmpeg_path).resolve()
        else:
            static_ffmpeg.add_paths()
            self._ffmpeg_path = "static_ffmpeg"
        if ffprobe_path:
            self._ffprobe_path = Path(ffprobe_path).resolve()
        else:
            self._ffprobe_path = "static_ffprobe"
        self._ffmpeg_run = [self._ffmpeg_path] + self._ffmpeg_options
        self._ffprobe_run = [self._ffprobe_path] + self._ffprobe_options

    def _prep_paths(
        self,
        input_path: str | Path | None = None,
        output_path: str | Path | None = None,
        suffix: str | None = None,
    ) -> Path:
        """
        Prepare input and output paths for the video-to-captions conversion.

        Args:
            input_path (str | Path | None): Path to the input video file.
            output_path (str | Path | None): Path to the output captions file.
            suffix (str | None): Suffix to be appended to the input file name for the output file.

        Returns:
            Path: Tuple containing the resolved input and output paths.
        """
        return (
            Path(input_path).resolve(),
            Path(output_path).resolve()
            if output_path
            else Path(input_path).parent / f"{Path(input_path).stem}{suffix}",
        )

    def blank(
        self,
        input_path: str | Path,
        color: str = "000000",
        width: int = 2160,
        height: int = 720,
    ) -> Path:
        """
        Creates a blank video with the original audio from the given input video file.

        Args:
            input_path (str | Path): The path to the input video file.
            color (str, optional): The color of the blank video in hexadecimal format. Defaults to "000000".
            width (int, optional): The width of the blank video in pixels. Defaults to 2160.
            height (int, optional): The height of the blank video in pixels. Defaults to 720.

        Returns:
            Path: The path to the generated blank video file.
        """
        input_path, _ = self._prep_paths(input_path)
        output_path = Path(input_path).parent / f"{Path(input_path).stem}-blank.mp4"
        logging.info(f"Creating blank video with original audio from: {input_path}")

        # Extracting duration and FPS from the original video
        duration = (
            subprocess.check_output(
                self._ffprobe_run
                + [
                    "-i",
                    input_path,
                    "-show_entries",
                    "format=duration",
                    "-of",
                    "csv=p=0",
                ]
            )
            .strip()
            .decode()
        )

        fps = (
            subprocess.check_output(
                self._ffprobe_run
                + [
                    "-i",
                    input_path,
                    "-show_entries",
                    "stream=r_frame_rate",
                    "-select_streams",
                    "v",
                    "-of",
                    "csv=p=0",
                ]
            )
            .strip()
            .decode()
            .split("/")
        )
        fps = float(fps[0]) / float(fps[1])

        # ffmpeg command to generate blank video with the original audio
        subprocess.run(
            self._ffmpeg_run
            + [
                "-f",
                "lavfi",
                "-i",
                f"color=c={color}:s={width}x{height}:r={fps}:d={duration}",
                "-i",
                input_path,
                "-map",
                "0:v:0",  # Use video from the first input (blank video)
                "-map",
                "1:a:0",  # Use audio from the second input (original video)
                "-c:v",
                "libx264",
                "-c:a",
                "aac",
                "-shortest",
                output_path,
            ]
        )
        logging.info(f"Video saved: {output_path}")
        return output_path

    def mask(
        self,
        input_path: str | Path,
        color: str = "000000",
        tolerance: float = 0.01,
        fps: int | None = None,
        output_path: str | Path | None = None,
    ) -> Path:
        """
        Applies a color key mask to a video file.

        Args:
            input_path: Path to the input video file.
            color: Color to be masked in hexadecimal format. Defaults to "000000".
            tolerance: Tolerance level for color matching. Defaults to 0.01.
            fps: Frames per second of the output video. Defaults to None.
            output_path: Path to save the output video file. Defaults to None.

        Returns:
            Path to the output video file.
        """
