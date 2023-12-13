# `vid2captionsai`

`vid2captionsai` is a Python-based tool designed to prepare videos for use with [captions.ai](https://www.captions.ai/), a platform focused on generating captions for audio and video content. 

[captions.ai](https://www.captions.ai/) allows you to burn nice animated “hard subtitles” into your video. You upload the video and you get the same video but with the subtitles burned in. But what if you’d prefer to have some control? `vid2captionsai` offers two commands that help you get just the subtitles, as a separate video with transparency (without your original video content). 

You can then import that new video into your video editor, overlay it on top of your original video, scale, trim, edit, and have the subtitles rendered on top of your original video the way you want it. 
 
## Installation

Ensure that Python 3.10 or higher is installed on your system, and run: 

```bash
python3 -m pip install --upgrade vid2captionsai
```

Or with the development version: 

```bash
python3 -m pip install --upgrade git+https://github.com/twardoch/vid2captionsai
```

## Usage

After installation, `vid2captionsai` can be used via the command line. It has two commands: 

### `blank`: Create a blank video

Run the `blank` command: 

```bash
vid2captionsai blank /path/to/your/video.mp4 -c 000000 -w 2160 -h 720
``` 

This creates a blank video with the same duration as your original video, and the original sound, but the video track contains a plain background with the specified color (default: black) and specified dimensions (default: 2160x720).

The video will be saved in the same folder as your original video, but with the suffix `-blank.mp4`.

Then upload that video to the [captions.ai](https://www.captions.ai/) web or desktop app, and generate the subtitles. Download the generated file and place it into the same folder as your original video, with the same name but with the suffix `-subs.mp4`.

More info on the `blank` command: 

```
SYNOPSIS
    vid2captionsai blank INPUT_PATH <flags>

POSITIONAL ARGUMENTS
    INPUT_PATH
        Type: str | pathlib.Path

FLAGS
    -c, --color=COLOR
        Type: str
        Default: '000000'
    -w, --width=WIDTH
        Type: int
        Default: 2160
    -h, --height=HEIGHT
        Type: int
        Default: 720
```

### `mask`: Change color to transparent

Once you have your `video-subs.mp4` video, run the tool again with the `mask` command: 

```bash
vid2captionsai mask /path/to/your/video.mp4 -c 000000 -t 0.01 -f 6 -o /path/to/your/video-mask.mov
```

This will create a new video where the specified color will be replaced with full transparency and similar colors within the specified tolerance `-t` will be semi-transparent. The video is saved in the Apple ProRes 4444 codec in the MOV format, which supports alpha transparency. 

The video track will contain just the subtitles produced by captions.ai. Note: =the video won’t have sound (I may add an option in future to keep it). 

Since the background color is transparent, you can import this video into your video editor and overlay it on top of your original content. 

More info about the `mask` command:

```
SYNOPSIS
    vid2captionsai mask INPUT_PATH <flags>

POSITIONAL ARGUMENTS
    INPUT_PATH
        Type: str | pathlib.Path

FLAGS
    -c, --color=COLOR
        Type: str
        Default: '000000'
    -t, --tolerance=TOLERANCE
        Type: float
        Default: 0.01
    -f, --fps=FPS
        Type: Optional[int | None]
        Default: None
    -o, --output_path=OUTPUT_PATH
        Type: Optional[str | pathlib...
        Default: None
```

## Example

![vid2captionsai.jpg](https://twardoch.github.io/vid2captionsai/assets/vid2captionsai.jpg)

This image shows the result of the tool + captions.ai: 

1. `vid2captionsai blank` was used to convert the original video to a new “blank” video in the 2160x720 resolution, against a black background. This resolution is the width of a 4K video and the height of 1/3 of a 4K video, which makes the video a good “container” for the subtitles. 
2. Captions.ai was used to added subtitles to that “blank” video. 
3. Captions.ai was used to export a new video, again at 2160x720 resolution. The exported video has captions.ai-made subtitles hard-burned onto the black background. 
4. `vid2captionsai mask` was used to convert the captions.ai-exported black-background video into a video where the black color is made transparent, and the dark subtitle backdrops are made a little bit semitransparent. 
5. The resulting transparent video is dropped into the video editor (this is the part shown selected in the image), where it can be scaled and positioned freely. 

## Credits & License

- [`vid2captionsai`](https://pypi.org/project/vid2captionsai/) © 2023 Adam Twardoch
- Published under the [Apache-2.0](https://github.com/twardoch/vid2captionsai/blob/main/LICENSE.txt) license
