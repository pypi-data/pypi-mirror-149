#!/usr/bin/python3
import re
from pathlib import Path
from typing import Union
from PyQt5 import QtWidgets, QtCore, QtGui

try:
    from QTermWidget import QTermWidget
except ImportError:
    QTermWidget = QtCore.QObject

try:
    from ..backend import UserDirs, RootDirs, logger
    from ..notes import Note
except (ValueError, ImportError):
    from backend import UserDirs, RootDirs, logger
    from notes import Note

log = logger.new(__name__)


class Console(Note):
    mode = "console"

    def __init__(self, core, path: Path):
        super().__init__(core, path)
        self._initNoteWindow(path)
        self.body = Terminal(self)
        self.gridLayout.addWidget(self.body, 1, 0, 1, 3)

    def reload(self):
        """Closes and reload the current terminal"""
        self.body.deleteLater()
        self.body = Terminal(self)
        self.gridLayout.addWidget(self.body, 1, 0, 1, 3)
        self.body.setFocus(True)


class Terminal(QTermWidget):
    def __init__(self, note, startnow=1):
        shebang = self._shebang(note.path)
        if shebang and not note.mode == "vim":  # Script execution
            super().__init__(0)
            self.setAutoClose(False)
            self.setShellProgram(shebang)
            self.setArgs([str(note.path)])
            self.startShellProgram()
        else:  # Vim or console
            super().__init__(startnow)

        self.note = note
        self._setupUi()

    def _exit(self):
        """Cleanly discards parent note"""
        note = self.note
        note.core.loaded[note.path].close()

    def _lostFocus(self):
        """Propagates focus out event to Note"""
        event = QtGui.QFocusEvent(QtCore.QEvent.FocusOut)
        QtCore.QCoreApplication.postEvent(self.note, event)

    def _setupUi(self):
        policy = QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        self.setSizePolicy(*policy)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setFlowControlEnabled(False)
        self.setEnvironment(["TERM=xterm"])  # Enable correct mouse & hotkeys capture
        self.finished.connect(self._exit)
        self.termLostFocus.connect(self._lostFocus)

        db = self.note.core.sdb["terminal"]
        font = self.font()
        font.setFamily(db["font family"])
        font.setPointSize(db["font size"])
        colorscheme = Path(db["color scheme"]).stem

        hasCustomSchemes = [f for f in UserDirs.TERMINAL.glob("*.colorscheme") if f.is_file()]
        configDir = UserDirs.TERMINAL if hasCustomSchemes else RootDirs.TERMINAL
        self.setTerminalFont(font)
        self.addCustomColorSchemeDir(str(configDir))
        self.setColorScheme(colorscheme)
        self.setTerminalSizeHint(False)

    def _shebang(self, path: Path) -> Union[str, None]:
        """Determines if a file is a script by parsing its shebang (#!)"""
        with open(path, encoding="utf-8") as f:
            r = re.findall(r"^#!(\/\w+.*)", f.read())
        return r[0] if r else None
