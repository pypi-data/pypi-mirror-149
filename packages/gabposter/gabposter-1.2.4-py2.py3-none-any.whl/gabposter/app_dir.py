"""
Provides an application directory path.
"""

import pathlib
import sys


def app_dir() -> pathlib.Path:
    """
    Returns a parent directory path
    where persistent application data can be stored.

    # linux: ~/.local/share
    # macOS: ~/Library/Application Support
    # windows: C:/Users/<USER>/AppData/Roaming
    """
    home = pathlib.Path.home()
    out = None
    if sys.platform == "win32":
        out = home / "AppData/Roaming/gabposter"
    elif sys.platform == "linux":
        out = home / ".local/share/gabposter"
    elif sys.platform == "darwin":
        out = home / "Library/Application Support/gabposter"
    assert out, "Unsupported platform"
    out.mkdir(parents=True, exist_ok=True)
    return out
