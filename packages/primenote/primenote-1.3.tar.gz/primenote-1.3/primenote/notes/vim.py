#!/usr/bin/python3
from pathlib import Path
from PyQt5 import QtCore

try:
    from QTermWidget import QTermWidget
except ImportError:
    QTermWidget = QtCore.QObject

try:
    from ..backend import UserDirs, UserFiles, RootDirs, RootFiles, logger
    from ..notes import Note
    from ..notes.console import Terminal
    from ..menus.bars import WordsCounter
except (ValueError, ImportError):
    from backend import UserDirs, UserFiles, RootDirs, RootFiles, logger
    from notes import Note
    from notes.console import Terminal
    from menus.bars import WordsCounter

log = logger.new(__name__)


class Vim(Note):
    mode = "vim"

    def __init__(self, core, path: Path):
        super().__init__(core, path)
        self._initNoteWindow(path)
        self.ref = f"note_{id(self)}"
        self.server = VimServer(self)
        self.body = VimTerminal(self)
        self.gridLayout.addWidget(self.body, 1, 0, 1, 3)
        if self.core.sdb["message bar"]["words"]:
            self.wordsCounter = WordsCounter(self)
            self.msgbarLayout.addWidget(self.wordsCounter)
            self.wordsCounter.update()

    def drop(self, mime):
        """Handler for dropped text"""
        with open(self.path, "a", encoding="utf-8", newline="\n") as f:
            f.write(mime.data)


class VimTerminal(Terminal):
    def __init__(self, note):
        super().__init__(note, startnow=0)
        runtime = UserDirs.VIM if UserFiles.VIM.is_file() else RootDirs.VIM
        vimrc = UserFiles.VIM if UserFiles.VIM.is_file() else RootFiles.VIM
        args = [
            "--clean",
            "--noplugin",
            "--servername",
            note.ref,
            "--cmd",
            f"let &rtp.=',{runtime}'",
            "-u",
            str(vimrc),
            str(note.path),
        ]
        self.setShellProgram("vim")
        self.setArgs(args)
        self.startShellProgram()


class VimServer(QtCore.QProcess):
    def __init__(self, note):
        super().__init__()
        self.note = note
        self.setProgram("vim")
        self.setStandardOutputFile(self.nullDevice())
        self.setStandardErrorFile(self.nullDevice())

    def move(self, new: Path):
        """Updates the current file path and working directory in Vim"""
        buffer = f"cd {new.parent} | edit {new.name}"
        autocmd = "autocmd TextChanged,TextChangedI <buffer> silent write"
        args = ["--servername", self.note.ref, "--remote-expr", f'execute("{buffer} | {autocmd}")']

        log.info(f"{self.note.id} : vim {' '.join(args)}")
        self.setArguments(args)
        self.startDetached()
