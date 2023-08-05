#!/usr/bin/python3
import json
import re
import requests
import shutil
import sys
import zipfile
from argparse import Namespace
from cryptography.fernet import Fernet
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterable, List
from PyQt5 import QtWidgets, QtCore, QtGui

try:
    from .__id__ import APP_NAME, ID, VERSION
    from .__db__ import CSS_DEFAULT, SDB_DEFAULT, NDB_DEFAULT
    from .backend import (
        UserDirs,
        UserFiles,
        CoreActions,
        DeepPath,
        RootDirs,
        RootFiles,
        Tuples,
        cli,
        logger,
        sanitizeFileName,
    )
    from .backend.cli import CommandParser
    from .backend.cryptography import Cipher, MasterKeyPrompt
    from .backend.database import Database
    from .backend.observer import ObserverList
    from .backend.legacy import Legacy
    from .menus import MoveDialog
    from .menus.core import CoreMenu, ConfirmPrompt
    from .menus.search import Launcher, Search
    from .notes import Note
    from .notes.console import Console
    from .notes.vim import Vim
    from .notes.plain import Plain
    from .notes.html import HTML
    from .notes.image import Image
    from .settings import Settings
    from .settings.wizard import Wizard
    from .plugins import antidote
except (ValueError, ImportError):
    from __id__ import APP_NAME, ID, VERSION
    from __db__ import CSS_DEFAULT, SDB_DEFAULT, NDB_DEFAULT
    from backend import (
        UserDirs,
        UserFiles,
        CoreActions,
        DeepPath,
        RootDirs,
        RootFiles,
        Tuples,
        cli,
        logger,
        sanitizeFileName,
    )
    from backend.cli import CommandParser
    from backend.cryptography import Cipher, MasterKeyPrompt
    from backend.database import Database
    from backend.observer import ObserverList
    from backend.legacy import Legacy
    from menus import MoveDialog
    from menus.core import CoreMenu, ConfirmPrompt
    from menus.search import Launcher, Search
    from notes import Note
    from notes.console import Console
    from notes.vim import Vim
    from notes.plain import Plain
    from notes.html import HTML
    from notes.image import Image
    from settings import Settings
    from settings.wizard import Wizard
    from plugins import antidote

HAS_TERMINAL = "QTermWidget" in sys.modules
log = logger.new(__name__)


