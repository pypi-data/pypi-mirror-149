#!/usr/bin/python3
import pythoncom
import win32api
import win32com.client
import win32com.server.util
import win32con
import win32gui
from typing import Callable, Union
from win32com.server import localserver
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QTextCursor

try:
    PACKAGED = True
    from ...__id__ import ID
    from ...backend import logger
except (ValueError, ImportError):
    PACKAGED = False
    from __id__ import ID
    from backend import logger

log = logger.new(__name__)


def getRegKey(hkey: str, path: str, name: str) -> Union[str, int]:
    """Returns value from a registry key"""
    hkey = {"HKLM": win32con.HKEY_LOCAL_MACHINE, "HKCU": win32con.HKEY_CURRENT_USER}[hkey.upper()]
    key = win32api.RegOpenKey(hkey, path)
    value = win32api.RegQueryValueEx(key, name)[0]
    return value


def setRegKey(hkey: str, path: str, value: str):
    """Sets a registry key value"""
    hkey = {"HKLM": win32con.HKEY_LOCAL_MACHINE, "HKCU": win32con.HKEY_CURRENT_USER}[hkey.upper()]
    win32api.RegSetValue(hkey, path, win32con.REG_SZ, value)


class Adapter:
    _reg_clsctx_ = pythoncom.CLSCTX_LOCAL_SERVER
    _public_attrs_ = ["parent"]
    _public_methods_ = [
        "setParent",
        "ActiveApplication",
        "ActiveDocument",
        "DonneDebutSelection",
        "DonneFinSelection",
        "DonneIdDocumentCourant",
        "DonneIdZoneDeTexte",
        "DonneIdZoneDeTexteCourante",
        "DonneIntervalle",
        "DonneLongueurZoneDeTexte",
        "DonneNbZonesDeTexte",
        "DonnePolice",
        "DonneTitreDocCourant",
        "RemplaceIntervalle",
        "SelectionneIntervalle",
    ]

    def setParent(self, parent: object):  # parent: PyIDispatch
        """Converts the PyIDispatch object into an <unknown> COMObject"""
        self.parent = win32com.client.Dispatch(parent)

    @classmethod
    def register(cls, progid: str):
        """Registers a local COM server into the registry"""
        import win32com.server.register

        clsid = str(pythoncom.CreateGuid())
        python = win32com.server.register._find_localserver_exe(1)
        python = win32api.GetShortPathName(python)
        server32 = win32com.server.register._find_localserver_module()
        server32 = f'{python} "{server32}" {clsid}'
        namespace = f"{ID}." if PACKAGED else ""
        namespace = f"{namespace}plugins.antidote.com.{cls.__name__}"

        try:
            setRegKey("HKCU", rf"Software\Classes\{progid}\CLSID", clsid)
            setRegKey("HKCU", rf"Software\Classes\AppID\{clsid}", progid)
            setRegKey("HKCU", rf"Software\Classes\CLSID\{clsid}\LocalServer32", server32)
            setRegKey("HKCU", rf"Software\Classes\CLSID\{clsid}\ProgID", progid)
            setRegKey("HKCU", rf"Software\Classes\CLSID\{clsid}\PythonCOM", namespace)
            log.info(f"Registered server {progid} as {clsid}")
        except BaseException:
            log.error(f"Failed to register COM server {progid}")

    @classmethod
    def unregister(cls, progid: str):
        """Removes the local COM server from the registry"""
        try:
            clsid = getRegKey("HKCU", rf"Software\Classes\{progid}\CLSID", "")
            win32api.RegDeleteTree(win32con.HKEY_CURRENT_USER, rf"Software\Classes\{progid}")
            win32api.RegDeleteTree(win32con.HKEY_CURRENT_USER, rf"Software\Classes\AppID\{clsid}")
            win32api.RegDeleteTree(win32con.HKEY_CURRENT_USER, rf"Software\Classes\CLSID\{clsid}")
            log.info(f"Unregistered COM server {progid}")
        except BaseException:
            log.error(f"Failed to unregister COM server {progid}")

    def ActiveApplication(self):
        self.parent.activeApplication()

    def ActiveDocument(self, idDocument: int):
        self.parent.activeDocument(idDocument)

    def DonneDebutSelection(self, idDocument: int, idZoneDeTexte: int) -> int:
        return self.parent.donneDebutSelection(idDocument, idZoneDeTexte)

    def DonneFinSelection(self, idDocument: int, idZoneDeTexte: int) -> int:
        return self.parent.donneFinSelection(idDocument, idZoneDeTexte)

    def DonneIdDocumentCourant(self) -> int:
        return self.parent.donneIdDocumentCourant()

    def DonneIdZoneDeTexte(self, idDocument: int, indiceZoneDeTexte: int) -> int:
        return self.parent.donneIdZoneDeTexte(idDocument, indiceZoneDeTexte)

    def DonneIdZoneDeTexteCourante(self, idDocument: int) -> int:
        return self.parent.donneIdZoneDeTexteCourante(idDocument)

    def DonneIntervalle(self, idDocument: int, idZoneDeTexte: int, debut: int, fin: int) -> str:
        return self.parent.donneIntervalle(idDocument, idZoneDeTexte, debut, fin)

    def DonneLongueurZoneDeTexte(self, idDocument: int, idZoneDeTexte: int) -> int:
        return self.parent.donneLongueurZoneDeTexte(idDocument, idZoneDeTexte)

    def DonneNbZonesDeTexte(self, idDocument: int) -> int:
        return self.parent.donneNbZonesDeTexte(idDocument)

    def DonnePolice(self, idDocument: int, idZoneDeTexte: int) -> str:
        return self.parent.donnePolice(idDocument, idZoneDeTexte)

    def DonneTitreDocCourant(self) -> str:
        return self.parent.donneTitreDocCourant()

    def RemplaceIntervalle(self, idDocument: int, idZoneDeTexte: int, debut: int, fin: int, chaine: str):
        self.parent.remplaceIntervalle(idDocument, idZoneDeTexte, debut, fin, chaine)

    def SelectionneIntervalle(self, idDocument: int, idZoneDeTexte: int, debut: int, fin: int):
        self.parent.selectionneIntervalle(idDocument, idZoneDeTexte, debut, fin)


