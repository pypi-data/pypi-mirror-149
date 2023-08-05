#!/usr/bin/python3
import ctypes
import re
import sys
from cryptography.fernet import InvalidToken
from pathlib import Path
from typing import Iterable
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QLabel, QSizePolicy, QSpacerItem

try:
    from ..__id__ import APP_NAME, ID
    from ..backend import UserFiles, UserDirs, RootDirs, logger, sanitizeFileName
    from ..backend.database import AutoCheckBox, AutoComboBoxGlob, AutoFontComboBox, AutoSpinBox
    from ..backend.cryptography import Cipher, MasterKeyPrompt, PasswordInputDialog
    from ..settings.base import HSpacer, VSpacer, Page
except (ValueError, ImportError):
    from __id__ import APP_NAME, ID
    from backend import UserFiles, UserDirs, RootDirs, logger, sanitizeFileName
    from backend.database import AutoCheckBox, AutoComboBoxGlob, AutoFontComboBox, AutoSpinBox
    from backend.cryptography import Cipher, MasterKeyPrompt, PasswordInputDialog
    from settings.base import HSpacer, VSpacer, Page

log = logger.new(__name__)


class PageAdvanced(Page):
    def __init__(self, *args):
        super().__init__(*args)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(Terminal(self))
        layout.addWidget(Encryption(self))
        layout.addWidget(Symlink(self))
        layout.addWidget(Folder(self))
        layout.addItem(VSpacer())


class Terminal(QtWidgets.QGroupBox):
    def __init__(self, parent):
        super().__init__("Terminal", parent)
        colorSchemeBox = AutoComboBoxGlob(parent.db, ("terminal", "color scheme"), "terminal")
        fontSizeBox = AutoSpinBox(parent.db, ("terminal", "font size"))
        fontFamilyBox = AutoFontComboBox(parent.db, ("terminal", "font family"))

        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(QLabel("Colorscheme"), 0, 0, 1, 1)
        layout.addWidget(colorSchemeBox, 0, 1, 1, 2)
        layout.addWidget(QLabel("Font family"), 1, 0, 1, 1)
        layout.addWidget(fontFamilyBox, 1, 1, 1, 2)
        layout.addWidget(QLabel("Font size"), 2, 0, 1, 1)
        layout.addWidget(fontSizeBox, 2, 1, 1, 1)
        layout.addItem(HSpacer(), 2, 2, 1, 1)


class Encryption(QtWidgets.QGroupBox):
    def __init__(self, parent):
        super().__init__("Encryption", parent)
        self.core = parent.core
        setButton = QtWidgets.QPushButton("Set/Replace Master Key")
        setButton.clicked.connect(self._setPassword)
        encryptAllBox = AutoCheckBox("Encrypt all notes by default", parent.db, ("general", "encrypt all"))
        self.removeButton = QtWidgets.QPushButton("Remove Master Key")
        self.removeButton.clicked.connect(self._removePassword)
        self.removeButton.setEnabled(UserFiles.KEYRING.is_file())

        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(setButton, 1, 0, 1, 1)
        layout.addWidget(self.removeButton, 1, 1, 1, 1)
        layout.addWidget(encryptAllBox, 0, 0, 1, 2)

    def _findEncrypted(self) -> Iterable:
        """Iterates over text files encrypted with the master key"""
        files = [f for f in UserDirs.NOTES.rglob("*.txt") if f.is_file()]
        for path in files:
            with open(path, encoding="utf-8") as f:
                content = f.read()
            if not content and path in self.core.loaded:
                if self.core.loaded[path].key == self.core.masterKey:
                    yield path, ""
            elif content.startswith(Cipher.MAGIC):
                length = len(Cipher.MAGIC)
                token = content[length:].encode()
                try:
                    yield path, Cipher.decrypt(self.core.masterKey, token)
                except InvalidToken:
                    pass

    def _removePassword(self):
        """Removes encryption of all master key encrypted files"""
        if not self.core.masterKey:
            if MasterKeyPrompt.login(self.core):
                self._removePassword()
            return

        for path, text in self._findEncrypted():
            if path in self.core.loaded:
                self.core.loaded[path].content = text
                self.core.loaded[path].keyring.setKey(None)
            else:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(text)
            log.info(f"{path.name} : Removed encryption")
        UserFiles.KEYRING.unlink()
        self.core.masterKey = None
        self.removeButton.setEnabled(False)
        log.info(f"Removed master token '{UserFiles.KEYRING}'")

    def _replacePassword(self):
        """Replaces the password of all master key encrypted files"""
        dialog = PasswordInputDialog(
            self.core, "Master key replacement", "Please provide a new master key."
        )
        if dialog.exec_() == dialog.Accepted:
            for path, text in self._findEncrypted():
                if path in self.core.loaded:
                    self.core.loaded[path].keyring.setKey(dialog.key)
                else:
                    with open(path, "w", encoding="utf-8") as f:
                        token = Cipher.encrypt(dialog.key, text)
                        token = Cipher.MAGIC + token.decode("utf-8")
                        f.write(token)
                log.info(f"{path.name} : Replaced key")
            MasterKeyPrompt.save(self.core, dialog.key)

    def _setPassword(self):
        """Sets or replaces the master key"""
        if not UserFiles.KEYRING.is_file():
            if MasterKeyPrompt.set(self.core):
                self.removeButton.setEnabled(True)

        elif not self.core.masterKey:
            if MasterKeyPrompt.login(self.core):
                self._setPassword()

        else:
            self._replacePassword()