class Core(QtCore.QObject):
    def __init__(self, app: QtWidgets.QApplication):
        super().__init__()
        self.app = app
        self.clipboard = app.clipboard()
        self.notes = NoteOperations(self)
        self.setup = CoreSetup(self)
        self.notes.init()
        app.primaryScreenChanged.connect(self.notes.reposition)
        log.info("Initialization completed")

    @property
    def loaded(self) -> dict:
        return self.notes.loaded

    def colorize(self, icon: QtGui.QIcon, color: QtGui.QColor) -> QtGui.QIcon:
        """Applies a custom foreground color on a monochrome QIcon"""
        pixmap = icon.pixmap(48, 48)
        painter = QtGui.QPainter(pixmap)
        painter.setCompositionMode(painter.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), color)
        painter.end()
        return QtGui.QIcon(pixmap)

    def execute(self, db: str, key: str, path: Path = None):
        """Translates mouse press events into core or note actions"""
        try:
            group, action = self.sdb["mouse events"][db][key]
            cmd = {group: [action]}
            if group == "note":
                cmd["note"].append(path)
            self.parser.fromDict(cmd)
        except (KeyError, ValueError):
            pass

    def fileManager(self, path: Path = UserDirs.NOTES):
        """Opens the default file system manager. Uses xdg-open for Linux or explorer for Windows"""
        path = path if path.is_dir() else path.parent
        self.fm.setArguments([str(path)])
        if not self.fm.startDetached()[0]:
            log.warning(f"Could not open directory '{path}'")

    def getNoteDecorationsCSS(self, *paths: Path) -> dict:
        """Serializes and combines the content of NoteDecorations{} selector from stylesheets"""
        css = dict(CSS_DEFAULT)
        if UserFiles.DECORATIONS.is_file():
            with open(UserFiles.DECORATIONS, encoding="utf-8") as f:
                css.update(json.load(f))

        stylesheets = [p for p in paths if p and p.is_file()]
        for s in stylesheets:
            with open(s, encoding="utf-8") as f:
                selector = re.findall(self.regex.selector, f.read())
                elements = re.findall(self.regex.elements, "".join(selector))
            for e in elements:
                css[e[0]] = e[1]
        return css

    def getNotesFiles(self, path: Path, recursive=True) -> list:
        """Returns a recursive list of note files. Accepts a directory"""
        files = []
        for ext in ("txt", "png"):
            if recursive:
                files += [f for f in path.rglob(f"*.{ext}") if f.is_file()]
            else:
                files += [f for f in path.glob(f"*.{ext}") if f.is_file()]
        return files

    def moveDialog(self, path: Path) -> Path:
        """Opens subfolder browser dialog"""
        dialog = MoveDialog(path)
        if dialog.exec_() == dialog.Accepted:
            dest = DeepPath(dialog.selectedFiles()[0]) / path.name
            if dest != path:
                dest = self.nameIndex(dest) if dest.exists() else dest
                self.notes.move(path, dest)

    def nameIndex(self, path: Path) -> Path:
        """Increments a numeric suffix until a unique name is found"""
        taken = [f.stem for f in path.parent.glob("*.txt") if f.exists()]
        taken += [f.stem for f in path.parent.glob("*.png") if f.exists()]
        taken += [f.name for f in path.parent.glob("*") if f.is_dir()]
        title = path.stem
        try:
            index = int(path.stem.rsplit(" ", 1)[1])
            title = path.stem.rsplit(" ", 1)[0]
        except (ValueError, IndexError):
            index = 1

        name = f"{title} {index}"
        while name in taken:
            name = f"{title} {index}"
            index += 1
        return (path.parent / name).with_suffix(path.suffix)

    def quit(self, *args):
        """Closes all notes and saves databases"""
        for path in dict(self.loaded):
            self.loaded[path].close()
        self.ndb.save()
        self.pdb.save()
        log.info(f"Leaving {APP_NAME}")
        self.app.quit()
        sys.exit(0)

    def savePNG(self, pixmap: QtGui.QPixmap):
        """Saves and loads a PNG file from a Mime object pixmap"""
        name = self.sdb["general"]["default name"] + ".png"
        path = self.nameIndex(UserDirs.NOTES / name)
        f = QtCore.QFile(str(path))
        f.open(QtCore.QIODevice.WriteOnly)
        pixmap.save(f, "PNG")
        self.notes.add(path)

    def searchToggle(self, show: bool = None):
        """Shows, hides or toggles the note search utility"""
        if show is None:
            visible = self.launcher.isVisible()
            self.launcher.setVisible(not visible)
        else:
            self.launcher.setVisible(show)
            self.launcher.activateWindow()

    def setGlobalIconsColor(self, key: str, color: str):
        """Sets a property override for NoteDecorations{} CSS"""

        def _reloadMenuIcons():
            self.setup.reloadIcons()
            for path, note in self.loaded.items():
                note.decorate()

        if UserFiles.DECORATIONS.is_file():
            with open(UserFiles.DECORATIONS, encoding="utf-8") as f:
                css = json.load(f)
        else:
            css = {}
        css[key] = color

        with open(UserFiles.DECORATIONS, "w", encoding="utf-8") as f:
            f.write(json.dumps(css, indent=2))

        if key == "tray-icon":
            self.tray.update()
        elif key == "menu-icon":
            _reloadMenuIcons()

    def settings(self):
        """Opens the settings dialog"""
        self.settingsDialog = Settings(self)

    def screen(self) -> QtGui.QScreen:
        """Returns the primary screen geometry"""
        screen = self.app.primaryScreen()
        return screen.availableGeometry()

    def screens(self) -> Iterable[QtGui.QScreen]:
        """Returns the all screens geometry"""
        for s in self.app.screens():
            yield s.availableGeometry()

    def trash(self, path: Path):
        """Moves a file or a folder tree to /trash/"""
        relative = path.relative_to(UserDirs.NOTES)
        dest = UserDirs.TRASH / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        if path.is_symlink():
            path.unlink()
        elif path.is_dir():
            shutil.copytree(path, dest, dirs_exist_ok=True)
            shutil.rmtree(path, ignore_errors=True)
        else:
            try:
                shutil.move(path, dest)
                log.info(f"Thrashed '{path}'")
            except FileNotFoundError:
                log.warning(f"trash() : No such file '{path}'")

    def wizard(self):
        """Launches wizard dialog"""
        self.wizardDialog = Wizard(self)
        self.wizardDialog.show()

    def _dropEvent(self, path: Path, mime: Tuples.Mime):
        """Handler for Mime objects parsed in a Note dropEvent. Accepts filesystem or web URL"""
        if path not in self.loaded:
            return  # Avoid race condition while saving dropped pixmap

        note = self.loaded[path]
        log.info(f"{note.id} : DropEvent : {mime}")

        if mime.type == "image":
            log.info(f"{note.id} : DropEvent : Saving dropped pixmap ...")
            if path.stat().st_size == 0:
                self.notes.delete(path)
            self.savePNG(mime.data)
        elif mime.type == "text":
            if note.mode in ("plain", "html", "vim"):
                note.drop(mime)

    def _popupMenu(self):
        """Opens the main contextual menu"""
        pos = QtGui.QCursor.pos()
        try:
            self.tray.menu.popup(pos)
        except AttributeError:
            log.error("System tray icon is not yet available")


