from typing import TextIO

import pytomlpp


def read_config(config_file: TextIO) -> dict:
    return pytomlpp.load(config_file)
