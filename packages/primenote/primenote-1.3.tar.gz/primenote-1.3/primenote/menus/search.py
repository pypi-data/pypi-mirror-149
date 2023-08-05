#!/usr/bin/python3
import re
from pathlib import Path
from typing import Callable, Iterable, Union
from PyQt5 import QtCore, QtGui, QtWidgets

try:
    from ..__id__ import APP_NAME
    from ..backend import UserDirs, logger
except (ValueError, ImportError):
    from __id__ import APP_NAME
    from backend import UserDirs, logger

log = logger.new(__name__)


class Search(QtWidgets.QWidget):
    """Self-contained class for the 'find & replace' dialog (text modes)"""

    def __init__(self, core):
        super().__init__()
        self.core = core
        self.note = None
        self.attached = set()
        self._setupUI()

    def closeEvent(self, event: QtGui.QCloseEvent):
        self.hide()

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Escape:
                self.hide()
        return QtCore.QObject.event(obj, event)

    def hideEvent(self, event: QtGui.QHideEvent):
        self._activateNoteWindow()
        for path in self.attached.copy():
            note = self.core.loaded[path]
            self.note = note
            self._clearHighlighting()
        self.attached.clear()
        super().hideEvent(event)

    def showEvent(self, event: QtGui.QShowEvent):
        selection = self.body.textCursor().selectedText()
        self.replaceLine.clear()
        self.findLine.setText(selection)
        self.findLine.selectAll()
        self.findLine.setFocus(True)
        super().showEvent(event)

    def reattach(func: Callable) -> Callable:
        """Fallback to the next available note when the attached note becomes unavailable"""

        def wrapper(self, *args, **kwargs) -> any:
            try:
                return func(self, *args, **kwargs)
            except RuntimeError:
                self._attachNext()

        return wrapper

    def attach(self, path: Path):
        """Links the search utility with the latest shown note"""
        note = self.core.loaded[path]
        if note.mode in ("plain", "html"):
            self.note = note
            self.attached.add(path)
            self.setWindowTitle(f"Search in '{note.id}'")

    def detach(self, path: Path):
        """Removes the latest hidden note from the attached set"""
        self.attached.discard(path)
        if not self.attached:
            self.hide()

    @property
    def body(self) -> Union[QtWidgets.QTextEdit, QtWidgets.QPlainTextEdit]:
        """Returns the body object (Q_TextEdit) of the currently attached note"""
        if self.note:
            return self.note.body
        return QtWidgets.QPlainTextEdit()

    @reattach
    def find(self, *args):
        """Finds next occurence in text"""
        self._clearHighlighting()
        if not self._findNext() and self.wrapBox.isChecked():
            self.body.moveCursor(QtGui.QTextCursor.Start)
            self._findNext()

    @reattach
    def findAll(self, text: str = None):
        """Highlights all occurences in text"""
        self._clearHighlighting()
        app = self.core.app
        pos = self.body.verticalScrollBar().value()
        extraSelections = self.body.extraSelections()
        self.body.moveCursor(QtGui.QTextCursor.Start)
        while self._findNext(text):
            bg = app.palette().highlight().color().lighter(125)
            fg = app.palette().highlightedText().color().darker(125)
            extra = QtWidgets.QTextEdit.ExtraSelection()
            extra.cursor = self.body.textCursor()
            extra.format.setBackground(bg)
            extra.format.setForeground(fg)
            extraSelections.append(extra)
        self.body.setExtraSelections(extraSelections)
        self.body.verticalScrollBar().setValue(pos)
        self.body.textCursor().clearSelection()
        self._activateNoteWindow()

    @reattach
    def replace(self, *args):
        """Replaces next occurence in text"""
        matchCase = self.caseBox.isChecked()
        selection = self.body.textCursor().selectedText()
        find = self.findLine.text()
        validSelection = (selection == find) if matchCase else (selection.lower() == find.lower())
        if validSelection:
            subs = self.replaceLine.text()
            self.body.textCursor().insertText(subs)
        self.find()

    @reattach
    def replaceAll(self, *args):
        """Replaces all occurences in text"""
        find = self.findLine.text()
        subs = self.replaceLine.text()
        pos = self.body.verticalScrollBar().value()

        self.body.moveCursor(QtGui.QTextCursor.Start)
        cursor = self.body.textCursor()
        cursor.beginEditBlock()
        while self._findNext(find):
            cursor = self.body.textCursor()
            end = cursor.position()
            start = end - len(find)
            cursor.setPosition(start)
            cursor.setPosition(end, QtGui.QTextCursor.KeepAnchor)
            cursor.insertText(subs)
        cursor.endEditBlock()
        self.body.verticalScrollBar().setValue(pos)
        self.findAll(text=subs)  # Highlight the newly replaced text

    def _activateNoteWindow(self):
        """Tries to call activateWindow() on the current or previous attached note"""
        try:
            self.note.activateWindow()
        except RuntimeError:
            self._attachNext()
            self.note.activateWindow()

    def _attachNext(self):
        """Attaches the next available note to the search utility"""
        while self.attached:
            try:
                path = self.attached.pop()
                note = self.core.loaded[path]
                if note.isVisible():
                    self.attach(path)
                    break
            except (KeyError, RuntimeError):
                pass
        else:
            self.hide()

    @reattach
    def _clearHighlighting(self):
        """Removes all highlighting of the current body object"""
        extraSelections = self.body.extraSelections()
        extraSelections.clear()
        self.body.setExtraSelections(extraSelections)

    @reattach
    def _findNext(self, text: str = None) -> bool:
        """Returns the next occurence matching the selected search flags"""
        text = self.findLine.text() if not text else text
        flags = QtGui.QTextDocument.FindFlags()
        flags = flags | QtGui.QTextDocument.FindCaseSensitively if self.caseBox.isChecked() else flags
        flags = flags | QtGui.QTextDocument.FindWholeWords if self.wholeBox.isChecked() else flags
        return self.body.find(text, flags)

    def _setupUI(self):
        self.findLine = QtWidgets.QLineEdit()
        self.findButton = QtWidgets.QPushButton("Find next")
        self.findAllButton = QtWidgets.QPushButton("Find all")
        self.replaceLine = QtWidgets.QLineEdit()
        self.replaceButton = QtWidgets.QPushButton("Replace")
        self.replaceAllButton = QtWidgets.QPushButton("Replace all")
        self.wholeBox = QtWidgets.QCheckBox("Whole Words")
        self.caseBox = QtWidgets.QCheckBox("Match Case")
        self.wrapBox = QtWidgets.QCheckBox("Wrap Search")

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.addWidget(self.caseBox)
        self.horizontalLayout.addWidget(self.wholeBox)
        self.horizontalLayout.addWidget(self.wrapBox)

        self.layout = QtWidgets.QGridLayout()
        self.layout.addWidget(self.findLine, 0, 0, 1, 1)
        self.layout.addWidget(self.replaceLine, 1, 0, 1, 1)
        self.layout.addWidget(self.findButton, 0, 1, 1, 1)
        self.layout.addWidget(self.replaceButton, 1, 1, 1, 1)
        self.layout.addWidget(self.findAllButton, 0, 2, 1, 1)
        self.layout.addWidget(self.replaceAllButton, 1, 2, 1, 1)
        self.layout.addLayout(self.horizontalLayout, 2, 0, 1, 3)
        self.setLayout(self.layout)

        self.findLine.setTextMargins(5, 1, 5, 1)
        self.replaceLine.setTextMargins(5, 1, 5, 1)
        self.findLine.setPlaceholderText("Search ...")
        self.replaceLine.setPlaceholderText("Replace with ...")
        self.wrapBox.setChecked(True)

        self.findLine.returnPressed.connect(self.findButton.click)
        self.replaceLine.returnPressed.connect(self.replaceButton.click)
        self.findButton.clicked.connect(self.find)
        self.findAllButton.clicked.connect(lambda: self.findAll())
        self.replaceButton.clicked.connect(self.replace)
        self.replaceAllButton.clicked.connect(self.replaceAll)

        self.installEventFilter(self)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.resize(420, 100)


