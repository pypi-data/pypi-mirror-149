#!/usr/bin/python3
from copy import deepcopy
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QDialogButtonBox as QButtonBox

try:
    from ..__id__ import APP_NAME, ID
    from ..backend import RootDirs, logger
    from ..settings.general import PageGeneral
    from ..settings.profile import PageProfile
    from ..settings.mouse import PageMouse
    from ..settings.hotkeys import PageHotkeys
    from ..settings.menus import PageCoreMenu, PageNoteContextMenu, PageNoteToolbarMenu
    from ..settings.logs import PageLogs
    from ..settings.advanced import PageAdvanced
    from ..settings.reset import ResetDialog
except (ValueError, ImportError):
    from __id__ import APP_NAME, ID
    from backend import RootDirs, logger
    from settings.general import PageGeneral
    from settings.profile import PageProfile
    from settings.mouse import PageMouse
    from settings.hotkeys import PageHotkeys
    from settings.menus import PageCoreMenu, PageNoteContextMenu, PageNoteToolbarMenu
    from settings.logs import PageLogs
    from settings.advanced import PageAdvanced
    from settings.reset import ResetDialog

log = logger.new(__name__)


class Settings(QtWidgets.QDialog):
    def __init__(self, core):
        super().__init__()
        self.core = core
        self.setWindowTitle(f"{APP_NAME} Settings")
        self.resize(580, 500)

        icon = QtGui.QIcon(str(RootDirs.ICONS / f"{ID}_settings.svg"))
        self.setWindowIcon(icon)

        items = [
            "General",
            "Profile default",
            "Mouse events",
            "Hotkeys",
            "Core menus",
            "Note context menus",
            "Note toolbars menus",
            "Logs and archives",
            "Advanced",
        ]
        self.sideMenu = QtWidgets.QListWidget()
        self.sideMenu.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.sideMenu.addItems(items)
        self.sideMenu.item(0).setSelected(True)
        self.sideMenu.selectionModel().selectionChanged.connect(self.setPageIndex)
        fm = QtGui.QFontMetrics(self.sideMenu.font())
        width = int(fm.horizontalAdvance(max(items)) * 1.8)
        self.sideMenu.setMinimumWidth(width)

        self.dbCopy = deepcopy(dict(core.sdb))
        self.general = PageGeneral(core, self.dbCopy)
        self.stack = QtWidgets.QStackedWidget()
        self.stack.addWidget(self.general)
        self.stack.addWidget(PageProfile(core, self.dbCopy))
        self.stack.addWidget(PageMouse(core, self.dbCopy))
        self.stack.addWidget(PageHotkeys(core, self.dbCopy))
        self.stack.addWidget(PageCoreMenu(core, self.dbCopy))
        self.stack.addWidget(PageNoteContextMenu(core, self.dbCopy))
        self.stack.addWidget(PageNoteToolbarMenu(core, self.dbCopy))
        self.stack.addWidget(PageLogs(core, self.dbCopy))
        self.stack.addWidget(PageAdvanced(core, self.dbCopy))

        splitter = QtWidgets.QSplitter()
        splitter.setOrientation(QtCore.Qt.Horizontal)
        splitter.addWidget(self.sideMenu)
        splitter.addWidget(self.stack)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(splitter)
        layout.addWidget(self.BottomFrame(self))
        self.show()

    def accept(self):
        super().accept()
        self.apply()

    def apply(self):
        """Applies new application settings"""
        for key, color in self.general.icons.colors.items():
            new = color.name()
            old = self.general.icons.currentColor(key).name()
            if new != old:
                self.core.setGlobalIconsColor(key, new)

        self.core.sdb.update(self.dbCopy)
        log.info("New settings applied")

    def reset(self):
        """Handles restore to default dialog"""
        dialog = ResetDialog(self.core)
        if dialog.exec() and dialog.isChecked():
            self.accept()
            for key, item in dialog.checkboxes.items():
                if item.isChecked():
                    dialog.resetKey(key)
            self.core.settings()

    def setPageIndex(self):
        """Updates the stack widget according to side menu changes"""
        index = self.sideMenu.currentRow()
        self.stack.setCurrentIndex(index)

    class BottomFrame(QtWidgets.QWidget):
        def __init__(self, parent):
            super().__init__()
            self.parent = parent
            self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum))

            buttons = QButtonBox.Cancel | QButtonBox.Ok | QButtonBox.Apply | QButtonBox.RestoreDefaults
            self.buttonBox = QButtonBox()
            self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
            self.buttonBox.setStandardButtons(buttons)
            self.buttonBox.accepted.connect(parent.accept)
            self.buttonBox.rejected.connect(parent.reject)
            self.buttonBox.clicked.connect(self._clicked)

            layout = QtWidgets.QHBoxLayout(self)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(self.buttonBox)

        def _clicked(self, button: QtWidgets.QPushButton):
            """Parses clicked button type"""
            button = self.buttonBox.standardButton(button)
            if button == QButtonBox.Apply:
                self.parent.apply()
            elif button == QButtonBox.RestoreDefaults:
                self.parent.reset()
