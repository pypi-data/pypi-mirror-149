#!/usr/bin/python3
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel

try:
    from ..backend.database import AutoSpinBox
    from ..notes import NoteSetup
    from ..settings.base import Page, ActionBox, ActionTree
except (ValueError, ImportError):
    from backend.database import AutoSpinBox
    from notes import NoteSetup
    from settings.base import Page, ActionBox, ActionTree

KEY_TO_TRIGGER = {
    "tray": "Tray icon",
    "status": "Status icon",
    "title": "Titlebar",
    "close": "Close button",
    "left": "Left click",
    "middle": "Middle click",
    "right": "Right click",
    "doubleclick": "Doubleclick",
    "up": "Wheel up",
    "down": "Wheel down",
}
TRIGGER_TO_KEY = {v: k for k, v in KEY_TO_TRIGGER.items()}


class PageMouse(Page):
    def __init__(self, *args):
        super().__init__(*args)
        self.tree = Tree(self)
        self.tree.itemSelectionChanged.connect(self._treeSelectionChanged)
        self.actionBox = ActionBox(self.core)
        self.actionBox.addItem("")
        self.actionBox.populate()
        self.actionBox.setEnabled(False)
        self.actionBox.activated.connect(self._boxActivated)

        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(Wheel(self), 0, 0, 1, 4)
        layout.addWidget(QLabel("<b>Mouse events</b>"), 2, 0, 1, 4)
        layout.addWidget(self.tree, 3, 0, 1, 4)
        layout.addWidget(QLabel("Action"), 4, 0, 1, 1)
        layout.addWidget(self.actionBox, 4, 1, 1, 3)

    def _boxActivated(self):
        """Updates current tree item from combo box text, save changes"""
        actionLabel = self.actionBox.currentText()
        self.tree.setSelectedItem(actionLabel)
        self.tree.save()

    def _treeSelectionChanged(self):
        """Updates combo box text from tree selection"""
        item = self.tree.currentItem()
        hasParents = bool(item.parent())
        if hasParents:
            key = TRIGGER_TO_KEY[item.parent().text(0)]
            enabled = bool(key != "tray")
            self.actionBox.noteActionsSetEnabled(enabled)
        self.actionBox.setCurrentText(item.text(1))
        self.actionBox.setEnabled(hasParents)


class Wheel(QtWidgets.QGroupBox):
    def __init__(self, parent):
        super().__init__("Mouse wheel threshold (sensitivity)", parent)
        slider = QtWidgets.QSlider()
        slider.setMinimum(1)
        slider.setMaximum(100)
        slider.setSingleStep(10)
        slider.setInvertedAppearance(True)
        slider.setInvertedControls(True)
        slider.setOrientation(QtCore.Qt.Horizontal)

        spinBox = AutoSpinBox(parent.db, ("general", "wheel threshold"))
        spinBox.setMinimum(1)
        spinBox.setMaximum(100)
        spinBox.valueChanged.connect(slider.setValue)
        slider.setValue(spinBox.value())
        slider.valueChanged.connect(spinBox.setValue)

        self.setToolTip("Adjust mouse sensitivity to trigger wheel up/down events")
        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(slider)
        layout.addWidget(spinBox)


class Tree(ActionTree):
    def __init__(self, parent):
        super().__init__(parent)
        self.header().setDefaultSectionSize(145)
        self.header().setMinimumSectionSize(145)
        self.setHeaderLabels(["Event", "Action"])
        self.setToolTip("Select a trigger in the tree to edit its action")
        self._populate()

    def save(self):
        """Save current tree structure to settings database"""
        mouseEvents = {}
        for item in self.iterate():
            source = TRIGGER_TO_KEY[item.text(0)]
            mouseEvents[source] = {}

            for i in range(item.childCount()):
                subItem = item.child(i)
                event = TRIGGER_TO_KEY[subItem.text(0)]
                mouseEvents[source][event] = []

                if subItem.text(1):
                    action = self.labelToAction(subItem.text(1))
                    mouseEvents[source][event] = [action.type, action.key]
        self.db["mouse events"] = mouseEvents

    def setSelectedItem(self, actionLabel: str):
        """Updates current tree item from combo box text"""
        item = self.currentItem()
        if actionLabel:
            action = self.labelToAction(actionLabel)
            item.setText(1, actionLabel)
            item.setIcon(1, action.icon)
        else:
            item.setText(1, "")
            item.setIcon(1, QtGui.QIcon())

    def _populate(self):
        """Parses database keys to generate QTreeWidget items"""
        noteActions = NoteSetup.actionsFromMode(self.core)
        coreActions = self.core.actions.tray
        for source, actions in self.db["mouse events"].items():
            item = QtWidgets.QTreeWidgetItem()
            item.setText(0, KEY_TO_TRIGGER[source])
            for event, command in actions.items():
                subItem = QtWidgets.QTreeWidgetItem()
                subItem.setText(0, KEY_TO_TRIGGER[event])
                if command:
                    type_, key = command
                    action = noteActions[key] if type_ == "note" else coreActions[key]
                    subItem.setIcon(1, action.icon)
                    subItem.setText(1, f"{action.label} ({type_})")
                item.addChild(subItem)
            self.addTopLevelItem(item)
        self.resizeColumnToContents(0)
        self.expandAll()
