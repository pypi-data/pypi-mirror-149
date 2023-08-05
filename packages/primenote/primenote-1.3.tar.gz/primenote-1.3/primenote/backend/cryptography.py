#!/usr/bin/python3
import base64
import secrets
from cryptography.fernet import Fernet, InvalidToken
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QCryptographicHash
from PyQt5.QtWidgets import QLabel, QSizePolicy, QSpacerItem

try:
    from ..backend import logger, UserFiles
except (ValueError, ImportError):
    from backend import logger, UserFiles

log = logger.new(__name__)


class Cipher:
    MAGIC = "<ENCRYPTED/>"

    @staticmethod
    def key(password: str) -> Fernet:
        """Creates a Fernet key from a clear text password"""
        key = password.encode()
        for x in range(256**2):
            key = QCryptographicHash.hash((key), QCryptographicHash.Sha256)
        b64 = base64.urlsafe_b64encode(key)
        return Fernet(b64)

    @staticmethod
    def decrypt(key: bytes, token: bytes) -> str:
        """Decrypts a token using a Fernet key"""
        return key.decrypt(token).decode("utf-8")

    @staticmethod
    def encrypt(key: bytes, plain: str) -> bytes:
        """Encrypts text using a Fernet key"""
        return key.encrypt(plain.encode())


class Keyring:
    def __init__(self, note):
        self.note = note
        self.core = note.core

    def hasEncryption(self) -> bool:
        """Verifies if a file begins with an encryption tag"""
        with open(self.note.path, encoding="utf-8") as f:
            return f.read().startswith(Cipher.MAGIC)

    def hasKey(self) -> bool:
        """Verifies if the file content is clear text"""
        try:
            text = self.note.body.toPlainText()
        except AttributeError:
            text = None
        text = text if text else self.note.content
        return not text.startswith(Cipher.MAGIC)

    def logout(self):
        """Resets entered creditals"""
        if not self.hasEncryption():
            return

        if self.hasKey():
            self.note.lockScreen.setEnabled(True)
            self.note.key = None
            self.note.load()
            log.info(f"{self.note.id} : Logged out")

    def remove(self):
        """Removes encryption"""
        if self.hasKey():
            self.setKey(None)
            log.info(f"{self.note.id} : Removed encryption")

    def replace(self):
        """Replaces current key"""
        if not self.hasEncryption():
            self.setUnique()
            return
        elif not self.hasKey():
            return

        dialog = PasswordInputDialog(
            self.core, "Key replacement", f"Please provide a new password for\n{self.note.id}."
        )
        if dialog.exec_() == dialog.Accepted:
            self.setKey(dialog.key)
            log.info(f"{self.note.id} : Replaced unique key")

    def setKey(self, key: Fernet):
        """Sets or removes a key, updates content and handles lock screen"""
        self.note.key = key
        self.note.save()
        self.note.load()
        self.note.encryptionLabel.update()
        try:
            if self.hasKey():
                self.note.lockScreen.setEnabled(False)
        except AttributeError:
            pass

    def setMaster(self):
        """Sets a master key"""
        # Current key is unknown
        if not self.hasKey():
            return

        # Master key is known
        elif self.core.masterKey:
            self.setKey(self.core.masterKey)
            log.info(f"{self.note.id} : Encrypted with master key")

        # Master key exist but is unknown
        elif UserFiles.KEYRING.is_file():
            MasterKeyPrompt.login(self.core)

        # Master key do not exist yet
        else:
            if MasterKeyPrompt.set(self.core):
                self.setMaster()

    def setUnique(self):
        """Sets a unique key"""
        if not self.hasKey():
            return

        dialog = PasswordInputDialog(
            self.core, "Encrypt with a unique key", f"Please provide a new password for\n{self.note.id}."
        )
        if dialog.exec_() == dialog.Accepted:
            self.setKey(dialog.key)
            log.info(f"{self.note.id} : Encrypted with unique key")


class MasterKeyPrompt:
    @staticmethod
    def login(core) -> bool:
        """Shows a login prompt for master password"""
        dialog = MasterPasswordInputDialog(core, "Master Password", "Please provide the master password.")
        if dialog.exec_() == dialog.Accepted:
            core.masterKey = dialog.key
            log.info("Valid master key entered")
            return True
        else:
            log.warning("No master password provided")
            return False

    @staticmethod
    def save(core, key: Fernet):
        """Creates a file containing the new master key"""
        core.masterKey = key
        token = Cipher.encrypt(key, secrets.token_hex(16))
        with open(UserFiles.KEYRING, "w", encoding="utf-8") as f:
            f.write(token.decode("utf-8"))
        log.info(f"Master token created in '{UserFiles.KEYRING}'")

    @classmethod
    def set(cls, core) -> bool:
        """Shows a prompt to set a new master key"""
        dialog = PasswordInputDialog(
            core, "Set the master key", "Please provide a password for the master key."
        )
        if dialog.exec_() == dialog.Accepted:
            cls.save(core, dialog.key)
            return True
        return False


class PasswordLine(QtWidgets.QLineEdit):
    def __init__(self, core):
        super().__init__()
        self.setObjectName("lockscreen-input")
        self.setEchoMode(self.Password)
        self.setTextMargins(5, 2, 5, 2)
        self.setAutoFillBackground(True)
        self.setFocus(True)
        self.textChanged.connect(lambda: self.setErrorPalette(False))

        icon = core.icons["style"]
        passwordRevealAction = QtWidgets.QAction(icon, "Show password", self)
        self.addAction(passwordRevealAction, self.TrailingPosition)
        eyeButton = self.findChild(QtWidgets.QAbstractButton)
        eyeButton.pressed.connect(self._showPassword)
        eyeButton.released.connect(self._hidePassword)

    def setErrorPalette(self, enabled: bool):
        """Colorizes password input/confirmation fields"""
        enabled = "true" if enabled else "false"
        self.setProperty("error", enabled)
        self.style().polish(self)

    def _hidePassword(self):
        self.setEchoMode(self.Password)

    def _showPassword(self):
        self.setEchoMode(self.Normal)


