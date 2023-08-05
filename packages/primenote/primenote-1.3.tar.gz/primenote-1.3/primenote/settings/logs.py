#!/usr/bin/python3
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLabel, QSizePolicy

try:
    from ..backend.database import AutoCheckBox, AutoSpinBox
    from ..settings.base import HSpacer, VSpacer, Page
except (ValueError, ImportError):
    from backend.database import AutoCheckBox, AutoSpinBox
    from settings.base import HSpacer, VSpacer, Page


class PageLogs(Page):
    def __init__(self, *args):
        super().__init__(*args)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(General(self))
        layout.addWidget(Storage(self))
        layout.addItem(VSpacer())


class General(QtWidgets.QGroupBox):
    def __init__(self, parent):
        super().__init__("General", parent)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        archiveBox = AutoSpinBox(parent.db, ("archives", "frequency"))
        archiveBox.setSizePolicy(sizePolicy)
        blankBox = AutoCheckBox("Remove blank notes on startup", parent.db, ("clean", "blanks"))
        archiveFormatText = AutoCheckBox("Text", parent.db, ("archives", "text"))
        archiveFormatImage = AutoCheckBox("Image", parent.db, ("archives", "image"))

        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(blankBox, 0, 0, 1, 3)
        layout.addWidget(QLabel("Create an archive every"), 1, 0, 1, 1)
        layout.addWidget(archiveBox, 1, 1, 1, 1)
        layout.addWidget(QLabel("day(s)"), 1, 2, 1, 1)
        layout.addWidget(QLabel("Archive formats"), 2, 0, 1, 1)
        layout.addWidget(archiveFormatText, 2, 1, 1, 2)
        layout.addWidget(archiveFormatImage, 3, 1, 1, 2)


class Storage(QtWidgets.QGroupBox):
    def __init__(self, parent):
        super().__init__("Storage duration (days)", parent)
        trashBox = AutoSpinBox(parent.db, ("clean", "trash"))
        archiveBox = AutoSpinBox(parent.db, ("clean", "archives"))
        logBox = AutoSpinBox(parent.db, ("clean", "logs"))

        layout = QtWidgets.QGridLayout(self)
        layout.addItem(HSpacer(), 0, 2, 1, 1)
        layout.addWidget(QLabel("Archives"), 0, 0, 1, 1)
        layout.addWidget(archiveBox, 0, 1, 1, 1)
        layout.addWidget(QLabel("Trash"), 1, 0, 1, 1)
        layout.addWidget(trashBox, 1, 1, 1, 1)
        layout.addWidget(QLabel("Logs"), 2, 0, 1, 1)
        layout.addWidget(logBox, 2, 1, 1, 1)