class Launcher(QtWidgets.QWidget):
    """Main class for the notes repository search utility"""

    def __init__(self, core):
        super().__init__()
        self.core = core
        self.timer = QtCore.QTimer(interval=500, singleShot=True)
        self.timer.timeout.connect(self.update)
        self.worker = WorkerThread()
        self.workerThread = QtCore.QThread()
        self.worker.moveToThread(self.workerThread)
        self.worker.addItem.connect(self._addItem)
        self.workerThread.start()
        self._setupUI()

    def activate(self, item: QtWidgets.QTreeWidgetItem):
        """Loads the selected note"""
        path = UserDirs.NOTES / item.text(0)
        if not path.is_file():
            log.error(f"File not found '{path}'")
            return
        try:
            note = self.core.loaded[path]
            note.show()
            note.activateWindow()
        except KeyError:
            self.core.notes.add(path)

        if self.hideBox.isChecked():
            self.hide()

    def closeEvent(self, event: QtGui.QCloseEvent):
        self.hide()

    def showEvent(self, event: QtGui.QShowEvent):
        self._moveToCenter()
        self.lineEdit.setFocus(True)
        self.lineEdit.selectAll()
        super().showEvent(event)

    def update(self):
        """Initiates a new search"""
        pattern = self.lineEdit.text()
        if pattern:
            self.listWidget.clear()
            pattern = QtCore.Q_ARG(str, pattern)
            case = QtCore.Q_ARG(bool, self.caseBox.isChecked())
            QtCore.QMetaObject.invokeMethod(
                self.worker, "search", QtCore.Qt.QueuedConnection, pattern, case
            )

    def _addItem(self, path: str, hits: str, icon: str):
        """Appends the items to tree as they are ready"""
        icon = self.core.icons[icon]
        item = TreeWidgetItem(path, hits, icon)
        self.listWidget.addTopLevelItem(item)

    def _moveToCenter(self):
        """Place widget at the center of the screen"""
        rect = self.core.screen()
        pos = self.frameGeometry()
        pos.moveCenter(rect.center())
        self.move(pos.x(), pos.y())

    def _setupUI(self):
        self.lineEdit = LineEdit(self.core)
        self.listWidget = TreeWidget(self)
        self.caseBox = Checkbox(self.core, "case", "Match Case")
        self.hideBox = Checkbox(self.core, "hide", "Hide on launch")
        self.caseBox.setFocusPolicy(QtCore.Qt.NoFocus)

        self.lineEdit.hide.connect(self.hide)
        self.lineEdit.focusTreeBottom.connect(self.listWidget.focusBottom)
        self.lineEdit.focusTreeTop.connect(self.listWidget.focusTop)
        self.lineEdit.search.connect(self.update)
        self.lineEdit.textChanged.connect(self.timer.start)
        self.listWidget.activate.connect(self.activate)
        self.listWidget.hide.connect(self.hide)
        self.listWidget.focusLine.connect(self.lineEdit.setFocus)
        self.caseBox.stateChanged.connect(self.update)

        self.layout = QtWidgets.QGridLayout()
        self.layout.addWidget(self.lineEdit, 0, 0, 1, 4)
        self.layout.addWidget(self.listWidget, 1, 0, 1, 4)
        self.layout.addWidget(self.caseBox, 2, 0, 1, 1)
        self.layout.addWidget(self.hideBox, 2, 1, 1, 1)
        self.setLayout(self.layout)

        self.setWindowTitle(f"{APP_NAME} — Search")
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.resize(450, 250)