class API:  # API Antidote v2.0 r2
    _public_methods_ = [
        "activeApplication",
        "activeDocument",
        "donneDebutSelection",
        "donneFinSelection",
        "donneIdDocumentCourant",
        "donneIdZoneDeTexte",
        "donneIdZoneDeTexteCourante",
        "donneIntervalle",
        "donneLongueurZoneDeTexte",
        "donneNbZonesDeTexte",
        "donnePolice",
        "donneTitreDocCourant",
        "remplaceIntervalle",
        "selectionneIntervalle",
    ]

    def ignoreRuntimeError(func: Callable) -> Callable:
        """Logs API calls and ignores RuntimeError during execution"""

        def wrapper(self, *args) -> any:
            try:
                _return = func(self, *args)
                log.debug(f"{func.__qualname__}{args} -> {repr(_return)}")
                return _return
            except RuntimeError:
                log.debug(f"RuntimeError in {func.__qualname__}{args}")

        return wrapper

    @ignoreRuntimeError
    def activeApplication(self):
        self.body.window().activateWindow()
        self.body.window().raise_()

    def activeDocument(self, idDocument: int):
        self.activeApplication()

    @ignoreRuntimeError
    def donneDebutSelection(self, idDocument: int, idZoneDeTexte: int) -> int:
        ancre = self.body.textCursor().anchor()
        position = self.body.textCursor().position()
        return min(ancre, position)

    @ignoreRuntimeError
    def donneFinSelection(self, idDocument: int, idZoneDeTexte: int) -> int:
        ancre = self.body.textCursor().anchor()
        position = self.body.textCursor().position()
        return max(ancre, position)

    def donneIdDocumentCourant(self) -> int:
        return 1

    def donneIdZoneDeTexte(self, idDocument: int, indiceZoneDeTexte: int) -> int:
        return 1

    def donneIdZoneDeTexteCourante(self, idDocument: int) -> int:
        return 1

    @ignoreRuntimeError
    def donneIntervalle(self, idDocument: int, idZoneDeTexte: int, debut: int, fin: int) -> str:
        textCursor = self.body.textCursor()
        textCursor.movePosition(QTextCursor.Start)
        textCursor.movePosition(QTextCursor.NextCharacter, QTextCursor.MoveAnchor, debut)
        textCursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor, fin - debut)
        return textCursor.selectedText()

    @ignoreRuntimeError
    def donneLongueurZoneDeTexte(self, idDocument: int, idZoneDeTexte: int) -> int:
        return len(self.body.toPlainText())

    def donneNbZonesDeTexte(self, idDocument: int) -> int:
        return 1

    def donnePolice(self, idDocument: int, idZoneDeTexte: int) -> str:
        return ""

    @ignoreRuntimeError
    def donneTitreDocCourant(self) -> str:
        return self.body.window().windowTitle()

    @ignoreRuntimeError
    def remplaceIntervalle(self, idDocument: int, idZoneDeTexte: int, debut: int, fin: int, chaine: str):
        if debut >= 0 and fin >= 0:
            textCursor = self.body.textCursor()
            textCursor.setPosition(debut)
            textCursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor, fin - debut)
            textCursor.insertText(chaine)
        self.body.ensureCursorVisible()

    @ignoreRuntimeError
    def selectionneIntervalle(self, idDocument: int, idZoneDeTexte: int, debut: int, fin: int):
        textCursor = self.body.textCursor()
        textCursor.setPosition(debut)
        textCursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor, fin - debut)
        self.body.setTextCursor(textCursor)