class LockScreen(QtWidgets.QWidget):
    def __init__(self, note):
        super().__init__()
        self.setObjectName("lockscreen")
        self.note = note
        self.passwordLine = PasswordLine(note.core)
        self.passwordLine.returnPressed.connect(self._validate)

        frame = QtWidgets.QWidget()
        frame.setObjectName("lockscreen-frame")
        label = QLabel("The content of this file is encrypted. Please provide the key to continue.")
        label.setObjectName("lockscreen-label")
        label.setWordWrap(True)
        label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        innerLayout = QtWidgets.QVBoxLayout(frame)
        innerLayout.addWidget(label)
        innerLayout.addWidget(self.passwordLine)

        layout = QtWidgets.QGridLayout(self)
        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding), 0, 1, 1, 1)
        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum), 1, 0, 1, 1)
        layout.addWidget(frame, 1, 1, 1, 1)
        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum), 1, 2, 1, 1)
        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding), 2, 1, 1, 1)
        self.setAutoFillBackground(True)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(note.menuTool)
        self.hide()

    def focusInEvent(self, event):
        """Forwards focus event to Note"""
        self.note.focusInEvent(event)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        """Forwards focus event to Note"""
        self.note.focusOutEvent(event)
        super().focusOutEvent(event)

    def paintEvent(self, event):
        """Provides stylesheet support for QWidget subclasses
        https://stackoverflow.com/a/18344643/4586648"""
        style = QtWidgets.QStyle.PE_Widget
        opt = QtWidgets.QStyleOption()
        opt.initFrom(self)
        painter = QtGui.QPainter(self)
        self.style().drawPrimitive(style, opt, painter, self)
        super().paintEvent(event)

    def setEnabled(self, enabled: bool):
        """Turns the lock screen on or off"""
        self.note.body.setVisible(not enabled)
        self.note.toolbarFrame.setVisible(not enabled)
        self.note.msgbarFrame.setVisible(not enabled)
        self.note.showOuterFrames()
        self.setVisible(enabled)
        self.passwordLine.clear()

    def _validate(self):
        """Saves the key if its valid else throw an error"""
        key = Cipher.key(self.passwordLine.text())
        try:
            with open(self.note.path, encoding="utf-8") as f:
                length = len(Cipher.MAGIC)
                token = f.read()[length:]
            Cipher.decrypt(key, token.encode())
            self.note.key = key
            self.note.load()
            self.setEnabled(False)
            log.info(f"{self.note.id} : Valid password provided")
        except InvalidToken:
            self.passwordLine.setErrorPalette(True)
            log.error(f"{self.note.id} : Invalid password")


class PasswordInputDialog(QtWidgets.QDialog):
    def __init__(self, core, title: str, label: str):
        super().__init__()
        self.passwordLine = PasswordLine(core)
        self.passwordLine.setPlaceholderText("Password")
        self.mirrorLine = PasswordLine(core)
        self.mirrorLine.setPlaceholderText("Confirm password")

        frame = QtWidgets.QWidget()
        self.innerLayout = QtWidgets.QVBoxLayout(frame)
        self.innerLayout.addWidget(QLabel(label))
        self.innerLayout.addWidget(self.passwordLine)
        self.innerLayout.addWidget(self.mirrorLine)

        self.buttonBox = QtWidgets.QDialogButtonBox()
        self.buttonBox.setStandardButtons(self.buttonBox.Cancel | self.buttonBox.Save)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QtWidgets.QGridLayout(self)
        layout.addItem(QSpacerItem(0, 100, QSizePolicy.Minimum, QSizePolicy.Expanding), 0, 1, 1, 1)
        layout.addItem(QSpacerItem(100, 0, QSizePolicy.Expanding, QSizePolicy.Minimum), 1, 0, 1, 1)
        layout.addWidget(frame, 1, 1, 1, 1)
        layout.addItem(QSpacerItem(100, 0, QSizePolicy.Expanding, QSizePolicy.Minimum), 1, 2, 1, 1)
        layout.addItem(QSpacerItem(0, 100, QSizePolicy.Minimum, QSizePolicy.Expanding), 2, 1, 1, 1)
        layout.addWidget(self.buttonBox, 3, 1, 1, 1)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle(title)
        self.resize(1, 1)

    def _validate(self) -> bool:
        """Saves the key if the password matches the confirmation field"""
        password = self.passwordLine.text()
        if not password:
            self.passwordLine.setErrorPalette(True)
        elif password != self.mirrorLine.text():
            self.mirrorLine.setErrorPalette(True)
        else:
            self.key = Cipher.key(password)
            return True
        return False

    def accept(self):
        if self._validate():
            super().accept()


class MasterPasswordInputDialog(PasswordInputDialog):
    def __init__(self, core, title: str, label: str):
        super().__init__(core, title, label)
        self.buttonBox.setStandardButtons(self.buttonBox.Cancel | self.buttonBox.Open)
        self.mirrorLine.hide()

    def accept(self):
        if self.passwordLine.text():
            self.key = Cipher.key(self.passwordLine.text())
            with open(UserFiles.KEYRING, encoding="utf-8") as f:
                token = f.read().encode()
            try:
                Cipher.decrypt(self.key, token)
                QtWidgets.QDialog.accept(self)
            except InvalidToken:
                self.passwordLine.setErrorPalette(True)
        else:
            self.passwordLine.setErrorPalette(True)
