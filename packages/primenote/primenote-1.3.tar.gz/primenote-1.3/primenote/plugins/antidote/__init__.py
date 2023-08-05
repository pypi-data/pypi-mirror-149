#!/usr/bin/python3
import sys
from pathlib import Path

try:
    from ...backend import logger
except (ValueError, ImportError):
    from backend import logger

log = logger.new(__name__)


def isInstalled() -> bool:
    """Verifies if Antidote is installed"""
    return Path(getBinaryPath()).is_file()


def getBinaryPath() -> str:
    """Finds the path of Antidote executable"""

    def hklm(path: str, name: str) -> str:
        import win32api
        import win32con

        key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE, path)
        return win32api.RegQueryValueEx(key, name)[0]

    if sys.platform.startswith("win"):
        try:
            folder = hklm(r"Software\Druide informatique inc.\Antidote", "DossierAntidote")
            return rf"{folder}\Antidote.exe"  # MS Windows
        except ImportError:
            log.error("pywin32 module not found")
        except BaseException:
            pass
    else:
        if Path("/usr/local/bin/AgentConnectix").is_file():
            return "/usr/local/bin/AgentConnectix"  # Linux (Antidote 10)
        elif Path("/usr/local/bin/Antidote").is_file():
            return "/usr/local/bin/Antidote"  # Linux (Antidote 9)
    return ""  # Unsupported


def getHandler(uid: str, init=False, silent=False) -> object:
    """Returns the right handler class according to the user OS"""
    path = getBinaryPath()
    if Path(path).is_file():
        if sys.platform.startswith("win"):
            try:
                from plugins.antidote.com import Antidote
            except (ValueError, ImportError):
                from ...plugins.antidote.com import Antidote
        else:
            try:
                from plugins.antidote.dbus import Antidote
            except (ValueError, ImportError):
                from ...plugins.antidote.dbus import Antidote
        return Antidote(uid, path, init)
    elif silent:
        log.debug("Could not find Antidote binary")
    else:
        raise FileNotFoundError("Could not find Antidote binary")
    return None
