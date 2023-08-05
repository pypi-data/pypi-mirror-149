#!/usr/bin/python3
import re
from pathlib import Path
from typing import Callable
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QTextCursor, QTextCharFormat
from PyQt5.QtWidgets import QTextEdit

try:
    from ..notes.text import AbstractText, AbstractTextBody, Polling
except (ValueError, ImportError):
    from notes.text import AbstractText, AbstractTextBody, Polling


class HTML(AbstractText, Polling):
    mode = "html"

    def __init__(self, core, path: Path):
        self.body = Body(self)
        super().__init__(core, path)
        self.body._init(self)

    @Polling.load  # Preload and decrypt file content as needed
    def load(self):
        """Loads file content"""
        cursor = self.body.textCursor()
        if self.content.startswith("<!DOCTYPE HTML") or self.path.is_html():
            html = self._toHtml()
            self.body.setHtml(html)
        else:
            self.body.setPlainText(self.content)
        self.body.setTextCursor(cursor)

    def _toHtml(self) -> str:
        """Converts plain text to HTML format, preserving linebreaks and tabs"""
        text = self.content
        head = "<head><style>body { white-space: pre-wrap; }</style></head>"  # Preserve linebreaks height and tabs
        return f"<html>{head}<body>{text}</body></html>"


class Body(AbstractTextBody, QtWidgets.QTextEdit):
    def __init__(self, note):
        super().__init__()
        self.note = note
        self.setObjectName("html")
        self.setAcceptRichText(False)

    def insertFromMimeData(self, mime):
        """Accepts HTML content named 'qrichtext' (assumed to be an internal operation)"""
        accept = self.core.sdb["general"]["accept qrichtext"]
        isNative = re.findall(r'<\s*meta\s+name\s*=\s*"qrichtext".*?/>', mime.html())
        if accept and isNative and mime.hasHtml():
            self.insertHtml(mime.html())
        else:
            super().insertFromMimeData(mime)  # Insert as plain text

    def bold(self):
        Format.bold(self)

    def clearFormat(self):
        Format.clear(self)

    def highlight(self):
        format_ = Format(self)
        format_.highlight()

    def italic(self):
        Format.italic(self)

    def strike(self):
        Format.strike(self)

    def underline(self):
        Format.underline(self)


class Format:
    def __init__(self, body):
        self.qtext = body
        self.bg = body.note.css["highlight-bg"]
        self.fg = body.note.css["highlight-fg"]

    @classmethod
    def bold(cls, qtext):
        """Toggles text decoration for bold"""
        condition, operation = cls._hasBold, cls._setBold
        cls._toggleFormat(qtext, condition, operation)

    def highlight(self):
        """Toggles text decoration for highlighting"""
        condition, operation = self._hasHighlight, self._setHighlight
        self._toggleFormat(self.qtext, condition, operation)

    @classmethod
    def italic(cls, qtext):
        """Toggles text decoration for italic"""
        condition, operation = cls._hasItalic, cls._setItalic
        cls._toggleFormat(qtext, condition, operation)

    @classmethod
    def strike(cls, qtext):
        """Toggles text decoration for strikethrough"""
        condition, operation = cls._hasStrike, cls._setStrike
        cls._toggleFormat(qtext, condition, operation)

    @classmethod
    def underline(cls, qtext):
        """Toggles text decoration for underline"""
        condition, operation = cls._hasUnderline, cls._setUnderline
        cls._toggleFormat(qtext, condition, operation)

    @staticmethod
    def clear(qtext: QTextEdit):
        """Clears all text formatting"""
        charFormat = QTextCharFormat()
        charFormat.setFontItalic(False)
        charFormat.setFontStrikeOut(False)
        charFormat.setFontUnderline(False)
        charFormat.setFontWeight(QtGui.QFont.Normal)
        charFormat.setForeground(charFormat.foreground())
        charFormat.setBackground(charFormat.background())
        qtext.mergeCurrentCharFormat(charFormat)

    @staticmethod
    def _hasBold(charFormat: QTextCharFormat) -> bool:
        return charFormat.fontWeight() == QtGui.QFont.Bold

    @staticmethod
    def _hasHighlight(charFormat: QTextCharFormat) -> bool:
        return charFormat.background().isOpaque()

    @staticmethod
    def _hasItalic(charFormat: QTextCharFormat) -> bool:
        return charFormat.fontItalic()

    @staticmethod
    def _hasStrike(charFormat: QTextCharFormat) -> bool:
        return charFormat.fontStrikeOut()

    @staticmethod
    def _hasUnderline(charFormat: QTextCharFormat) -> bool:
        return charFormat.fontUnderline()

    @staticmethod
    def _setBold(charFormat: QTextCharFormat, enable: bool) -> QTextCharFormat:
        charFormat.setFontWeight(QtGui.QFont.Bold if enable else QtGui.QFont.Normal)
        return charFormat

    def _setHighlight(self, charFormat: QTextCharFormat, enable: bool) -> QTextCharFormat:
        default = QTextCharFormat()
        bg, fg = QtGui.QColor(self.bg), QtGui.QColor(self.fg)
        charFormat.setBackground(bg if enable else default.background())
        charFormat.setForeground(fg if enable else default.foreground())
        return charFormat

    @staticmethod
    def _setItalic(charFormat: QTextCharFormat, enable: bool) -> QTextCharFormat:
        charFormat.setFontItalic(enable)
        return charFormat

    @staticmethod
    def _setStrike(charFormat: QTextCharFormat, enable: bool) -> QTextCharFormat:
        charFormat.setFontStrikeOut(enable)
        return charFormat

    @staticmethod
    def _setUnderline(charFormat: QTextCharFormat, enable: bool) -> QTextCharFormat:
        charFormat.setFontUnderline(enable)
        return charFormat

    @classmethod
    def _toggleFormat(cls, qtext: QTextEdit, condition: Callable, operation: Callable):
        """Toggles a text decoration on the anchor or the selected text"""
        if qtext.textCursor().hasSelection():
            charFormat = cls._reverseSelectionFormat(qtext, condition, operation)
        else:  # Reverses anchor format
            enabled = condition(qtext.currentCharFormat())
            charFormat = QTextCharFormat()
            charFormat = operation(charFormat, not enabled)
        qtext.mergeCurrentCharFormat(charFormat)

    @staticmethod
    def _reverseSelectionFormat(
        qtext: QTextEdit, condition: Callable, operation: Callable
    ) -> QTextCharFormat:
        """Searches for a decoration in the selection then toggle its state"""
        charFormat = QTextCharFormat()
        cursor = qtext.textCursor()

        # Improves reliability compared to the assessment of the selection as a whole
        span = cursor.selectionEnd() - cursor.selectionStart()
        cursor.setPosition(cursor.selectionStart())
        for c in range(span):
            cursor.clearSelection()
            cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor)
            if condition(cursor.charFormat()):
                charFormat = operation(charFormat, False)
                break
        else:
            charFormat = operation(charFormat, True)
        return charFormat
