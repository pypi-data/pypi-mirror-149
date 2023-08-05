#!/usr/bin/python3
from pathlib import Path
from typing import Tuple
from PyQt5 import QtCore, QtWidgets, QtGui

try:
    from ..backend import logger
    from ..notes import Note
    from ..menus.bars import MessageLabel
except (ValueError, ImportError):
    from backend import logger
    from notes import Note
    from menus.bars import MessageLabel

log = logger.new(__name__)


class Image(Note):
    mode = "image"
    keepAspectRatio = False

    def __init__(self, core, path: Path):
        super().__init__(core, path)
        self._initNoteWindow(path)
        self.body = Body(self)
        self.gridLayout.addWidget(self.body, 1, 0, 1, 3)
        if core.sdb["message bar"]["pixels"]:
            self.pixelsCounter = PixelsCounter(self)
            self.msgbarLayout.addWidget(self.pixelsCounter)

    def resizeEvent(self, event):
        """Allows to resize window regardless of image size"""
        self.body.setMinimumSize(1, 1)
        if self.body.isVisible():
            super().resizeEvent(event)

    def resizeFit(self):
        """Downsizes large image so they fit on screen"""
        screen = self.core.screen()
        iw, ih = self._size()
        sw, sh = screen.width(), screen.height()
        if iw * 1.2 > sw or ih * 1.2 > sh:
            factor = min(sw / iw, sh / ih) * 0.6
            width = int(iw * factor)
            height = int(ih * factor)
            self.core.pdb[self.id]["width"] = width
            self.core.pdb[self.id]["height"] = height
            self.resize(width, height)
            self.restoreAspectRatio()
        else:
            self._resizeOriginal()

    def resizeOriginal(self):
        """Restores original size"""
        self._resizeOriginal()
        self.restoreAspectRatio()  # Prevent imperfections

    def restoreAspectRatio(self):
        """Adjusts image size to fit original image aspect ratio"""
        # Redraw pixmap with proportional aspect ratio
        self.body.setScaledContents(False)
        self.body.redraw(QtCore.Qt.KeepAspectRatioByExpanding)

        # Adjust window to new scaled image size
        pixmap = self.body.pixmap()
        size = pixmap.width(), pixmap.height()
        self.body.setMinimumSize(*size)
        self.resize(1, 1)

        # Restore default resizing behavior
        self.body.setScaledContents(not self.keepAspectRatio)
        self.body.setMinimumSize(1, 1)

    def toClipboard(self):
        """Copies current image to system clipboard"""
        raise NotImplementedError  # child: _noteImageToClipboard

    def toggleAspectRatio(self):
        """Toggles 'keep aspect ratio' feature"""
        self.keepAspectRatio = not self.keepAspectRatio
        self.body.setScaledContents(not self.keepAspectRatio)
        self.body.redraw(QtCore.Qt.KeepAspectRatio)

        # Refresh toolbar latching icon
        self.setup.actions()
        self.setup.toolbar()

    def _resizeOriginal(self):
        """Restores original size"""
        size = self._size()
        self.body.setMinimumSize(*size)
        self.core.pdb[self.id]["width"] = 1
        self.core.pdb[self.id]["height"] = 1
        self.resize(1, 1)

    def _savePNG(self, path: Path):
        """Saves curent image as a PNG file"""
        f = QtCore.QFile(self.path)
        f.open(QtCore.QIODevice.WriteOnly)
        image = QtGui.QPixmap(str(self.path))
        image.save(f, "PNG")

    def _size(self) -> Tuple[int, int]:
        # Returns original image size
        if not self.path.exists():
            self._savePNG(self.path)
        image = QtGui.QPixmap(str(self.path))
        return image.width(), image.height()


class Body(QtWidgets.QLabel):
    def __init__(self, note):
        super().__init__()
        self.note = note
        self.setObjectName("image")
        image = QtGui.QPixmap(str(note.path))
        policy = QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding

        self.setSizePolicy(*policy)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setScaledContents(True)
        self.setMinimumSize(1, 1)
        self.setPixmap(image)

        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(note.menuTool)

    def focusInEvent(self, event):
        """Forwards focus event to Note"""
        self.note.focusInEvent(event)

    def focusOutEvent(self, event):
        """Forwards focus event to Note"""
        self.note.focusOutEvent(event)

    def redraw(self, aspect: QtCore.Qt.AspectRatioMode):
        """Redraws image at scale"""
        w, h = self.width(), self.height()
        transform = QtCore.Qt.SmoothTransformation
        image = QtGui.QPixmap(str(self.note.path))
        image = image.scaled(w, h, aspect, transformMode=transform)
        self.setPixmap(image)

    def resizeEvent(self, event):
        """Resizes with or without ratio correction"""
        if self.note.keepAspectRatio:
            self.redraw(QtCore.Qt.KeepAspectRatio)


class PixelsCounter(MessageLabel):
    def __init__(self, note):
        self.body = note.body
        super().__init__(note)
        self.setObjectName("msgbar-pixels")

    def _update(self):
        """Updates the pixel counter label for the current image"""
        w, h = self.body.width(), self.body.height()
        self.setText(f"{w} x {h} px")
        self.setVisible(self.core.sdb["message bar"]["pixels"])
