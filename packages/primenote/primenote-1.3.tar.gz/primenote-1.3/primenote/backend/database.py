#!/usr/bin/python3
import json
from copy import deepcopy
from pathlib import Path, PurePath
from typing import Tuple
from PyQt5 import QtCore, QtWidgets

try:
    from ..backend import configEnum, logger
    from ..backend.observer import Observer
except (ValueError, ImportError):
    from backend import configEnum, logger
    from backend.observer import Observer

log = logger.new(__name__)
REPAIR_EXCLUSIONS = ("key events",)


class AbstractDatabaseInterface:
    """Provides load and save methods to interface a dict key 'path'
    Converts a tuple to a nested dict key pointer; (k1, k2) -> dict[k1][k2]"""

    def __init__(self, db: dict, slices: Tuple):
        self.db = db
        self.slices = slices

    def _load(self) -> any:
        """Loads a database value"""
        value = self.db
        for s in self.slices:
            value = value.get(s)
        return value

    def _save(self, state: int):
        """Saves new value to database"""
        _db = self.db
        for key in self.slices[:-1]:
            _db = _db[key]
        _db[self.slices[-1]] = self.value()


class AutoCheckBox(AbstractDatabaseInterface, QtWidgets.QCheckBox):
    """Self loading/saving QCheckBox widget"""

    def __init__(self, text: str, db: dict, slices: Tuple):
        super(QtWidgets.QCheckBox, self).__init__(text)
        AbstractDatabaseInterface.__init__(self, db, slices)
        self.load()
        self.stateChanged.connect(self._save)

    def load(self):
        self.setChecked(self._load())

    def value(self) -> bool:
        return self.isChecked()


class AutoComboBox(AbstractDatabaseInterface, QtWidgets.QComboBox):
    """Self loading/saving QComboBox widget"""

    def __init__(self, db: dict, slices: Tuple):
        super(QtWidgets.QComboBox, self).__init__()
        AbstractDatabaseInterface.__init__(self, db, slices)
        self.load()
        self.currentTextChanged.connect(self._save)

    def load(self):
        self.setCurrentText(self._load())

    def value(self) -> str:
        return self.currentText()


class AutoFontComboBox(AbstractDatabaseInterface, QtWidgets.QFontComboBox):
    """Self loading/saving QFontComboBox widget"""

    def __init__(self, db: dict, slices: Tuple):
        super(QtWidgets.QFontComboBox, self).__init__()
        AbstractDatabaseInterface.__init__(self, db, slices)
        self.load()
        self.currentTextChanged.connect(self._save)

    def load(self):
        self.setCurrentText(self._load())

    def value(self) -> str:
        return self.currentText()


class AutoComboBoxGlob(AbstractDatabaseInterface, QtWidgets.QComboBox):
    """Self loading/saving QComboBox widget"""

    def __init__(self, db: dict, slices: Tuple, type_: str):
        super(QtWidgets.QComboBox, self).__init__()
        AbstractDatabaseInterface.__init__(self, db, slices)

        files = configEnum(type_)
        self.nameToStem = {str(f.name): f.stem.title() for f in files}
        self.stemToName = {f.stem.title(): str(f.name) for f in files}
        self.addItems(sorted([f.stem.title() for f in files]))
        self.load()
        self.currentTextChanged.connect(self._save)

    def load(self):
        try:
            stem = self.nameToStem[self._load()]
            self.setCurrentText(stem)
        except KeyError:
            log.error(f"'{self._load()}' not found")

    def value(self) -> str:
        name = self.stemToName[self.currentText()]
        return name


class AutoLineEdit(AbstractDatabaseInterface, QtWidgets.QLineEdit):
    """Self loading/saving QLineEdit widget"""

    def __init__(self, db: dict, slices: Tuple):
        super(QtWidgets.QLineEdit, self).__init__()
        AbstractDatabaseInterface.__init__(self, db, slices)
        self.load()
        self.textEdited.connect(self._save)

    def load(self):
        self.setText(self._load())

    def value(self) -> str:
        return self.text()


class AutoDoubleSpinBox(AbstractDatabaseInterface, QtWidgets.QDoubleSpinBox):
    """Self loading/saving QDoubleSpinBox widget"""

    def __init__(self, db: dict, slices: Tuple):
        super(QtWidgets.QDoubleSpinBox, self).__init__()
        AbstractDatabaseInterface.__init__(self, db, slices)
        self.setMaximum(1)
        self.setSingleStep(0.1)
        self.load()
        self.valueChanged.connect(self._save)

    def load(self) -> float:
        self.setValue(self._load())


class AutoSpinBox(AbstractDatabaseInterface, QtWidgets.QSpinBox):
    """Self loading/saving QSpinBox widget"""

    def __init__(self, db: dict, slices: Tuple):
        super(QtWidgets.QSpinBox, self).__init__()
        AbstractDatabaseInterface.__init__(self, db, slices)
        self.setMaximum(9999)
        self.load()
        self.valueChanged.connect(self._save)

    def load(self) -> int:
        self.setValue(self._load())


class Database(Observer):
    def __init__(self, path: Path, default: dict):
        self.timer = QtCore.QTimer(singleShot=True, interval=5000)
        self.timer.timeout.connect(self.save)
        super().__init__(self, callback=self.timer.start)
        self.path = path
        self.name = path.stem
        self.default = default
        self._setup()

    def save(self):
        """Saves dict content to JSON"""
        self.timer.stop()
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                f.write(json.dumps(self, indent=2, sort_keys=False, cls=self.SetEncoder))
            log.info(f"Saved {self.name} database")
        except PermissionError:
            log.error(f"Could not save {self.name} database")

    def _load(self):
        """Loads JSON file content"""
        with open(self.path, encoding="utf-8") as f:
            self.update(json.load(f))
        log.info(f"Loaded {self.name} database")

    def _repair(self, db, default):
        """Repairs missing keys and type inconsistencies"""
        for key, value in default.items():
            if isinstance(value, dict):
                db.setdefault(key, value)
                if key not in REPAIR_EXCLUSIONS:
                    self._repair(db[key], value)
            else:
                db.setdefault(key, value)
            if not isinstance(db[key], type(value)):
                log.warning(f"Fixed type for '{key}': {type(db[key])} to {type(value)}")
                db[key] = default.get(key)

    def _setup(self):
        if self.path.is_file() and self.path.stat().st_size > 0:
            self._load()
            self._validate()
        else:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.update(deepcopy(self.default))
            with open(self.path, "w", encoding="utf-8") as f:
                f.write(json.dumps(self, indent=2, sort_keys=False))
            log.info(f"Created {self.name} database '{self.path}'")

    def _validate(self):
        """Saves repairs to file (if any)"""
        old = json.dumps(self, sort_keys=True)
        default = deepcopy(self.default)
        self._repair(self, default)
        new = json.dumps(self, sort_keys=True)
        if not new == old:
            log.warning(f"Repaired missing keys in {self.name} database")
            self.save()

    class SetEncoder(json.JSONEncoder):
        def default(self, obj):
            """Converts sets and Paths"""
            if isinstance(obj, set):
                return list(obj)
            elif isinstance(obj, Path) or isinstance(obj, PurePath):
                return str(obj)
            return json.JSONEncoder.default(self, obj)
