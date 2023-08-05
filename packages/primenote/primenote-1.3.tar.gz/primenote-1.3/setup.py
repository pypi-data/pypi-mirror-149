#!/usr/bin/python3
import setuptools
import setuptools.command.build_py
import sys
from collections import namedtuple
from pathlib import Path

VERSION = "1.3"
DEPENDANCIES = ["pyqt5", "requests", "cryptography"]
PACKAGE_DATA = ["ui/*", "ui/*/*", "ui/*/*/*"]
APP_NAME = "PrimeNote"
ID = "primenote"
ALIAS = "pnote"

URL = f"https://gitlab.com/william.belanger/{ID}"
AUTHOR = "William Belanger"
DESCRIPTION = "Fanciest sticky note-taking application. Now with Vim!"
LONG_DESCRIPTION = (Path(__file__).parent / "README.md").read_text()
KEYWORDS = "sticky note plain rich text vim css pyqt qt"

PLATFORMS = ["Linux"]
CLASSIFIERS = [
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Programming Language :: Python :: 3.6",
    "Operating System :: POSIX :: Linux",
]

shortcuts = namedtuple("Shortcuts", ("title", "filename", "cmd", "icon"))
SHORTCUTS = [
    shortcuts(APP_NAME, f"{ID}.desktop", ALIAS, "primenote"),
    shortcuts(
        f"{APP_NAME} Settings", f"{ID}-settings.desktop", f"{ALIAS} -c settings", "primenote_settings"
    ),
]


class Shortcuts(setuptools.command.build_py.build_py):
    def run(self):
        for s in SHORTCUTS:
            path = Path(__file__).parent / s.filename
            with open(path, "w") as f:
                f.write(
                    "[Desktop Entry]\n"
                    f"Name={s.title}\n"
                    "Type=Application\n"
                    "Categories=Utility;\n"
                    f"Icon={s.icon}\n"
                    f"Exec={s.cmd}\n"
                )
        setuptools.command.build_py.build_py.run(self)


def datafiles():
    icons_path = [f"{ID}/ui/icons/{s.icon}.svg" for s in SHORTCUTS]
    links_path = [s.filename for s in SHORTCUTS]
    return [
        ("share/icons/hicolor/scalable/apps", icons_path),
        ("share/applications", links_path),
    ]


def setup():
    setuptools.setup(
        name=ID,
        version=VERSION,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        keywords=KEYWORDS,
        author=AUTHOR,
        url=URL,
        classifiers=CLASSIFIERS,
        install_requires=DEPENDANCIES,
        platforms=PLATFORMS,
        cmdclass={"build_py": Shortcuts},
        data_files=datafiles(),
        package_data={"": PACKAGE_DATA},
        packages=setuptools.find_packages(),
        entry_points={"gui_scripts": [f"{ID}={ID}:main", f"{ALIAS}={ID}:main"]},
    )


if __name__ == "__main__":
    if sys.version_info < (3, 6):
        sys.exit("Python 3.6 or later is required to install this package")
    setup()
