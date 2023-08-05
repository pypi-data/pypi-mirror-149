#!/usr/bin/python3
import re
from collections import namedtuple
from typing import Iterator
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QSizePolicy, QSpacerItem

try:
    from ..notes import NoteSetup
except (ValueError, ImportError):
    from notes import NoteSetup

ActionID = namedtuple("ActionID", ("key", "type", "icon"))
KEY_TO_MODE = {
    "console": "Console",
    "image": "Image",
    "html": "Rich text",
    "plain": "Plain text",
    "vim": "Vim",
}
MODE_TO_KEY = {v: k for k, v in KEY_TO_MODE.items()}


class VSpacer(QSpacerItem):
    def __init__(self, height: int = 40):
        policy = QSizePolicy.Minimum, QSizePolicy.Expanding
        super().__init__(0, height, *policy)


class HSpacer(QSpacerItem):
    def __init__(self, width: int = 40):
        policy = QSizePolicy.Expanding, QSizePolicy.Minimum
        super().__init__(width, 0, *policy)


class Page(QtWidgets.QWidget):
    def __init__(self, core, db: dict):
        super().__init__()
        self.core = core
        self.db = db


class ActionBox(QtWidgets.QComboBox):
    def __init__(self, core):
        super().__init__()
        self.core = core
        self.setEditable(True)
        self.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        self.completer().setCompletionMode(QtWidgets.QCompleter.PopupCompletion)

    def noteActionsSetEnabled(self, enabled: bool):
        """Toggles enabled status of notes-only actions"""
        for i in range(self.count()):
            item = self.model().item(i)
            if enabled:
                item.setEnabled(True)
            elif item.text().endswith(" (note)"):
                item.setEnabled(False)

    def populate(self):
        """Fetch, sort and fill the combo box with all actions"""
        exclusions = ("folders list", "notes list", "separator")
        sets = {"note": NoteSetup.actionsFromMode(self.core), "core": self.core.actions.tray}
        for type_, actions in sets.items():
            actions = [f"{actions[a].label} ({type_})" for a in actions if a not in exclusions]
            self.addItems(sorted(actions))


class ActionTree(QtWidgets.QTreeWidget):
    def __init__(self, parent):
        super().__init__()
        self.core = parent.core
        self.db = parent.db
        self.setIndentation(20)
        self.setAlternatingRowColors(True)

    def iterate(self) -> Iterator[QtWidgets.QTreeWidgetItem]:
        """Iterator function for the top level items"""
        for i in range(self.topLevelItemCount()):
            yield self.topLevelItem(i)

    def labelToAction(self, text: str) -> ActionID:
        """Converts an action label into a tuple of action identifying data"""
        label, type_ = re.findall(r"(.+)\s+\((\w+)\)$", text)[0]
        for actions in (NoteSetup.actionsFromMode(self.core), self.core.actions.tray):
            for key, action in actions.items():
                if label == action.label:
                    return ActionID(key, type_, action.icon)
