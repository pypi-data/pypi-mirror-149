#!/usr/bin/python3
import argparse
from pathlib import Path
from PyQt5 import QtCore, QtDBus

try:
    from ..__id__ import ID
    from ..backend import DeepPath, UserDirs, logger
except (ValueError, ImportError):
    from __id__ import ID
    from backend import DeepPath, UserDirs, logger

log = logger.new(__name__)


def parser(argv: list) -> argparse.Namespace:
    """Setups the command line interface, validates and parses command line options"""
    parser = argparse.ArgumentParser(prog=ID, add_help=False, allow_abbrev=False)
    parser.add_argument("-h", "--help", action="store_true")
    parser.add_argument("-q", "--quit", action="store_true")
    parser.add_argument(
        "-v",
        "--verbose",
        action="store",
        choices=["debug", "info", "warning", "error", "critical", "quiet"],
    )
    parser.add_argument("-c", "--core", action="store", type=str, nargs="+", default=[])
    parser.add_argument("-n", "--note", action="store", type=str, nargs="+")
    parser.add_argument("-p", "--path", action="store", type=str, nargs=1)
    parser.add_argument(
        "-s", "--search", action="store", nargs="?", const="toggle", choices=["toggle", "show", "hide"]
    )
    parser.add_argument(
        "-r",
        "--reset",
        action="store",
        nargs="?",
        const="all",
        choices=["all", "profiles", "settings"],
    )
    args = parser.parse_args(argv)
    if args.note and args.path is None:
        parser.error("--note requires --path option")
    elif args.note and args.path:
        path = Path(args.path[0])
        if (UserDirs.NOTES / path).is_file():
            args.path[0] = UserDirs.NOTES / path
        elif not path.expanduser().is_file():
            parser.error(f"Invalid path '{path}'")

    if args.quit:
        args.core.append("quit")

    if args.verbose:
        from backend import logger
        logger.ConsoleHandler.VERBOSE = args.verbose.upper()
    return args


class QDBusObject(QtCore.QObject):
    def __init__(self, core):
        QtCore.QObject.__init__(self)
        self.__dbusAdaptor = QDBusServerAdapter(self, core)
        self.start()

    def start(self):
        """Initializes D-Bus session"""
        bus = QtDBus.QDBusConnection.sessionBus()
        bus.registerObject(f"/org/{ID}", self)
        bus.registerService(f"org.{ID}")
        return bus


class QDBusServerAdapter(QtDBus.QDBusAbstractAdaptor):
    QtCore.Q_CLASSINFO("D-Bus Interface", f"org.{ID}")
    QtCore.Q_CLASSINFO(
        "D-Bus Introspection",
        f'<interface name="org.{ID}">\n'
        '  <method name="ParseCommands">\n'
        '    <arg direction="in" type="a{s}" name="commands"/>\n'
        "  </method>\n"
        "</interface>\n",
    )

    def __init__(self, server, core):
        super().__init__(server)
        self.core = core

    @QtCore.pyqtSlot(list)
    def ParseCommands(self, argv: list):
        """Forwards the parsed arguments Namespace to the running instance"""
        args = QtCore.Q_ARG(object, parser(argv))
        QtCore.QMetaObject.invokeMethod(self.core.parser, "fromNamespace", QtCore.Qt.QueuedConnection, args)


class CommandParser(QtCore.QObject):
    def __init__(self, core):
        super().__init__()
        self.core = core

    def fromDict(self, args: dict):
        """Parses internal commands"""
        if "core" in args:  # cmd = {'core': ['new']}
            self._core(key for key in args["core"])

        if "note" in args:  # cmd = {'note': ['rename', 'Untitled 1.txt']}
            action, path = args["note"]
            path = DeepPath(path).expanduser()
            self._note([action], path)

    @QtCore.pyqtSlot(argparse.Namespace)
    def fromNamespace(self, args: argparse.Namespace):
        """Parses external commands received through the command line interface (case insensitive)"""
        if args.core:
            actions = [key.lower() for key in args.core]
            self._core(actions)

        if args.note:
            actions = [key.lower() for key in args.note]
            path = DeepPath(args.path[0]).expanduser()
            self._note(actions, path)

        if args.search:
            options = {"show": True, "hide": False, "toggle": None}
            self.core.searchToggle(options[args.search])

    def _core(self, cmd: list):
        """Handler for core actions"""
        for action in cmd:
            if action in self.core.actions.tray:
                action = self.core.actions.tray[action]
                log.info(f"Core : {action.label}")
                action.call()
            else:
                log.error(f"Invalid action '{action}'")

    def _note(self, cmd: list, path: DeepPath):
        """Handler for note actions"""
        if path not in self.core.loaded:
            self.core.notes.add(path)
        note = self.core.loaded[path]

        for action in cmd:
            try:
                action = note.actions[action]
                log.info(f"{note.id} : {action.label}")
                try:
                    action.call()
                except TypeError:
                    action.call(path)
            except KeyError:
                log.error(f"Invalid action '{action}'")
