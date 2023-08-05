#!/usr/bin/python3
import argparse
import shutil
import sys
from pathlib import Path
from typing import Tuple
from PyQt5 import QtCore, QtDBus, QtWidgets

try:
    from .__id__ import ID, HELP
    from .backend import UserDirs, UserFiles, RootDirs, logger
    from .backend.cli import parser
except ImportError:
    from __id__ import ID, HELP
    from backend import UserDirs, UserFiles, RootDirs, logger
    from backend.cli import parser

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
log = logger.new(__name__)


def initialize(args: argparse.Namespace):
    service = f"org.{ID}"
    path = f"/org/{ID}"
    bus = QtDBus.QDBusConnection.sessionBus()
    interface = QtDBus.QDBusInterface(service, path, "", bus)

    if interface.isValid():
        # FIXME: Can a Namespace object be sent through DBus ?
        interface.call("ParseCommands", sys.argv[1:])
        sys.exit(0)
    else:
        with open(UserFiles.LOG, "w", encoding="utf-8"):
            log.info("Cleaned previous session log")

        Setup.install()
        if args.reset:
            Setup.reset(args.reset)
        try:
            app = __import__(f"{ID}.main", fromlist=["main"])
        except ImportError:
            import main as app
        app.main(args)


def main():
    args = parser(sys.argv[1:])  # Early filter for help or malformed commands
    if args.help:
        for h in HELP:
            print(h.expandtabs(18))
        sys.exit(0)
    initialize(args)


class Setup:
    def install():
        """Creates userspace directories and shortcuts"""

        def _dirs():
            dirs = (
                UserDirs.NOTES,
                UserDirs.PALETTES,
                UserDirs.STYLES,
                UserDirs.TERMINAL,
                UserDirs.VIM,
            )
            for path in dirs:
                path.mkdir(parents=True, exist_ok=True)

        def _linksLinux():
            links = {
                UserDirs.PALETTES / "default": RootDirs.PALETTES,
                UserDirs.STYLES / "default": RootDirs.STYLES,
                UserDirs.TERMINAL / "default": RootDirs.TERMINAL,
                UserDirs.VIM / "default": RootDirs.VIM,
            }
            for path, target in links.items():
                try:
                    path.symlink_to(target, target_is_directory=True)
                except FileExistsError:
                    pass

        def _linksWindows():
            links = {
                UserDirs.PALETTES / "default.lnk": RootDirs.PALETTES,
                UserDirs.STYLES / "default.lnk": RootDirs.STYLES,
                UserDirs.TERMINAL / "default.lnk": RootDirs.TERMINAL,
                UserDirs.VIM / "default.lnk": RootDirs.VIM,
            }
            from win32com.client import Dispatch

            shell = Dispatch("WScript.Shell")
            for path, target in links.items():
                path, target = str(path), str(target)
                shortcut = shell.CreateShortCut(path)
                shortcut.Targetpath = target
                shortcut.save()

        def _readme():
            path = UserDirs.UI / "readme.txt"
            if path.exists():
                return

            with open(path, "w", encoding="utf-8") as f:
                f.write(
                    "Users can create their own styles and palettes simply by dropping new CSS\n"
                    "files in the relevant folders. In case of a file name collision, default\n"
                    "configuration is overridden. Default styles and palettes can be ignored\n"
                    "by adding new file names under 'general/ignored css' (settings.json).\n\n"
                    "Vim and QTermWidget palettes are also fully customizable. A typical\n"
                    "approach is to copy a file from the 'default' folders and to edit it.\n"
                    "Qt's CSS documentation and QTermWidget color schemes can be found at:\n\n"
                    "https://doc.qt.io/qt-5/stylesheet-syntax.html\n"
                    "https://doc.qt.io/qt-5/stylesheet-reference.html\n"
                    "https://stuff.mit.edu/afs/athena/software/texmaker_v5.0.2/qt57/doc/qtwidgets/stylesheet-examples.html\n"
                    "https://github.com/lxqt/qtermwidget/tree/master/lib/color-hasCustomSchemes"
                )

        _dirs()
        _readme()
        if sys.platform.startswith("win"):
            _linksWindows()
        else:
            _linksLinux()

    @classmethod
    def reset(cls, args: str):
        """Resets userspace configuration files"""
        if args == "all":
            cls.reset("settings")
            cls.reset("profiles")

        elif args == "settings":
            cls._deleteFiles((UserFiles.SETTINGS, UserFiles.NOTES))

        elif args == "profiles":
            cls._deleteFiles((UserFiles.PROFILES,))

    def _copyFile(src: Path, dest: Path):
        """Copies a file and creates its parent tree"""
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest)

    @classmethod
    def _deleteFiles(cls, paths: Tuple[Path]):
        """Removes files without errors"""
        for path in paths:
            try:
                path.unlink()
                log.warning(f"Removed user file '{cls._shortName(path)}'")
            except PermissionError:
                log.error(f"PermissionError: Could not delete '{cls._shortName(path)}'")
            except FileNotFoundError:
                log.error(f"FileNotFoundError: Could not delete '{cls._shortName(path)}'")

    @classmethod
    def _hasChanges(cls, root: Path, user: Path) -> bool:
        """Verifies if two files are the same"""
        with open(root, encoding="utf-8") as f1, open(user, encoding="utf-8") as f2:
            return f1.read() != f2.read()

    @classmethod
    def _overwrite(cls, root: Path, user: Path):
        """Prompts user before overwriting existing configuration"""
        log.warning(f"Resetting '{cls._shortName(user)}'")
        if cls._prompt(f"This will overwrite all changes made in '{user.name}'. Continue?"):
            cls._copyFile(root, user)
            log.warning(f"Overwritten user file '{cls._shortName(user)}'")

    def _prompt(question: str) -> bool:
        """Command-line interface prompt for user confirmation"""
        reply = None
        while reply not in ("", "y", "n"):
            reply = input(f"{question} (Y/n): ").lower()
        return reply in ("", "y")

    @classmethod
    def _resetFiles(cls, files: tuple):
        """Copies non-existent configuration, else prompt user for overwriting"""
        for root, user in files:
            if not user.exists():
                cls._copyFile(root, user)
                log.info(f"Copied default file '{cls._shortName(user)}'")
            elif cls._hasChanges(root, user):
                cls._overwrite(root, user)

    def _shortName(path: Path) -> str:
        """Replaces path to home directory with ~"""
        return str(path).replace(str(Path.home()), "~")


if __name__ == "__main__":
    main()
