#!/usr/bin/env python3

import logging
import subprocess
from pathlib import Path

import static_ffmpeg


def setup_logging(verbose: bool = False):
    if verbose:
        logging_level = logging.INFO
        ffmpeg_level = "info"
    else:
        logging_level = logging.WARNING
        ffmpeg_level = "warning"
    logging.basicConfig(level=logging_level, format="\n>> %(message)s")
    return ffmpeg_level


class PrepAudioVideo:
    def __init__(
        self,
        ffmpeg_path: str | Path | None = None,
        ffprobe_path: str | Path | None = None,
        verbose: bool = False,
    ):
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
    ):
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
    ):
        input_path, output_path = self._prep_paths(
            input_path, output_path, "-alpha.mov"
        )
        logging.info(
            f"Changing #{color} with tolerance {tolerance} to transparent in: {input_path}"
        )

        # Build the basic ffmpeg command
        _ffmpeg_command = self._ffmpeg_run + [
            "-i",
            input_path,
            "-an",  # This option removes the audio stream
            "-vf",
            f"colorkey=0x{color}:{tolerance}:0.1",
            "-c:v",
            "prores_ks",
            "-profile:v",
            "4444",
            "-pix_fmt",
            "yuva444p10le",
        ]

        # Add fps transcoding if fps is specified
        if fps:
            _ffmpeg_command.extend(["-r", str(fps)])
            str_fps = f"{fps}"
        else:
            str_fps = "original"

        # Add the output path to the command
        _ffmpeg_command.append(output_path)

        # Execute the command
        subprocess.run(_ffmpeg_command)
        logging.info(f"Video with {str_fps} fps saved: {output_path}")
        return output_path
