#!/usr/bin/python3
import hashlib
import shutil
from pathlib import Path

try:
    from ..__id__ import APP_NAME
    from ..__db__ import SDB_DEFAULT
    from ..backend import UserDirs, UserFiles, logger
    from ..menus.core import ConfirmPrompt
except (ValueError, ImportError):
    from __id__ import APP_NAME
    from __db__ import SDB_DEFAULT
    from backend import UserDirs, UserFiles, logger
    from menus.core import ConfirmPrompt

log = logger.new(__name__)


class Legacy:
    @classmethod
    def css(cls, core):
        """Removes stale configuraton files installed prior to version 1.3"""
        if core.sdb["legacy"] < 1.3:
            stales = {
                UserFiles.CSS: "5e36002b1a0fce95a47df9b603335d65",
                UserDirs.PALETTES / "graphite.css": "7ff06b4333796b1c8f5af023052d1991",
                UserDirs.PALETTES / "classic.css": "697c22cf0db5b2c1c77cc09c5a93a7b5",
                UserDirs.PALETTES / "northern.css": "38d66b9c288928fa6f904e7dba06822b",
                UserDirs.STYLES / "toolbar.css": "34515e90227deb2dcc6a34a5775e014a",
                UserDirs.STYLES / "minimal.css": "a27d50e188bbe3eb19e337b6113b3883",
                UserDirs.VIM / "vimrc": "dc0f2ef31112f91093d7ccf1c912b70a",
                UserDirs.VIM / "colors" / "flattown.vim": "ceac229594f9541bce9bb06041c17c39",
                UserDirs.TERMINAL / "default.colorscheme": "dde0fac8fb0cd36750e7fdf599b35658",
            }
            for file, md5 in stales.items():
                if cls._fileEqualMD5(file, md5):
                    file.unlink()
                    log.warning(f"Removed deprecated file '{file}'")

            if UserFiles.CSS.is_file():
                name = UserFiles.CSS.parent / f"{UserFiles.CSS.name}.bak"
                UserFiles.CSS.rename(name)
                log.warning(f"Disabled file '{UserFiles.CSS}'")

            colors = UserDirs.VIM / "colors"
            if colors.is_dir() and colors.is_empty():
                colors.rmdir()

    @classmethod
    def menus(cls, core):
        """Replaces non-customized menus to default prior to version 1.3"""
        if core.sdb["legacy"] < 1.3:
            menus = {
                "context menus": "d91125298788cccfb5cfe4b6e80022a6",
                "toolbar menus": "66430991463994a90955af877474e5a0",
            }
            for key, md5 in menus.items():
                currentMenu = str(core.sdb[key])
                if md5 == cls._md5(currentMenu):
                    core.sdb[key].clear()
                    core.sdb[key].update(SDB_DEFAULT[key])
                    log.warning(f"Replaced default '{key}' content")

    @classmethod
    def prompt(cls, core):
        """Proposes notes migration from a legacy version (former QtPad users)"""
        qtpad = UserDirs.CONFIG.parent / "qtpad" / "notes"
        if qtpad.is_dir():
            msg = (
                "Notes from an older version were found in the folder\n"
                f"'{qtpad}'\n\n"
                f"Would you like to copy those into {APP_NAME} notes repository ?"
            )
            dialog = ConfirmPrompt("QtPad Notes Migration", msg)
            if dialog.exec_() == dialog.Yes:
                cls._migrate(qtpad)

    @classmethod
    def _fileEqualMD5(cls, file: Path, md5: str) -> bool:
        """Compares a MD5 hash with a MD5 sum of a file"""
        if not file.is_file():
            return False

        with open(file, encoding="utf-8") as f:
            if md5 == cls._md5(f.read()):
                return True
        return False

    def _md5(text: str) -> str:
        """Computes a MD5 hash from a string"""
        h = hashlib.md5(text.encode("utf8"))
        return h.hexdigest()

    def _migrate(src: Path):
        """Copy notes from a legacy version (former QtPad users)"""
        files = [f for f in src.rglob("*.txt") if f.is_file()]
        files += [f for f in src.rglob("*.png") if f.is_file()]
        for f in files:
            dest = UserDirs.NOTES / f.relative_to(src)
            if dest.exists():
                log.warning(f"Ignored migration of '{f}'")
            else:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(f, dest)
                log.info(f"Copied '{f}'")