class ServerThread(QtCore.QObject):
    def __init__(self):
        super().__init__()

    def run(self):
        pythoncom.CoInitialize()
        localserver.serve([self.clsid])


class Antidote(QtCore.QObject, API):
    ready = QtCore.pyqtSignal()

    def __init__(self, uid: str, path: str, init: bool):
        super().__init__()
        self.progid = f"{uid}.Antidote"
        self.body = QtWidgets.QPlainTextEdit()  # Placeholder
        self.api = None

        version = getRegKey("HKLM", r"Software\Druide informatique inc.\Antidote", "VersionAPI")
        version = min([2.0, float(version)])
        self.version = str(version)
        self._launch(path)
        if init:
            self.init()

    def correct(self, body: QtWidgets.QPlainTextEdit):
        """Launches Antidote's corrector tool"""
        if self.api:
            self.body = body
            self.api.LanceOutilDispatch2(self.server, "C", "", self.version)
        else:
            log.error("Could not call Antidote: Local COM server is not ready")

    def init(self):
        """Initializes COM interface"""
        self.worker = ServerThread()
        self.workerThread = QtCore.QThread()
        self.workerThread.started.connect(self.worker.run)
        self.workerThread.started.connect(self._setup)
        self.worker.moveToThread(self.workerThread)
        self._serve()

    def _launch(self, path: str):
        """Opens Antidote binary"""
        if not win32gui.FindWindow("AntQ", None):
            QtCore.QProcess.startDetached(path, ["-activex"])
            log.info(f"{path} -activex")

    def _serve(self, failed=False):
        """Initializes the local COM server"""
        try:
            clsid = getRegKey("HKCU", rf"Software\Classes\{self.progid}\CLSID", "")
            self.worker.clsid = clsid
            self.workerThread.start()
        except BaseException:
            if failed:
                log.error("Failed to initialize local COM server")
                Adapter.unregister(self.progid)
            else:
                log.info("Local COM server not found in registry")
                Adapter.register(self.progid)
                self._serve(failed=True)

    def _setup(self):
        """Initializes the local COM server along with Antidote API OLE public server"""
        if win32gui.FindWindow("AntQ", None):
            try:
                self.server = win32com.client.Dispatch(f"{self.progid}")
                self.server.setParent(win32com.server.util.wrap(self))
                self.api = win32com.client.Dispatch("Antidote.ApiOle")
                self.ready.emit()
            except BaseException:
                log.error("Server dispatch failed")
                Adapter.unregister(self.progid)
        else:
            QtCore.QTimer.singleShot(1000, self._setup)
