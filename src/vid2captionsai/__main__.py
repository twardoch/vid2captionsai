#!/usr/bin/env python3

import fire

from .vid2captionsai import PrepAudioVideo


def cli():
    fire.core.Display = lambda lines, out: print(*lines, file=out)
    fire.Fire(PrepAudioVideo)


if __name__ == "__main__":
    cli()
