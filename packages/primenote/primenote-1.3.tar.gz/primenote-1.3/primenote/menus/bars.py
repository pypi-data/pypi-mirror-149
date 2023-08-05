#!/usr/bin/python3
import re
from typing import Tuple
from PyQt5 import QtCore, QtGui, QtWidgets

try:
    from ..backend import UserDirs, logger
except (ValueError, ImportError):
    from backend import UserDirs, logger

log = logger.new(__name__)


# # # # # TITLE BAR # # # # #


class MouseFilter(QtCore.QObject):
    def __init__(self, note):
        super().__init__()
        self.note = note
        self.core = note.core
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setToolTipDuration(0)
        self.debounce = 0

    def mouseDoubleClickEvent(self, event):
        """Handler for double click event"""
        self.core.execute(self.group, "doubleclick", self.note.path)

    def mousePressEvent(self, event):
        """Handler for mouse button events"""
        buttons = {
            QtCore.Qt.LeftButton: "left",
            QtCore.Qt.MiddleButton: "middle",
            QtCore.Qt.RightButton: "right",
        }
        button = buttons.get(event.button())
        self.core.execute(self.group, button, self.note.path)
        self.note.mousePressEvent(event)

    def wheelEvent(self, event):
        """Handler for mouse wheel events"""
        threshold = self.core.sdb["general"]["wheel threshold"]
        if self.debounce >= threshold:
            direction = "up" if event.angleDelta().y() > 0 else "down"
            self.core.execute(self.group, direction, self.note.path)
        self.debounce += 1 if self.debounce < threshold else -threshold


class TitleCloseButton(QtWidgets.QPushButton, MouseFilter):
    group = "close"

    def __init__(self, note):
        super().__init__(note)
        self.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.setObjectName("topbar-close")
        self.setText("×")


class TitleLabel(QtWidgets.QLabel, MouseFilter):
    group = "title"

    def __init__(self, note):
        super().__init__(note)
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Maximum)
        self.setObjectName("topbar-title")


class TitleStatusButton(QtWidgets.QPushButton, MouseFilter):
    group = "status"

    def __init__(self, note):
        super().__init__(note)
        self.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.setObjectName("topbar-status")


# # # # # MESSAGE BAR # # # # #


class MessageLabel(QtWidgets.QLabel):
    def __init__(self, note):
        super().__init__()
        self.note = note
        self.core = note.core
        self.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        self.update()

    def autoWrap(self):
        """Disables word wrap when the message bar horizontal space is sufficient"""
        self.setWordWrap(self.isBarFull)

    @property
    def isBarFull(self) -> bool:
        """Measures the available horizontal space based on the real width of unwrapped
        labels. This include the space used by CSS padding, margins and font metrics"""
        used = 0
        msgbar = self.note.msgbarFrame
        for label in msgbar.findChildren(QtWidgets.QLabel):
            mock = QtWidgets.QLabel(label.text())
            mock.setObjectName(label.objectName())
            mock.adjustSize()
            used += mock.width()
        margins = self.note.contentsMargins()
        available = self.note.width() - margins.left() - margins.right()
        return (available - used) <= 1

    def update(self):
        """Wrapper for private _update() function. Prevents windows resizing by enabling wordwrap
        before setText() call. Toggles message bar visibility as needed"""
        self.setWordWrap(True)
        self._update()
        self.autoWrap()


class EncryptionLabel(MessageLabel):
    def __init__(self, note):
        super().__init__(note)
        self.setObjectName("msgbar-encryption")
        self.setStyleSheet("padding: 0px 1px 0px 4px;")

    def _update(self):
        """Sets visibility of the encryption indicator"""
        enabled = bool(self.note.key and self.core.sdb["message bar"]["encryption"])
        self.setVisible(enabled)
        if enabled:
            color = QtGui.QColor(self.note.css["preview-fg"])
            icon = self.note.icons.menu["key_encrypt"]
            icon = self.core.colorize(icon, color)
            icon = icon.pixmap(QtCore.QSize(12, 12))
            self.setPixmap(icon)


class FolderLabel(MessageLabel):
    def __init__(self, note):
        super().__init__(note)
        self.setObjectName("msgbar-folder")

    def _update(self):
        """Updates the folder label according to the current note path"""
        path = self.note.path.relative_to(UserDirs.NOTES)
        path = str(path.parent)
        path = "" if path == "." else path
        enabled = bool(path and self.note.core.sdb["message bar"]["folder"])
        self.setText(path)
        self.setVisible(enabled)


class WordsCounter(MessageLabel):
    def __init__(self, note):
        if note.mode in ("plain", "html"):
            note.body.textChanged.connect(self.update)
            note.body.selectionChanged.connect(self.update)
        else:
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.update)
            self.timer.setInterval(1000)
            self.timer.start()
        self.body = note.body
        super().__init__(note)
        self.setObjectName("msgbar-words")

    def _count(self, text: str) -> Tuple[int, int]:
        """Counts the amount of words and characters in a string"""
        words = len(re.findall(r"\S+", text))
        chars = len(text)
        return (words, chars)

    def _external(self) -> Tuple[str, str, str]:
        """Fetches content from file"""
        with open(self.note.path, encoding="utf-8") as f:
            return f.read().rstrip(), "", ""

    def _internal(self) -> Tuple[str, str, str]:
        """Fetches content from Q_TextEdit"""
        cursor = self.body.textCursor()
        prefix, suffix = ("[", "]") if cursor.hasSelection() else ("", "")
        text = cursor.selectedText() if cursor.hasSelection() else self.body.toPlainText()
        return text, prefix, suffix

    def _update(self, force=False):
        """Updates the words counter label for the current selection or the whole text"""
        if self.note.mode == "vim":
            if self.text() and not self.note.isVisible():
                return
            text, prefix, suffix = self._external()
        else:
            text, prefix, suffix = self._internal()

        words, chars = self._count(text)
        wordsNum = "s" if words > 1 else ""
        charsNum = "s" if chars > 1 else ""
        self.setText(f"{prefix}{words} word{wordsNum}, {chars} character{charsNum}{suffix}")
        self.setVisible(self.core.sdb["message bar"]["words"])


# # # # # TOOL BAR # # # # #


class ToolbarSpacer(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        policy = QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Ignored
        self.setSizePolicy(*policy)
        self.setObjectName("toolbar-spacer")
        self.hide()


class ToolButton(QtWidgets.QPushButton):
    def __init__(self, note, action):
        super().__init__()
        self.note = note
        self.action = note.actions[action]
        self.setObjectName("toolbar-icon")
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setToolTip(self.action.label)
        self.clicked.connect(self._clicked)

    def _clicked(self, event):
        """Handler for left click event"""
        log.info(f"{self.note.id} : {self.action.label}")
        try:
            self.action.call()
        except TypeError:
            self.action.call(self.note.path)


# # # # # HOT BAR # # # # #


class HotbarSpacer(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        policy = QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Ignored
        self.setSizePolicy(*policy)
        self.setObjectName("hotbar-spacer")


class SizeGrip(QtWidgets.QSizeGrip):
    def __init__(self, note, tag=None):
        super().__init__(note)
        self.note = note
        self.setObjectName(tag)
        self.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)


class SizeGripVertical(SizeGrip):
    def __init__(self, note):
        super().__init__(note)
        self.setObjectName("center")

    def mousePressEvent(self, event):
        """Blocks horizontal resizing"""
        self.note.setFixedWidth(self.note.width())
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """Restores horizontal resizing"""
        self.note.setFixedWidth(QtWidgets.QWIDGETSIZE_MAX)
        super().mouseReleaseEvent(event)