class LineEdit(QtWidgets.QLineEdit):
    focusTreeTop = QtCore.pyqtSignal()
    focusTreeBottom = QtCore.pyqtSignal()
    hide = QtCore.pyqtSignal()
    search = QtCore.pyqtSignal()

    def __init__(self, core):
        super().__init__()
        self.setTextMargins(5, 2, 5, 2)
        self.setPlaceholderText("Search for a note ...")

        icon = core.icons["search"]
        self.action = QtWidgets.QAction(icon, "Search")
        self.action.triggered.connect(self.search.emit)
        self.addAction(self.action, QtWidgets.QLineEdit.TrailingPosition)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
            self.search.emit()

        elif event.key() == QtCore.Qt.Key_Escape:
            self.hide.emit()

        elif event.key() == QtCore.Qt.Key_Up:
            self.focusTreeBottom.emit()

        elif event.key() == QtCore.Qt.Key_Down:
            self.focusTreeTop.emit()

        super().keyPressEvent(event)


class TreeWidget(QtWidgets.QTreeWidget):
    activate = QtCore.pyqtSignal(QtWidgets.QTreeWidgetItem)
    focusLine = QtCore.pyqtSignal(bool)
    hide = QtCore.pyqtSignal()

    def __init__(self, launcher):
        super().__init__()
        self.launcher = launcher
        self.itemDoubleClicked.connect(self.activate.emit)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.setIndentation(5)

        self.setHeaderLabels(["path", "hits"])
        self.setColumnWidth(1, 0)  # Minimizes hits column
        self.sortItems(1, QtCore.Qt.DescendingOrder)  # Sort by hits
        self.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.header().setStretchLastSection(False)  # Minimizes hits column
        self.header().hide()

    def focusBottom(self):
        """Selects the last item of the tree"""
        last = self.topLevelItem(self.topLevelItemCount() - 1)
        self.setCurrentItem(last)
        self.setFocus(True)

    def focusTop(self):
        """Selects the first item of the tree"""
        first = self.topLevelItem(0)
        self.setCurrentItem(first)
        self.setFocus(True)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
            self.activate.emit(self.currentItem())

        elif event.key() == QtCore.Qt.Key_Escape:
            self.hide.emit()

        elif event.key() == QtCore.Qt.Key_Up:
            if self.currentIndex().row() == 0:
                self.focusBottom()
                event.ignore()

        elif event.key() == QtCore.Qt.Key_Down:
            if self.currentIndex().row() == self.topLevelItemCount() - 1:
                self.focusTop()
                event.ignore()
        else:
            self._postKeyEvent(event)
            self.focusLine.emit(True)

        if event.isAccepted():
            super().keyPressEvent(event)

    def _postKeyEvent(self, event: QtGui.QKeyEvent):
        """Forwards key events to the LineEdit widget"""
        try:
            sequence = QtGui.QKeySequence(event.key())
            sequence = sequence.toString().lower()
            sequence = sequence.replace("space", " ")
            sequence.encode("utf-8")
        except UnicodeEncodeError:
            return
        keyEvent = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, event.key(), event.modifiers(), sequence)
        QtCore.QCoreApplication.postEvent(self.launcher.lineEdit, keyEvent)


class TreeWidgetItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, path: str, hits: str, icon: QtGui.QIcon):
        super().__init__()
        self.setTextAlignment(1, QtCore.Qt.AlignCenter)
        self.setIcon(0, icon)
        self.setText(0, path)
        self.setText(1, hits)

    def __lt__(self, other: QtWidgets.QTreeWidgetItem) -> bool:
        """Sorts numbers higher than 10"""
        column = self.treeWidget().sortColumn()
        key1 = self.text(column)
        key2 = other.text(column)
        return int(key1) < int(key2)


class Checkbox(QtWidgets.QCheckBox):
    def __init__(self, core, key: str, text: str):
        super().__init__()
        self.core = core
        self.key = key
        self.setText(text)
        self.setChecked(core.sdb["launcher"][key])
        self.stateChanged.connect(self._stateChanged)

    def _stateChanged(self, state: int):
        state = not (state == QtCore.Qt.Unchecked)
        self.core.sdb["launcher"][self.key] = state


class WorkerThread(QtCore.QObject):
    addItem = QtCore.pyqtSignal(str, str, str)

    def __init__(self):
        super().__init__()

    @QtCore.pyqtSlot(str, bool)
    def search(self, pattern: str, case: bool):
        """Returns all files that match a text pattern"""
        for path, hits in FileSearch.seekContent(UserDirs.NOTES, pattern, case):
            self.addItem.emit(str(path), str(hits), "plain_regular")

        for path, hits in FileSearch.seekFileName(UserDirs.NOTES, pattern, case):
            self.addItem.emit(str(path), str(hits), "rename")


class FileSearch:
    @classmethod
    def seekContent(cls, src: Path, pattern: str, exact=False) -> Iterable:
        """Searches notes directory for matching content"""
        for path in [f for f in src.rglob("*.txt") if f.is_file()]:
            content = cls._toPlainText(path) if cls._isHtml(path) else cls._read(path)
            hits = content.count(pattern) if exact else cls._lazyCount(content, pattern)
            if hits:
                yield path.relative_to(src), hits

    @classmethod
    def seekFileName(cls, src: Path, pattern: str, exact=False) -> Iterable:
        """Searches notes directory for matching filename"""
        for path in [f.relative_to(src) for f in src.rglob("*.txt") if f.is_file()]:
            hits = path.stem.count(pattern) if exact else cls._lazyCount(path.stem, pattern)
            if hits:
                yield path, hits

    def _isHtml(path: Path) -> bool:
        """Verifies if the note file has HTML content"""
        with open(path, encoding="utf8") as f:
            first = f.readline()
        return first.startswith("<!DOCTYPE HTML")

    def _lazyCount(content: str, pattern: str) -> int:
        """Counts all matching pattern regardless of its case"""
        found = re.findall(pattern, content, re.IGNORECASE)
        return len(found)

    def _read(path: Path) -> str:
        """Returns a file content"""
        with open(path, encoding="utf8") as f:
            return f.read()

    def _toPlainText(path: Path) -> str:
        """Extracts plain text from an HTML note"""
        with open(path, encoding="utf8") as f:
            content = f.read()
        qtext = QtWidgets.QTextEdit()
        qtext.setHtml(content)
        return qtext.toPlainText()
