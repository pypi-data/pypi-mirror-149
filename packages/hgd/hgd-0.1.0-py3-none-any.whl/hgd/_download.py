"""
Download utilities.
"""

import os
from pathlib import Path

import gdown

from hgd.config import Config

WEIGHTS_URL = f"https://github.com/bhky/head-gesture-detection/releases/download/v0.1.0/{Config.weights_filename}"


def _get_home_dir() -> str:
    return str(os.getenv("HGD_HOME", default=Path.home()))


def get_default_weights_path() -> str:
    home_dir = _get_home_dir()
    return os.path.join(home_dir, f".hgd/weights/{Config.weights_filename}")


def download_weights_to(weights_path: str) -> None:
    download_dir = os.path.dirname(os.path.abspath(weights_path))
    os.makedirs(download_dir, exist_ok=True)
    print("Pre-trained weights will be downloaded.")
    gdown.download(WEIGHTS_URL, weights_path)
