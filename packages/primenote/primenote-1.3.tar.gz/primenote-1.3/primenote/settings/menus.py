#!/usr/bin/python3
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel, QSizePolicy, QSpacerItem

try:
    from ..notes import NoteSetup
    from ..settings.base import Page, MODE_TO_KEY, KEY_TO_MODE
except (ValueError, ImportError):
    from notes import NoteSetup
    from settings.base import Page, MODE_TO_KEY, KEY_TO_MODE


class PageMenu(Page):
    def __init__(self, core, db: dict):
        super().__init__(core, db)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setVerticalStretch(1)
        self.availableList = self.AvailablesList()
        self.availableList.setSizePolicy(sizePolicy)
        self.availableList.setIconSize(QtCore.QSize(16, 16))
        self.availableList.setToolTip("Drag an item from the available to the selected elements")

        self.selectedList = self.SelectedList()
        self.selectedList.setIconSize(QtCore.QSize(16, 16))
        self.selectedList.dropped.connect(self._save)
        self.selectedList.setToolTip(
            "Drag and drop an item inside of the selected elements\n"
            "to change its position, drop it outside to delete it"
        )

        self.setAcceptDrops(True)  # Act as a drop dump to discard item from selected list
        self._layout()

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent):
        event.setDropAction(QtCore.Qt.MoveAction)
        event.accept()

    def dropEvent(self, event: QtGui.QDropEvent):
        """Accepts drops so the whole widget act as a drop dump"""
        if event.source() is self.selectedList:
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
            QtCore.QTimer.singleShot(0, self._save)  # Wait for the item to be deleted

    def populate(self):
        """Parses availables actions/database keys to generate QListWidget items"""
        self.availableList.clear()
        for key, action in sorted(self.actions.items()):
            item = self._item(key, action)
            self.availableList.addItem(item)

        self.selectedList.clear()
        for key in self.menus[self.index]:
            action = self.actions[key]
            item = self._item(key, action)
            self.selectedList.addItem(item)

    def _item(self, key: str, action: object) -> QtWidgets.QListWidgetItem:
        """Converts a key/action pair to a QListWidgetItem"""
        item = QtWidgets.QListWidgetItem()
        item.setText(action.label)
        item.setIcon(action.icon)
        item.setData(QtCore.Qt.UserRole, key)
        return item

    def _layout(self):
        """Setups the page layout"""
        frame = QtWidgets.QWidget()
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        label = QtWidgets.QLabel("Current menu :  ", frame)
        label.setSizePolicy(sizePolicy)
        self.menuBox = QtWidgets.QComboBox(frame)
        self.menuBox.setToolTip("Select a menu to edit")

        menuLayout = QtWidgets.QHBoxLayout(frame)
        menuLayout.setContentsMargins(0, 0, 0, 0)
        menuLayout.addWidget(label)
        menuLayout.addWidget(self.menuBox)

        vspacer = QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed)
        hspacer = QSpacerItem(5, 0, QSizePolicy.Fixed, QSizePolicy.Minimum)
        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(frame, 0, 0, 1, 3)
        layout.addWidget(QLabel("Available elements"), 2, 0, 1, 1)
        layout.addWidget(QLabel("Selected elements"), 2, 2, 1, 1)
        layout.addWidget(self.availableList, 3, 0, 2, 1)
        layout.addItem(vspacer, 1, 0, 1, 1)
        layout.addWidget(self.selectedList, 3, 2, 2, 1)
        layout.addItem(hspacer, 3, 1, 1, 1)

    def _save(self):
        """Save selected list widget content to settings database"""
        selectedList = self.selectedList
        itemsCount = selectedList.count()
        items = [selectedList.item(i).data(QtCore.Qt.UserRole) for i in range(itemsCount)]
        self.menus[self.index] = items

    class AvailablesList(QtWidgets.QListWidget):
        def __init__(self):
            super().__init__()
            self.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)

    class SelectedList(QtWidgets.QListWidget):
        dropped = QtCore.pyqtSignal()

        def __init__(self):
            super().__init__()
            self.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
            self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        def dropEvent(self, event: QtGui.QDropEvent):
            """Accepts dropped items"""
            event.setDropAction(QtCore.Qt.MoveAction)
            super().dropEvent(event)
            self.dropped.emit()


class PageCoreMenu(PageMenu):
    def __init__(self, *args):
        super().__init__(*args)
        self.menuBox.addItems(["Tray", "Browser"])
        self.menuBox.currentTextChanged.connect(self.setMenu)
        self.setMenu("tray")

    def setMenu(self, menu: str):
        """Updates QListWidget content as the QComboBox content is changed"""
        menu = menu.lower()
        self.menus, self.index = self.db["core menus"], menu
        self.actions = self.core.actions.tray if menu == "tray" else self.core.actions.browser
        self.populate()


class PageNoteMenu(PageMenu):
    def __init__(self, *args):
        super().__init__(*args)
        current = self.db["profile default"]["mode"]
        current = KEY_TO_MODE[current]
        self.menuBox.addItems([menu for menu in MODE_TO_KEY])
        self.menuBox.setCurrentText(current)
        self.menuBox.currentTextChanged.connect(self.setMenu)
        self.setMenu(current)

    def setMenu(self, menu: str):
        """Updates QListWidget content as the QComboBox content is changed"""
        mode = MODE_TO_KEY[menu]
        self.menus, self.index = self.db[self.key], mode
        self.actions = NoteSetup.actionsFromMode(self.core, mode)
        self.populate()


class PageNoteContextMenu(PageNoteMenu):
    def __init__(self, *args):
        self.key = "context menus"
        super().__init__(*args)


class PageNoteToolbarMenu(PageNoteMenu):
    def __init__(self, *args):
        self.key = "toolbar menus"
        super().__init__(*args)
