#!/usr/bin/python3
from pathlib import Path
from typing import Tuple
from PyQt5 import QtCore, QtWidgets

try:
    from ..backend import UserDirs, Tuples, logger, DESKTOP_ENVIRONMENT
except (ValueError, ImportError):
    from backend import UserDirs, Tuples, logger, DESKTOP_ENVIRONMENT

log = logger.new(__name__)


class ConfirmPrompt(QtWidgets.QMessageBox):
    def __init__(self, title: str, msg: str):
        super().__init__()
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setStandardButtons(self.Yes | self.No)
        self.setDefaultButton(self.No)
        self.setIcon(self.Warning)
        self.setWindowTitle(title)
        self.setText(msg)


def sortQActions(data: list) -> list:
    """Sorts a list of QMenus or QActions"""
    try:
        return sorted(data, key=lambda item: item.title().lower())
    except AttributeError:
        return sorted(data, key=lambda item: item.text().lower())


class AbstractNoteAction(QtWidgets.QAction):
    def __init__(self, parent: QtWidgets.QMenu, path: Path):
        super().__init__(parent)
        self.core = parent.core
        self.path = path
        self.setCheckable(True)
        self.triggered.connect(self._triggered)
        self._setIcon()

    def truncate(self, label: str) -> str:
        """Truncates label if longer than threshold value"""
        threshold = self.core.sdb["general"]["truncate threshold"]
        if len(label) > threshold:
            return f"{label[:threshold - 4]} ..."
        return label

    def _setIcon(self):
        """Sets an icon according to note type"""
        nid = str(self.path.relative_to(UserDirs.NOTES))
        try:
            mode = self.core.pdb[nid]["mode"]
            prefix = mode if mode in ("console", "html", "image") else "plain"
        except KeyError:
            prefix = "image" if self.path.suffix == ".png" else "plain"

        favorites = self.core.ndb["favorites"]
        suffix = "starred" if nid in favorites else "regular"
        icon = self.core.icons[f"{prefix}_{suffix}"]
        self.setIcon(icon)


class CoreAction(QtWidgets.QAction):
    def __init__(self, core, action: Tuples.Action, path: Path = None):
        super().__init__(core)
        self.path = path
        self.action = action
        self.setIcon(action.icon)
        self.setText(action.label)
        self.triggered.connect(self._triggered)

    def _triggered(self):
        """Handles left click event, calls an action"""
        if self.path:
            log.info(f"Core : {self.action.label} : {self.path}")
            self.action.call(self.path)
        else:
            log.info(f"Core : {self.action.label}")
            self.action.call()


class CoreMenu(QtWidgets.QMenu):
    def __init__(self, core):
        super().__init__()
        self.core = core
        self.icons = core.icons
        self.aboutToShow.connect(self._refresh)

        # Preload menu to prevent odd appearance and others problems
        if DESKTOP_ENVIRONMENT in ("cinnamon", "xfce"):
            self.popup(QtCore.QPoint(0, 0))
            self.hide()

    def addFoldersList(self):
        """Adds root level folders top menus"""
        folders = [f for f in UserDirs.NOTES.iterdir() if f.is_dir()]
        folders = [SubMenu(self, f) for f in folders]
        for f in sortQActions(folders):
            self.addMenu(f)

    def addNotesList(self):
        """Inserts QActions for locals (root) and loaded sub-notes"""

        def hasParents(path: Path) -> bool:
            """Verifies if a note is located at the root of the notes directory"""
            parents = path.relative_to(UserDirs.NOTES)
            return bool(parents.parts[:-1])

        notes = [self.RootNoteAction(self, f) for f in UserDirs.NOTES.iterdir() if f.is_note()]
        for item in sortQActions(notes):
            self.addAction(item)

        subnotes = [self.RootNoteAction(self, f) for f in self.core.loaded if hasParents(f)]
        for item in sortQActions(subnotes):
            self.addAction(item)

        if not notes and not subnotes:
            item = QtWidgets.QAction(self)
            item.setText("Note folder is empty")
            item.setEnabled(False)
            self.addAction(item)

    def _refresh(self):
        """Updates core menu on request"""
        self.clear()
        for key in self.core.sdb["core menus"]["tray"]:
            if key == "separator":
                self.addSeparator()
            elif key == "folders list":
                self.addFoldersList()
            elif key == "notes list":
                self.addNotesList()
            else:
                action = self.core.actions.tray[key]
                action = CoreAction(self.core, action)
                self.addAction(action)

    class RootNoteAction(AbstractNoteAction):
        def __init__(self, parent: QtWidgets.QMenu, path: Path):
            super().__init__(parent, path)
            if self.path in self.core.loaded:
                isVisible = self.core.loaded[path].isVisible()
                self.setChecked(isVisible)

            label = self.path.stem
            if self.path.is_nested():
                label = self._shortPath(label)
            self.setText(self.truncate(label))

        def _shortPath(self, stem: str) -> str:
            """Abbreviates folder paths when a label exceed truncation threshold"""
            threshold = self.core.sdb["general"]["truncate threshold"]
            parts = self.path.relative_to(UserDirs.NOTES).parts
            label = " / ".join(parts[:-1]) + f" / {stem}"
            if len(label) > threshold:
                label = f"{parts[0]} // {stem}"
            return label

        def _triggered(self):
            """Handles left click event, toggles a note"""
            self.core.notes.toggle(self.path)


class SubMenu(QtWidgets.QMenu):
    def __init__(self, parent: QtWidgets.QMenu, path: Path):
        super().__init__(parent)
        self.core = parent.core
        self.path = path
        self.setTitle(path.name)
        self.aboutToShow.connect(self._refresh)

        loaded = self._loadedCount(path)
        title = f"{path.name} ({loaded})" if loaded else f"{path.name}"
        icon = "folder_active" if loaded else "folder_inactive"
        icon = self.core.icons[icon]
        self.setTitle(title)
        self.setIcon(icon)

    def _addSubActions(self, actions: Tuple):
        """Adds core actions"""
        for key in actions:
            if key == "separator":
                self.addSeparator()
            else:
                action = self.core.actions.browser[key]
                action = CoreAction(self.core, action, self.path)
                self.addAction(action)

    def _loadedCount(self, path: Path) -> int:
        """Counts how many notes of a folder are currently loaded"""
        count = 0
        for f in self.core.loaded:
            if f.is_relative_to(self.path):
                count += 1
        return count

    def _refresh(self):
        """Updates sub-menus on request"""
        self.clear()
        folders = [f for f in self.path.iterdir() if f.is_dir()]
        folders = [SubMenu(self, f) for f in folders]
        for menu in sortQActions(folders):
            self.addMenu(menu)

        files = [f for f in self.path.iterdir() if f.is_note()]
        files = [self.SubNoteAction(self, f) for f in files]
        for note in sortQActions(files):
            self.addAction(note)

        if files or folders:
            actions = self.core.sdb["core menus"]["browser"]
        else:
            actions = ("new", "rename", "move", "open", "separator", "delete")
        self._addSubActions(actions)

    class SubNoteAction(AbstractNoteAction):
        def __init__(self, parent: QtWidgets.QMenu, path: Path):
            super().__init__(parent, path)
            self.setChecked(self.path in self.core.loaded)
            self.setText(self.truncate(path.stem))

        def _triggered(self):
            """Handles left click event, toggles a sub-note"""
            if self.path in self.core.loaded:
                self.core.loaded[self.path].close()
            else:
                self.core.notes.add(self.path)