class Folder(QtWidgets.QGroupBox):
    def __init__(self, parent):
        super().__init__("Configuration files", parent)
        self.core = parent.core

        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        button = QtWidgets.QPushButton(f"Edit {APP_NAME}\nconfiguration")
        button.setSizePolicy(sizePolicy)
        button.setFocusPolicy(QtCore.Qt.NoFocus)
        button.clicked.connect(self._clicked)

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        label = QLabel("Manually edit CSS, Vim and\nQTermWidget configuration files")
        label.setSizePolicy(sizePolicy)
        label.setWordWrap(True)

        spacer = QSpacerItem(5, 0, QSizePolicy.Fixed, QSizePolicy.Maximum)
        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(label)
        layout.addItem(spacer)
        layout.addWidget(button)

    def _clicked(self):
        self.core.fileManager(UserDirs.CONFIG / "ui")


class Symlink(QtWidgets.QGroupBox):
    def __init__(self, parent):
        super().__init__("Symbolic links", parent)
        self.core = parent.core

        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        button = QtWidgets.QPushButton("Create symbolic\nlinks (symlinks)")
        button.setSizePolicy(sizePolicy)
        button.setFocusPolicy(QtCore.Qt.NoFocus)
        button.clicked.connect(self._clicked)
        button.setToolTip("Add new symbolic links to the notes repository")

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        label = QLabel(
            "This utility helps to create symbolic links and add them into the note repository. "
            "Use this tool to link a directory into the repository (ie. cloud storage drive)."
        )
        label.setSizePolicy(sizePolicy)
        label.setWordWrap(True)

        spacer = QSpacerItem(5, 0, QSizePolicy.Fixed, QSizePolicy.Maximum)
        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(label)
        layout.addItem(spacer)
        layout.addWidget(button)

    def _clicked(self):
        SymlinkDialog().exec()


class SymlinkDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        icon = QtGui.QIcon(str(RootDirs.ICONS / f"{ID}_settings.svg"))
        self.resize(420, 1)
        self.setWindowTitle("Symlinks Creation Utility")
        self.setWindowIcon(icon)

        self.browseButton = QtWidgets.QPushButton("Browse")
        self.browseButton.clicked.connect(self._browse)
        self.createButton = QtWidgets.QPushButton("Create symlink")
        self.createButton.clicked.connect(self._createSymlink)
        self.createButton.setEnabled(False)

        self.msgLabel = QLabel()
        self.targetLine = QtWidgets.QLineEdit()
        self.destLine = QtWidgets.QLineEdit()
        self.targetLine.textChanged.connect(self._nameChanged)
        self.destLine.textChanged.connect(self._nameChanged)

        buttonBox = QtWidgets.QDialogButtonBox()
        buttonBox.setStandardButtons(buttonBox.Close)
        buttonBox.rejected.connect(self.close)

        spacer = QSpacerItem(0, 10, QSizePolicy.Maximum, QSizePolicy.Fixed)
        gridLayout = QtWidgets.QGridLayout(self)
        gridLayout.addWidget(QLabel("Target"), 0, 0, 1, 1)
        gridLayout.addWidget(self.targetLine, 0, 1, 1, 1)
        gridLayout.addWidget(self.browseButton, 0, 2, 1, 1)
        gridLayout.addWidget(QLabel("Name"), 1, 0, 1, 1)
        gridLayout.addWidget(self.destLine, 1, 1, 1, 1)
        gridLayout.addWidget(self.createButton, 1, 2, 1, 1)
        gridLayout.addItem(spacer, 2, 0, 1, 1)
        gridLayout.addWidget(self.msgLabel, 2, 1, 1, 1)
        gridLayout.addWidget(buttonBox, 3, 0, 1, 3)
        self.browseButton.setFocus()

    @property
    def destination(self) -> Path:
        sep = "\\" if sys.platform.startswith("win") else "/"
        name = self.destLine.text().split(sep)
        return Path(UserDirs.NOTES, *name)

    @property
    def target(self) -> Path:
        return Path(self.targetLine.text())

    def _assertSymlink(self):
        """Shows a sucess/failure message following symlink creation"""
        self._block(False)
        if self.destination.is_symlink():
            self.targetLine.clear()
            self.destLine.clear()
            self._setMessage(f"Symlink successfully created:\n{self.destination}", "black")
        else:
            self._setMessage(f"Symlink creation failed:\n{self.destination}", "red")

    def _block(self, enabled: bool):
        """Toggles interactive widgets"""
        self.targetLine.setEnabled(not enabled)
        self.destLine.setEnabled(not enabled)
        self.browseButton.setEnabled(not enabled)
        self.createButton.setEnabled(not enabled)

    def _browse(self):
        """Opens a folder selection dialog"""
        dialog = self.BrowseDialog()
        if dialog.exec_() == dialog.Accepted:
            dest = dialog.selectedFiles()[0]
            self.targetLine.setText(dest)

    def _createSymlink(self):
        """Creates a symbolic link, ask for user account control (UAC) elevation in Windows"""
        self._block(True)
        try:
            args = f'/c mklink /D "{self.destination}" "{self.target}"'
            ctypes.windll.shell32.ShellExecuteW(None, "runas", "cmd", args, None, 1)
        except AttributeError:
            self.destination.symlink_to(self.target)
        QtCore.QTimer.singleShot(1000, self._assertSymlink)

    def _isValidName(self) -> bool:
        """Compares link's name with the valid name filter used in move/rename"""
        name = re.sub(r"[\:\/\\]", "", self.destLine.text())
        return name == sanitizeFileName(self.destLine.text())

    def _nameChanged(self, text: str):
        """Updates error message on change"""
        self.createButton.setEnabled(False)

        if not self.destLine.text() or not self.targetLine.text():
            self.msgLabel.clear()

        elif not self._isValidName():
            self._setMessage("Illegal name or characters", "red")

        elif not self.target.exists():
            self._setMessage("Target directory does not exist", "red")

        elif self.destination.exists():
            self._setMessage("Destination folder already exist", "red")

        else:
            self.msgLabel.clear()
            self.createButton.setEnabled(True)

    def _setMessage(self, text: str, color: str):
        self.msgLabel.setStyleSheet(f"color: {color};")
        self.msgLabel.setText(text)

    class BrowseDialog(QtWidgets.QFileDialog):
        def __init__(self):
            super().__init__()
            home = str(Path.home())
            self.setDirectory(home)
            self.setWindowTitle("Select a target directory")
            self.setFileMode(self.Directory)
            self.setOptions(self.ShowDirsOnly)
            self.setAcceptMode(self.AcceptOpen)
            self.setModal(True)
