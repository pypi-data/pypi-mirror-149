from copy import deepcopy
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QCheckBox

try:
    from ..__db__ import SDB_DEFAULT
    from ..settings.base import VSpacer
except (ValueError, ImportError):
    from __db__ import SDB_DEFAULT
    from settings.base import VSpacer


class ResetDialog(QtWidgets.QDialog):
    def __init__(self, core):
        super().__init__()
        self.core = core
        self.resize(1, 1)
        self.setWindowTitle("Restore to defaults")
        buttonBox = QtWidgets.QDialogButtonBox()
        buttonBox.setStandardButtons(buttonBox.Cancel | buttonBox.Ok)
        buttonBox.setCenterButtons(True)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        self.checkboxes = {}
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(Settings(self))
        layout.addItem(VSpacer())
        layout.addWidget(buttonBox)

    def isChecked(self) -> bool:
        """Returns a boolean wether any checkbox is checked"""
        for key, item in self.checkboxes.items():
            if item.isChecked():
                return True
        return False

    def resetKey(self, key: str):
        """Restores default value of a top level database key"""
        self.core.sdb[key] = deepcopy(SDB_DEFAULT[key])

        if key == "general":  # Hook for menu icon color
            css = self.core.getNoteDecorationsCSS()
            self.core.setGlobalIconsColor("menu-icon", css["menu-icon"])
            self.core.setGlobalIconsColor("tray-icon", css["tray-icon"])

        elif key == "profile default":  # Hook for default name (general settings)
            default = SDB_DEFAULT["general"]["default name"]
            self.core.sdb["general"]["default name"] = default

        elif key == "mouse events":  # Hook for wheel treshold (general settings)
            default = SDB_DEFAULT["general"]["wheel threshold"]
            self.core.sdb["general"]["wheel threshold"] = default


class Settings(QtWidgets.QGroupBox):
    def __init__(self, parent):
        super().__init__("Please confirm which settings to reset", parent)
        parent.checkboxes["general"] = QCheckBox("General")
        parent.checkboxes["message bar"] = parent.checkboxes["general"]
        parent.checkboxes["launcher"] = parent.checkboxes["general"]
        parent.checkboxes["archives"] = QCheckBox("Logs and archives")
        parent.checkboxes["clean"] = parent.checkboxes["archives"]
        parent.checkboxes["terminal"] = QCheckBox("Advanced")
        parent.checkboxes["profile default"] = QCheckBox("Profile default")
        parent.checkboxes["key events"] = QCheckBox("Hotkeys")
        parent.checkboxes["mouse events"] = QCheckBox("Mouse events")
        parent.checkboxes["core menus"] = QCheckBox("Core menus")
        parent.checkboxes["context menus"] = QCheckBox("Note context menus")
        parent.checkboxes["toolbar menus"] = QCheckBox("Note toolbars menus")

        cbs = parent.checkboxes
        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(self.AllCheckBox(cbs), 0, 0, 1, 1)
        layout.addWidget(cbs["core menus"], 0, 1, 1, 1)
        layout.addWidget(cbs["context menus"], 1, 1, 1, 1)
        layout.addWidget(cbs["general"], 1, 0, 1, 1)
        layout.addWidget(cbs["toolbar menus"], 2, 1, 1, 1)
        layout.addWidget(cbs["profile default"], 2, 0, 1, 1)
        layout.addWidget(cbs["archives"], 3, 1, 1, 1)
        layout.addWidget(cbs["key events"], 3, 0, 1, 1)
        layout.addWidget(cbs["terminal"], 4, 1, 1, 1)
        layout.addWidget(cbs["mouse events"], 4, 0, 1, 1)

    class AllCheckBox(QtWidgets.QCheckBox):
        def __init__(self, checkboxes: dict):
            super().__init__("All")
            self.checkboxes = checkboxes
            self.stateChanged.connect(self._update)

        def _update(self, state: int):
            """Propagates its own check state change to all checkboxes"""
            for key, item in self.checkboxes.items():
                item.setCheckState(state)