class CoreSetup:
    """Setups instances and variables for Core class"""

    def __init__(self, core):
        self.core = core
        newUser = not UserFiles.SETTINGS.is_file()
        self.database()
        self.clean()
        self.regex()
        self.fonts()
        self.icons()
        self.actions()
        self.extra()
        self.plugins()
        self.encryption()
        if newUser:
            core.wizard()
        else:
            Legacy.menus(core)
            Legacy.css(core)
        core.sdb["legacy"] = VERSION

    def actions(self):
        """Translates action names into labels, icons and function calls"""
        c = self.core
        Action = Tuples.Action

        c.actions = CoreActions(
            {
                # Core actions
                "folders list": Action("Folders tree", c.icons["folder_active"], lambda: None),
                "hide": Action("Hide all", c.icons["hide"], c.notes.hideAll),
                "load": Action("Load folders", c.icons["load_folders"], c.notes.load),
                "menu": Action("Show main menu", c.icons["tray"], c._popupMenu),
                "new": Action("New note", c.icons["new"], c.notes.new),
                "notes list": Action("Orphan notes list", c.icons["plain_regular"], lambda: None),
                "open": Action("Open in file manager", c.icons["folder_open"], c.fileManager),
                "quit": Action("Quit", c.icons["quit"], c.quit),
                "reset": Action("Reset positions", c.icons["reset"], c.notes.reset),
                "reverse": Action("Reverse all", c.icons["reverse"], c.notes.toggleAll),
                "search": Action("Search repository", c.icons["search"], c.searchToggle),
                "separator": Action("Separator", c.icons["separator"], lambda: None),
                "settings": Action("Settings", c.icons["settings"], c.settings),
                "show": Action("Show all", c.icons["show"], c.notes.showAll),
                "toggle": Action("Toggle favorites", c.icons["toggle"], c.notes.toggleFavorites),
                "unload": Action("Unload folders", c.icons["unload_folders"], c.notes.unloadAllFolders),
                "wizard": Action("Setup wizard", c.icons["wizard"], c.wizard),
            },
            {
                # Browser actions
                "delete": Action("Delete folder", c.icons["delete"], c.notes.delete),
                "load": Action("Load all", c.icons["load_folders"], c.notes.load),
                "move": Action("Move folder", c.icons["move"], c.moveDialog),
                "new": Action("New note", c.icons["new"], c.notes.new),
                "open": Action("Open in file manager", c.icons["folder_open"], c.fileManager),
                "rename": Action("Rename folder", c.icons["rename"], c.notes.rename),
                "separator": Action("Separator", c.icons["separator"], lambda: None),
                "show": Action("Show all", c.icons["show"], c.notes.showAll),
                "unload": Action("Unload all", c.icons["unload_folders"], c.notes.unload),
            },
        )
        log.info("Loaded core actions")

    def clean(self):
        """Removes blanks, lint, expired files and manage archives"""
        self.records = self.RecordKeeping(self.core)
        self.recordsThread = QtCore.QThread()
        self.records.moveToThread(self.recordsThread)
        self.recordsThread.start()
        self.archiveTimer = QtCore.QTimer(interval=3600000)  # 60 min
        self.archiveTimer.timeout.connect(self._makeArchive)
        self.archiveTimer.start()
        self._makeArchive()

    def css(self):
        """Loads global.css stylesheet"""
        sheet = UserFiles.CSS if UserFiles.CSS.is_file() else RootFiles.CSS
        with open(sheet, encoding="utf-8") as f:
            self.core.app.setStyleSheet(f.read())
        log.debug(f"Loaded global CSS '{sheet}'")

    def database(self):
        """Initializes databases and favorites notes"""
        self.core.pdb = Database(UserFiles.PROFILES, default={})  # Profiles
        self.core.sdb = Database(UserFiles.SETTINGS, default=SDB_DEFAULT)  # Settings
        self.core.ndb = Database(UserFiles.NOTES, default=NDB_DEFAULT)  # Notes

    def encryption(self):
        """Prompts user for master key password"""
        self.core.masterKey = None
        if UserFiles.KEYRING.is_file():
            MasterKeyPrompt.login(self.core)

    def extra(self):
        """Setups auxiliaries instances"""
        self.core.parser = CommandParser(self.core)
        self.core.tray = TrayIcon(self.core)

        # Drop filter
        self.core.dropFilter = DropFilter()
        self.core.dropThread = QtCore.QThread()
        self.core.dropFilter.moveToThread(self.core.dropThread)
        self.core.dropFilter.mime.connect(self.core._dropEvent)
        self.core.dropThread.start()

        # File manager
        self.core.fm = self.FileManager()
        log.info("Loaded auxiliaries objects")

        # Search file utilities
        self.core.search = Search(self.core)
        self.core.launcher = Launcher(self.core)

    def fonts(self):
        """Loads Liberation fonts for cross-platform stylesheets"""
        fonts = [str(f) for f in RootDirs.FONTS.glob("*.ttf") if f.is_file()]
        for f in fonts:
            QtGui.QFontDatabase.addApplicationFont(f)
        log.info("Loaded fonts")

    def icons(self):
        """Loads and colorize all SVG icons"""
        css = self.core.getNoteDecorationsCSS()
        color = QtGui.QColor(css["menu-icon"])
        self.core.icons = {}
        for path in [x for x in RootDirs.ICONS.glob("*.svg") if x.is_file()]:
            icon = QtGui.QIcon(str(path))
            self.core.icons[path.stem] = self.core.colorize(icon, color)
        log.info("Loaded icons")

    def plugins(self):
        """Loads third-party software"""
        if sys.platform.startswith("win"):
            self.core.antidote = antidote.getHandler(APP_NAME, init=True, silent=True)
        log.info("Loaded plugins")

    def regex(self):
        """Pre-compiles CSS regex patterns"""
        selector = re.compile(r"(?:NoteDecorations\s*\{\s*)([\s\S]*?)(?:\s*\})")  # NoteDecorations{}
        element = re.compile(r"([^:;\s]+)\s?:\s?([^;\s]+)(?=;)")  # Elements within a selector
        property_ = r"(NoteDecorations\s*\n*{[\w\W]*)%s\s*:\s*(#[abcdefABCDEF\d]{6}|\w+\s*);([\w\W]*?})"
        self.core.regex = Tuples.RegexCSS(selector, element, property_)

    def reloadIcons(self):
        """Reload icons in core and loaded notes"""
        self.icons()
        self.actions()
        for path in self.core.loaded:
            note = self.core.loaded[path]
            note.setup.actions()

    def _makeArchive(self):
        QtCore.QMetaObject.invokeMethod(self.records, "archive", QtCore.Qt.QueuedConnection)

    class FileManager(QtCore.QProcess):
        def __init__(self):
            super().__init__()
            self.setStandardOutputFile(QtCore.QProcess.nullDevice())
            self.setStandardErrorFile(QtCore.QProcess.nullDevice())
            if sys.platform.startswith("win"):
                self.setProgram("explorer")
            else:
                self.setProgram("xdg-open")

    class RecordKeeping(QtCore.QObject):
        def __init__(self, core):
            super().__init__()
            self.core = core
            self.blanks()
            self.purge()
            self.lint()

        @QtCore.pyqtSlot()
        def archive(self):
            """Creates a new archive if required"""
            if self.core.sdb["archives"]["frequency"]:
                UserDirs.ARCHIVES.mkdir(parents=True, exist_ok=True)
                limit = datetime.now() - timedelta(days=self.core.sdb["archives"]["frequency"])
                archives = [self._ctime(f) for f in UserDirs.ARCHIVES.glob("*.zip")]
                if not archives or max(archives) < limit:
                    self._saveArchive()

        def blanks(self):
            """Removes empty files and folders"""
            if self.core.sdb["clean"]["blanks"]:
                self._delete([f for f in UserDirs.NOTES.rglob("*") if f.is_empty()])

        def lint(self):
            """Removes dead keys from databases"""
            for nid in list(self.core.ndb["loaded"]):
                path = UserDirs.NOTES / nid
                if not path.exists():
                    self.core.ndb["loaded"].remove(nid)
                    log.warning(f"Removed '{nid}' from loaded database")

            for nid in list(self.core.ndb["favorites"]):
                path = UserDirs.NOTES / nid
                if not path.exists():
                    self.core.ndb["favorites"].remove(nid)
                    log.warning(f"Removed '{nid}' from favorites database")

            for nid in dict(self.core.pdb):
                path = UserDirs.NOTES / nid
                if not path.is_file():
                    del self.core.pdb[nid]
                    log.warning(f"Removed '{nid}' from profiles database")

            log.debug("Cleaned orphan databases entries")

        def purge(self):
            """Removes old files from trash, archives and logs folders"""
            tasks = (
                Tuples.Cleaner(UserDirs.TRASH, self.core.sdb["clean"]["trash"]),
                Tuples.Cleaner(UserDirs.LOGS, self.core.sdb["clean"]["logs"]),
                Tuples.Cleaner(UserDirs.ARCHIVES, self.core.sdb["clean"]["archives"]),
            )
            for task in tasks:
                expired = self._expired(task.dir, task.delay)
                self._delete(expired)
            log.info("Cleaned trashes, logs and archives")

        def _ctime(self, path: Path) -> datetime:
            """Returns the creation time of a file"""
            creation = path.stat().st_ctime
            return datetime.fromtimestamp(creation)

        def _delete(self, files: List[Path]):
            """Deletes a list of files or folders"""
            for f in files:
                try:
                    f.unlink()
                    log.info(f"Removed file '{f}'")
                except IsADirectoryError:
                    shutil.rmtree(f)
                    log.info(f"Removed folder '{f}'")
                except (PermissionError, FileNotFoundError):
                    pass

        def _expired(self, path: Path, days: int) -> List[Path]:
            """Recurses into a directory and returns a list of files older than <days>"""
            limit = datetime.now() - timedelta(days=days)
            try:
                return [f for f in path.rglob("*") if self._ctime(f) < limit]
            except FileNotFoundError as error:
                log.warning(f"{error}. Dead link ?")
            return []

        def _saveArchive(self):
            """Builds the archive"""
            files = []
            if self.core.sdb["archives"]["text"]:
                files += [f for f in UserDirs.NOTES.rglob("*.png") if f.is_file()]
            if self.core.sdb["archives"]["image"]:
                files += [f for f in UserDirs.NOTES.rglob("*.txt") if f.is_file()]

            if files:
                now = datetime.now()
                path = UserDirs.ARCHIVES / f"{now.year:02d}-{now.month:02d}-{now.day:02d}.zip"
                log.info(f"Saving new archive into '{path}' ...")
                self._zip(files, path)

        def _zip(self, files: List[Path], path: Path):
            """Creates a zip file while preserving the file tree"""
            try:
                with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as f:
                    for file in files:
                        f.write(file, file.relative_to(UserDirs.NOTES))
                log.info("Archive created successfully")
            except Exception:
                log.exception("Could not save archive")


