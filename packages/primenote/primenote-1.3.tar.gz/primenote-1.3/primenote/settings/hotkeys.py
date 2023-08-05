#!/usr/bin/python3
import re
from collections import namedtuple
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel

try:
    from ..notes import NoteSetup
    from ..settings.base import Page, ActionBox, ActionTree
except (ValueError, ImportError):
    from notes import NoteSetup
    from settings.base import Page, ActionBox, ActionTree

Action = namedtuple("Action", ("key", "type", "icon"))


class PageHotkeys(Page):
    def __init__(self, *args):
        super().__init__(*args)
        self.addButton = QtWidgets.QPushButton("Add")
        self.addButton.clicked.connect(self._addNewItem)
        self.addButton.setEnabled(False)
        self.delButton = QtWidgets.QPushButton("Delete")
        self.delButton.clicked.connect(self._deleteSelectedItems)
        self.delButton.setEnabled(False)

        self.tree = Tree(self)
        self.tree.itemSelectionChanged.connect(self._treeSelectionChanged)
        self.actionBox = ActionBox(self.core)
        self.actionBox.populate()
        self.actionBox.currentTextChanged.connect(self._addEnabledUpdate)
        self.hotkeyEdit = KeySequenceEdit()
        self.hotkeyEdit.keyComboPressed.connect(self._addEnabledUpdate)
        self.hotkeyEdit.keyComboFailed.connect(self._addEnabledUpdate)

        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(self.tree, 0, 0, 1, 4)
        layout.addWidget(QLabel("Action"), 1, 0, 1, 1)
        layout.addWidget(self.actionBox, 1, 1, 1, 3)
        layout.addWidget(QLabel("Hotkey"), 2, 0, 1, 1)
        layout.addWidget(self.hotkeyEdit, 2, 1, 1, 3)
        layout.addWidget(self.addButton, 3, 2, 1, 1)
        layout.addWidget(self.delButton, 3, 3, 1, 1)

    def _addEnabledUpdate(self):
        """Enables or disables add button"""
        seq = self.hotkeyEdit.sequence
        action = self.actionBox.currentText()
        for item in self.tree.iterate():
            if (item.text(0), item.text(1)) == (seq, action):
                self.addButton.setEnabled(False)
                return
        self.addButton.setEnabled(bool(seq))

    def _addNewItem(self):
        """Adds new hotkey item to tree widget and settings database"""
        seq = self.hotkeyEdit.sequence
        actionLabel = self.actionBox.currentText()
        if seq and actionLabel:
            self.tree.addItem(seq, actionLabel)
            self.tree.save()
            self._addEnabledUpdate()

    def _deleteSelectedItems(self):
        """Deletes selected items from tree and settings database"""
        self.tree.blockSignals(True)
        for i in self.tree.selectedItems():
            self.tree.deleteItem(i)
        self.tree.blockSignals(False)
        self.tree.save()

        self.delButton.setEnabled(False)
        self._addEnabledUpdate()

    def _treeSelectionChanged(self):
        """Updates combo box value from tree selection"""
        for i in self.tree.selectedItems():
            self.hotkeyEdit.sequence = i.text(0)
            self.actionBox.setCurrentText(i.text(1))
            break
        self.delButton.setEnabled(True)
        self._addEnabledUpdate()


class KeySequenceEdit(QtWidgets.QKeySequenceEdit):
    keyComboPressed = QtCore.pyqtSignal()
    keyComboFailed = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self._reset()

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        super().keyPressEvent(event)
        if self.sequence:
            seq = QtGui.QKeySequence(self.sequence)
            self.setKeySequence(seq)
            self.keyComboPressed.emit()
        else:
            self._reset()
            self.keyComboFailed.emit()

    @property
    def sequence(self) -> str:
        """Translates current key sequence into a plain hotkey string"""
        seq = self.keySequence().toString()
        seq = seq.split(",")[-1].strip()
        seq = "" if seq is None else seq
        if seq.count("+"):
            return seq

    @sequence.setter
    def sequence(self, text: str):
        """Sets current key sequence from a string"""
        seq = QtGui.QKeySequence.fromString(text)
        self.setKeySequence(seq)

    def _reset(self):
        """Clears current key sequence"""
        self.clear()
        lineEdit = self.findChild(QtWidgets.QLineEdit)
        lineEdit.setPlaceholderText("Press any key combination ...")


class Tree(ActionTree):
    def __init__(self, parent):
        super().__init__(parent)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.setHeaderLabels(["Hotkey", "Action"])
        self._populate()

    def addItem(self, sequence: str, actionLabel: str):
        """Adds or updates an existing hotkey in the tree"""
        action = self.labelToAction(actionLabel)
        for item in self.iterate():  # Update hotkey in place if already present
            if item.text(0) == sequence:
                item.setText(1, actionLabel)
                item.setIcon(1, action.icon)
                self.setCurrentItem(item)
                break

        else:  # Add new item to tree
            index = self.currentIndex().row() + 1
            item = QtWidgets.QTreeWidgetItem()
            item.setText(0, sequence)
            item.setText(1, actionLabel)
            item.setIcon(1, action.icon)
            self.insertTopLevelItem(index, item)
            self.setCurrentItem(item)

    def deleteItem(self, item: QtWidgets.QTreeWidgetItem):
        """Removes the selected tree item"""
        index = self.indexOfTopLevelItem(item)
        self.takeTopLevelItem(index)

    def save(self):
        """Saves tree content to settings database"""
        keyEvents = {}
        for item in self.iterate():
            hotkey = self._formatHotkey(item.text(0))
            action = self.labelToAction(item.text(1))
            keyEvents[hotkey] = [action.type, action.key]
        self.db["key events"] = keyEvents

    def _formatHotkey(self, text: str) -> str:
        """Translates hotkeys from Mod+Mod+Key to mod,mod;key format"""
        key = re.sub(r"(\+)(?!.*\+)", ";", text.lower())  # Replace last occurence of '+'
        key = key.replace("+", ",")  # Replace all others occurences of '+'
        return key

    def _populate(self):
        """Parses database keys to generate QTreeWidget items"""
        noteActions = NoteSetup.actionsFromMode(self.core)
        coreActions = self.core.actions.tray
        for hotkey, command in self.db["key events"].items():
            type_, key = command
            action = noteActions[key] if type_ == "note" else coreActions[key]
            hotkey = re.sub("[,;]", "+", hotkey).title()
            item = QtWidgets.QTreeWidgetItem()
            item.setIcon(1, action.icon)
            item.setText(0, hotkey)
            item.setText(1, f"{action.label} ({type_})")
            self.addTopLevelItem(item)
        self.resizeColumnToContents(0)
