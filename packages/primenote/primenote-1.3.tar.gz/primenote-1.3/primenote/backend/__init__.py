#!/usr/bin/python3
import os
import re
import sys
from collections import namedtuple
from dataclasses import dataclass
from glob import glob
from pathlib import Path
from PyQt5.QtGui import QTextFragment

try:
    from ..__id__ import ID
except (ValueError, ImportError):
    from __id__ import ID

DESKTOP_ENVIRONMENT = os.environ.get("DESKTOP_SESSION")
STYLE_DEFAULT = "minimal.css"
PALETTE_DEFAULT = "graphite.css"


class DeepPath(Path):
    _flavour = type(Path())._flavour

    def is_empty(self) -> bool:
        """Verifies if a file or a directory is empty"""
        if self.is_dir():
            empty = not [f for f in self.rglob("*")]
            return empty and not self.is_symlink()

        elif self.is_file():
            empty = self.stat().st_size == 0
            return empty

    def is_html(self) -> bool:
        """Verifies if the note file has HTML content"""
        with open(self, encoding="utf-8") as f:
            return f.read().startswith("<!DOCTYPE HTML")

    def is_nested(self) -> bool:
        """Verifies if the file is at the root of the note repository"""
        return self.relative_to(UserDirs.NOTES).parts[:-1]

    def is_note(self) -> bool:
        """Verifies if the path point to a note file"""
        return self.is_file() and self.suffix in (".png", ".txt")

    def is_relative_to(self, *other):  #
        """Returns True if the path is relative to another path or False
        Legacy support for Python 3.8.7 (added in Python 3.9)"""
        try:
            self.relative_to(*other)
            return True
        except ValueError:
            return False

    def is_script(self) -> bool:
        """Verifies if the note file is a script"""
        try:
            with open(self, encoding="utf-8") as f:
                return bool(re.findall(r"^#!(\/\w+.*)", f.read()))
        except UnicodeDecodeError:
            return False

    def rglob(self, pattern: str) -> list:
        """Search directory recursively"""
        # glob.glob temporarily replaces pathlib.glob to support directory links
        # see https://bugs.python.org/issue33428 (2018)
        path = str(self / "**" / pattern)
        found = glob(path, recursive=True)
        return [DeepPath(f) for f in found]


def configEnum(type_: str, ignored=[]) -> list:
    """Returns a filtered list of configuration files found in user and root folders"""
    Cfg = namedtuple("ConfigFolders", ("user", "root", "ext"))
    config = {
        "palette": Cfg(UserDirs.PALETTES, RootDirs.PALETTES, "css"),
        "style": Cfg(UserDirs.STYLES, RootDirs.STYLES, "css"),
        "terminal": Cfg(UserDirs.TERMINAL, RootDirs.TERMINAL, "colorscheme"),
    }[type_]

    user = [f for f in config.user.glob(f"*.{config.ext}") if f.is_file()]
    root = [f for f in config.root.glob(f"*.{config.ext}") if f.is_file()]
    rootNames = {f.name: f for f in root if f.name not in ignored}
    for f in user:
        if f.name in rootNames:
            del rootNames[f.name]
    root = [rootNames[n] for n in rootNames]
    return user + root


def userDir() -> Path:
    if sys.platform.startswith("win"):
        return DeepPath(Path.home() / ID)
    return DeepPath(Path.home() / ".config" / ID)


@dataclass
class UserDirs:
    CONFIG = userDir()
    NOTES = DeepPath(userDir() / "notes")
    ARCHIVES = CONFIG / "archives"
    LOGS = CONFIG / "logs"
    TRASH = CONFIG / "trash"
    UI = CONFIG / "ui"
    PALETTES = UI / "palettes"
    STYLES = UI / "styles"
    TERMINAL = UI / "terminal"
    VIM = UI / "vim"


@dataclass
class UserFiles:
    CSS = UserDirs.CONFIG / "ui" / "global.css"
    DECORATIONS = UserDirs.CONFIG / "ui" / "decorations.json"
    KEYRING = UserDirs.CONFIG / "master.key"
    LOG = UserDirs.LOGS / "session.log"
    NOTES = UserDirs.CONFIG / "notes.json"
    PROFILES = UserDirs.CONFIG / "profiles.json"
    SETTINGS = UserDirs.CONFIG / "settings.json"
    VIM = UserDirs.VIM / "vimrc"


@dataclass
class RootDirs:
    ROOT = Path(__file__).parents[1]
    FONTS = ROOT / "ui" / "fonts"
    ICONS = ROOT / "ui" / "icons"
    PALETTES = ROOT / "ui" / "palettes"
    STYLES = ROOT / "ui" / "styles"
    TERMINAL = ROOT / "ui" / "terminal"
    VIM = ROOT / "ui" / "vim"
    WIZARD = ROOT / "ui" / "wizard"


@dataclass
class RootFiles:
    CSS = RootDirs.ROOT / "ui" / "global.css"
    VIM = RootDirs.ROOT / "ui" / "vim" / "vimrc"
    DEFAULT_STYLE = RootDirs.STYLES / STYLE_DEFAULT
    DEFAULT_PALETTE = RootDirs.PALETTES / PALETTE_DEFAULT


@dataclass
class CoreActions:
    tray: dict
    browser: dict


@dataclass
class Cursor:
    pos: int
    anchor: int
    fragment: QTextFragment = None


@dataclass
class Tuples:
    Action = namedtuple("Action", ("label", "icon", "call"))
    Cleaner = namedtuple("Cleaner", ("dir", "delay"))
    Mime = namedtuple("Mime", ("type", "data"))
    Mode = namedtuple("Mode", ("icon", "label"))
    NoteIcons = namedtuple("NoteIcons", ("menu", "toolbar"))
    RegexCSS = namedtuple("RegexCSS", ("selector", "elements", "property"))
    SizeGrips = namedtuple("SizeGrips", ("left", "center", "right"))


def sanitizeFileName(text: str, default: str = ""):
    """Ensures that the filename are compliant with Windows and POSIX standards"""
    illegal = (
        "CON",
        "PRN",
        "AUX",
        "NUL",
        "COM1",
        "COM2",
        "COM3",
        "COM4",
        "COM5",
        "COM6",
        "COM7",
        "COM8",
        "COM9",
        "LPT1",
        "LPT2",
        "LPT3",
        "LPT4",
        "LPT5",
        "LPT6",
        "LPT7",
        "LPT8",
        "LPT9",
    )
    if text.upper() in illegal:
        return default

    for c in '\\/:*?"<>|':
        text = text.replace(c, "")
    text = text.replace("..", "")
    return text