class NoteOperations(QtCore.QObject):
    def __init__(self, core: QtCore.QObject):
        self.loaded = {}
        self.core = core

    @property
    def ndb(self) -> dict:
        return self.core.ndb

    @property
    def pdb(self) -> dict:
        return self.core.pdb

    @property
    def sdb(self) -> dict:
        return self.core.sdb

    def add(self, path: Path, show=True, recursive=True):
        """Adds Note objects to self.loaded. Accepts a file or a folder tree"""
        if path.is_file():
            if path not in self.loaded:
                self._load(path)
                if show:
                    self.loaded[path].show()
                log.info(f"Loaded '{path}'")

        elif path.is_dir():
            for f in self.core.getNotesFiles(path, recursive=recursive):
                self.add(f)

    def addConfirm(self, path: Path):
        """Prevents the user before loading excessive amount of notes"""
        notesCount = len(self.core.getNotesFiles(path))
        if notesCount >= self.sdb["general"]["maximum load"]:
            msg = f"This action will load <b>{notesCount}</b> notes<br>all at once. Continue ?"
            dialog = ConfirmPrompt("Confirmation", msg)
            if dialog.exec_() == dialog.Yes:
                self.add(path)
        else:
            self.add(path)

    def delete(self, path: Path):
        """Sends note file to trash. Accepts a file or a folder tree"""
        self.unload(path)
        if path.exists():
            self.core.trash(path)
        self.core.setup.records.lint()

    def hideAll(self):
        """Hides all but pinned notes"""
        for path in dict(self.loaded):
            nid = self.loaded[path].id
            if not self.pdb[nid]["pin"]:
                self.loaded[path].hide()

    def init(self):
        """Loads subnotes and load/raise pinned notes on startup"""
        if not self.sdb["general"]["minimize"]:
            for nid, profile in self.pdb.items():
                if profile["pin"]:
                    self.add((UserDirs.NOTES / nid), show=True)

        for nid in list(self.ndb["loaded"] + self.ndb["favorites"]):
            self.add((UserDirs.NOTES / nid), show=False)

    def load(self, path=UserDirs.NOTES):
        """Loads notes recursively"""
        if bool(self.sdb["general"]["maximum load"]):
            self.addConfirm(path)
        else:
            self.add(path)

    def mode(self, path: Path, mode: str):
        """Sets a note interface mode (plain/html/vim/console)"""
        note = self.loaded[path]
        log.info(f"{note.id} : Changing mode from '{note.mode}' to '{mode}'")

        def htmlToPlainText(content: str, key: Fernet) -> str:
            textEdit = QtWidgets.QTextEdit()
            textEdit.setHtml(content)
            if key:
                token = Cipher.encrypt(key, textEdit.toPlainText())
                return Cipher.MAGIC + token.decode("utf-8")
            else:
                return textEdit.toPlainText()

        def setMode(note):
            isHtml = note.content.startswith("<!DOCTYPE HTML") or path.is_html()
            content = htmlToPlainText(note.content, note.key)
            note.save()
            self.pdb[note.id]["mode"] = mode
            note.close()
            if mode != "html" and isHtml:
                try:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(content)
                except PermissionError:
                    pass
            self.add(path)

        note.busy = True
        note.load()
        key = note.key
        setMode(note)  # Creates a new Note
        self.loaded[path].keyring.setKey(key)
        self.loaded[path].save()

    def move(self, src: Path, dest: Path):
        """Renames a note or a group of note. Accepts a file or a folder"""
        log.info(f"Moving '{src}' to '{dest}'")

        if src.is_file() and src.is_symlink():
            src.rename(dest)
            self._moveNoteMetadata(src, dest)

        elif src.is_file():
            self._moveNoteFile(src, dest)
            self._moveNoteMetadata(src, dest)

        elif src.is_dir() and src.is_symlink():
            for f in src.rglob("*"):
                self._moveNoteMetadata(f, dest / f.relative_to(src))
            src.rename(dest)

        elif src.is_dir():
            for f in src.rglob("*"):
                self.move(f, dest / f.relative_to(src))
            shutil.rmtree(src, ignore_errors=True)

    def new(self, path: Path = UserDirs.NOTES):
        """Create a new text note"""
        mode = self.sdb["profile default"]["mode"]
        name = self.sdb["general"]["default name"] + ".txt"
        dest = self.core.nameIndex(path / name)
        if not dest.parent.is_dir():  # Opened from a note action call
            dest = self.core.nameIndex(path.parent / name)  # Use note's parent path instead
        dest.touch()
        note = self._loadNote(dest, mode)
        note.show()

    def rename(self, path: Path):
        """Opens a renaming prompt. Accepts a file or a folder tree"""
        relative = path.relative_to(UserDirs.NOTES)
        dialog = QtWidgets.QInputDialog()
        dialog.setFixedSize(280, 120)
        dialog.setInputMode(dialog.TextInput)
        dialog.setWindowFlags(dialog.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        dialog.setWindowTitle(f"Rename '{relative}'")
        dialog.setLabelText("Enter the new name:")
        dialog.setTextValue(path.stem)

        if dialog.exec_() == dialog.Accepted:
            dest = sanitizeFileName(dialog.textValue(), default=path.stem)
            dest = path.parent / (dest + path.suffix)
            if dest.exists() and dest != path:
                dest = self.core.nameIndex(dest)
            self.move(path, dest)

    def reposition(self, screen: QtGui.QScreen):
        """Moves out of bounds notes to the center of the primary screen"""
        if self.sdb["general"]["reposition"]:
            for path, note in self.loaded.items():
                if note.isVisible() and not note.onScreen:
                    note.snap()

    def reset(self):
        """Shows all and resets the geometry of all loaded notes"""

        def _move():
            total = len(self.loaded)
            for index, path in enumerate(self.loaded, start=1):
                note = self.loaded[path]
                pos = note.position(index, total)
                note.move(*pos)
                self.pdb[note.id]["position"] = pos

        def _opacity():
            for path, note in self.loaded.items():
                note.setWindowOpacity(1.0)
                self.pdb[note.id]["opacity"] = 1.0

        def _resize():
            for path, note in self.loaded.items():
                width = self.sdb["profile default"]["width"]
                height = self.sdb["profile default"]["height"]
                note.unroll()

                # Adjust image size prior to position calculation
                if note.mode == "image":
                    note.setMinimumSize(1, 1)
                    note.resize(width, height)

                # Profile and stylesheet update
                self.pdb[note.id]["width"] = width
                self.pdb[note.id]["height"] = height
                note.resize(width, height)
                note.activateWindow()

        self.showAll()
        QtCore.QTimer.singleShot(0, _opacity)
        QtCore.QTimer.singleShot(0, _resize)
        QtCore.QTimer.singleShot(0, _move)

    def showAll(self, folder: Path = UserDirs.NOTES):
        """Shows all loaded notes relative to a path"""
        self.add(UserDirs.NOTES, recursive=False)
        for path, note in self.loaded.items():
            if folder in path.parents:
                note.show()

    def toggle(self, path: Path):
        """Show or hide a note"""
        if path not in self.loaded:
            self.add(path)
        else:
            isVisible = self.loaded[path].isVisible()
            self.loaded[path].setVisible(not isVisible)

    def toggleAll(self):
        """Toggles all loaded notes"""
        for path in self.loaded:
            self.toggle(path)

    def toggleFavorites(self):
        """Updates favorites notes list and toggle their visibility"""

        def _activatePinned():
            for path, note in self.loaded.items():
                if self.pdb[note.id]["pin"]:
                    note.activateWindow()

        def _visiblesSurvey() -> Iterable:
            for path, note in self.loaded.items():
                pinned = self.pdb[note.id]["pin"]
                if note.isVisible() and not pinned:
                    yield path

        def _relative(path: Path) -> str:
            relative = path.relative_to(UserDirs.NOTES)
            return str(relative)

        visibles = [_relative(path) for path in _visiblesSurvey()]
        favorites = [path for path in visibles if path in self.ndb["favorites"]]
        favorites = favorites if favorites else visibles
        if visibles:
            cb = self.ndb["favorites"].cb
            self.ndb["favorites"] = ObserverList(favorites, callback=cb)
            self.hideAll()
            _activatePinned()
        else:
            for path, note in self.loaded.items():
                if _relative(path) in self.ndb["favorites"]:
                    note.show()

    def unload(self, path: Path):
        """Cleanly closes Note objects. Accepts a file or a folder tree"""
        if path.is_dir():
            for f in self.core.getNotesFiles(path):
                self.unload(f)
        elif path in self.loaded:
            self.loaded[path].close()

    def unloadAllFolders(self):
        """Unloads all sub-folders"""
        folders = [f for f in UserDirs.NOTES.glob("*") if f.is_dir()]
        for f in folders:
            self.unload(f)

    def _load(self, path: Path):
        """Creates an image or a text Note instance from a file"""
        nid = str(path.relative_to(UserDirs.NOTES))
        try:  # Existing "mode" attribute in profile
            mode = self.pdb[nid]["mode"]
            note = self._loadNote(path, mode)
        except KeyError:  # New note
            if path.suffix == ".png":
                mode = "image"
            elif path.is_html():
                mode = "html"
            elif path.is_script() and HAS_TERMINAL:
                mode = "console"
            else:
                mode = self.sdb["profile default"]["mode"]  # Default

            log.info(f"New profile created for '{nid}' ({mode})")
            note = self._loadNote(path, mode)
            QtCore.QTimer.singleShot(0, note.resizeToContent)

        if path.is_nested():
            if nid not in self.ndb["loaded"]:
                self.ndb["loaded"].append(nid)

    def _loadNote(self, path: Path, mode: str) -> Note:
        """Creates an instance of the desired mode"""
        if mode == "image":
            self.loaded[path] = Image(self.core, path)
        elif mode == "html":
            self.loaded[path] = HTML(self.core, path)
        elif mode == "console" and HAS_TERMINAL:
            self.loaded[path] = Console(self.core, path)
        elif mode == "vim" and HAS_TERMINAL:
            self.loaded[path] = Vim(self.core, path)
        else:
            self.loaded[path] = Plain(self.core, path)

        note = self.loaded[path]
        if mode in ("html", "plain"):
            note.shown.connect(self.core.search.attach)
            note.hidden.connect(self.core.search.detach)
        return note

    def _moveNoteFile(self, src: Path, dest: Path):
        """Moves note in the file system"""
        dest.parent.mkdir(parents=True, exist_ok=True)
        try:
            shutil.move(src, dest)
        except (OSError, FileExistsError, PermissionError) as error:
            log.exception(error)

    def _moveNoteMetadata(self, src: Path, dest: Path):
        """Moves note metadata among databases. Called only AFTER the file was moved (Vim)"""
        oid = str(src.relative_to(UserDirs.NOTES))
        nid = str(dest.relative_to(UserDirs.NOTES))
        dest = DeepPath(dest)

        if src in self.loaded:  # Update loaded list
            self.loaded[dest] = self.loaded.pop(src)
            self.loaded[dest].setup.uid(dest)

            if oid in self.ndb["favorites"]:  # Update favorites
                self.ndb["favorites"].remove(oid)
                self.ndb["favorites"].append(nid)

            if isinstance(self.loaded[dest], Vim):  # Notice the Vim server
                self.loaded[dest].server.move(dest)

        if src in self.core.search.attached:  # Update attached list (search widget)
            self.core.search.attached.remove(src)
            self.core.search.attached.add(dest)

        if oid in self.pdb:  # Update the profiles database
            self.pdb[nid] = self.pdb.pop(oid)

        if dest in self.loaded:  # Update the message bar
            self.loaded[dest].folderLabel.update()
            self.loaded[dest].activateWindow()  # Restore window focus


class DropFilter(QtCore.QObject):
    mime = QtCore.pyqtSignal(object, object)

    def __init__(self):
        super().__init__()
        # This URL validator regular expression belongs to Django Software
        # Copyright (c) Django Software Foundation and individual contributors
        # Please read https://github.com/django/django/blob/master/LICENSE
        self.regex = re.compile(
            r"^(?:http|ftp)s?://"  # http:// or https://
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}(?<!-)\.?)|"  # domain
            r"localhost|"  # localhost
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|"  # ipv4
            r"\[?[A-F0-9]*:[A-F0-9:]+\]?)"  # ipv6
            r"(?::\d+)?"  # optional port
            r"(?:/?|[/?]\S+)\Z",
            re.IGNORECASE,
        )

    @QtCore.pyqtSlot(object, str)
    def filter(self, path: Path, url: str) -> Tuples.Mime:
        """Returns the type & content of a filesystem or web URL"""
        url = self._sanitize(url)
        mime = Tuples.Mime("invalid", url)
        pixmap = QtGui.QPixmap(url)

        if self._isImage(pixmap):
            mime = Tuples.Mime("image", pixmap)

        elif self._isWebURL(url):
            req = self._request(url)
            pixmap.loadFromData(req)
            if self._isImage(pixmap):
                mime = Tuples.Mime("image", pixmap)
        else:
            try:
                with open(url, encoding="utf-8") as f:
                    mime = Tuples.Mime("text", f.read())
            except (UnicodeDecodeError, IsADirectoryError, PermissionError, OSError):
                pass
        self.mime.emit(path, mime)

    def _isImage(self, pixmap: QtGui.QPixmap) -> bool:
        return not pixmap.isNull()

    def _isWebURL(self, url: str) -> bool:
        return re.match(self.regex, url) is not None

    def _request(self, url: str) -> bytes:
        """Extracts content from a web URL"""
        try:
            return requests.get(url, timeout=5).content
        except requests.exceptions.RequestException:
            log.exception(f"Could not retrieve URL content '{url}'")

    def _sanitize(self, text: str) -> str:
        """Replaces hex codes from a string"""
        # ie. Replace '%5B~%5D' to '[~]'
        # %\d{2}       Patterns starting with a %, followed by two digit
        # %\d[a-fA-F]  Patterns starting with a %, followed by one digit and one letter from a to F
        hexChars = re.findall(r"%\d{2}|%\d[a-fA-F]", text)
        for code in hexChars:
            litteral = code.replace("%", "0x")
            litteral = chr(eval(litteral))
            text = text.replace(code, litteral)
        return text


class TrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, core):
        super().__init__()
        self.core = core
        self.activated.connect(self._clickEvent)
        self.update()

        # Fires a timer until the tray is available
        self.timer = QtCore.QTimer(singleShot=True, interval=1000)
        self.timer.timeout.connect(self._show)
        self.timer.start(0)

    def update(self):
        """Update tray icon svg and color"""
        css = self.core.getNoteDecorationsCSS()
        color = QtGui.QColor(css["tray-icon"])
        if color.isValid():
            # Overrides color if set in global.css
            icon = self.core.colorize(self.core.icons["tray"], color)
        else:
            path = str(RootDirs.ICONS / "tray.svg")
            icon = QtGui.QIcon(path)

        # QIcon to QPixmap conversion for KDE compatibility bug - FIXME: Still relevant ?
        pixmap = icon.pixmap(64, 64)
        self.setIcon(QtGui.QIcon(pixmap))

    def _clickEvent(self, button: QtWidgets.QSystemTrayIcon.ActivationReason):
        """Handler for mouse events on the tray icon"""
        key = {
            QtWidgets.QSystemTrayIcon.Trigger: "left",
            QtWidgets.QSystemTrayIcon.MiddleClick: "middle",
        }.get(button)
        self.core.execute("tray", key)

    def _show(self):
        """Waits until the system tray is available"""
        if self.isSystemTrayAvailable():
            self.menu = CoreMenu(self.core)
            self.setContextMenu(self.menu)
            self.show()
        else:
            self.timer.start()


def main(args: Namespace):
    """Initializes the application"""
    app = QtWidgets.QApplication(sys.argv)
    app.setDesktopFileName(ID)
    app.setApplicationName(APP_NAME)
    app.setQuitOnLastWindowClosed(False)
    core = Core(app)
    core.bus = cli.QDBusObject(core)
    core.parser.fromNamespace(args)
    app.exec()


if __name__ == "__main__":
    main()
