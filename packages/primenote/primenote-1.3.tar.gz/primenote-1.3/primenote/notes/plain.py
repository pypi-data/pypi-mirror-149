#!/usr/bin/python3
from pathlib import Path
from PyQt5 import QtWidgets

try:
    from ..notes.text import AbstractText, AbstractTextBody, Polling
except (ValueError, ImportError):
    from notes.text import AbstractText, AbstractTextBody, Polling


class Plain(AbstractText, Polling):
    mode = "plain"

    def __init__(self, core, path: Path):
        self.body = Body()
        super().__init__(core, path)
        self.body._init(self)

    @Polling.load  # Preload and decrypt file content as needed
    def load(self):
        """Loads file content"""
        cursor = self.body.textCursor()
        self.body.setPlainText(self.content)
        self.body.setTextCursor(cursor)


class Body(AbstractTextBody, QtWidgets.QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.setObjectName("plain")
