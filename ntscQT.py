import os
import sys
from pathlib import Path

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QLibraryInfo
from PyQt5.QtCore import QFile, QTextStream

from app import NtscApp
from app import logger

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QLibraryInfo.location(
    QLibraryInfo.PluginsPath
)

def crash_handler(type, value, tb):
    logger.trace(value)
    logger.exception("Uncaught exception: {0}".format(str(value)))
    sys.exit(1)

# Install exception handler
sys.excepthook = crash_handler

def main():
    translator = QtCore.QTranslator()
    locale = QtCore.QLocale.system().name()

    print("ntscQT by JargeZ")

    # if run by pyinstaller executable, frozen attr will be true
    if getattr(sys, 'frozen', False):
        # _MEIPASS contain temp pyinstaller dir
        base_dir = Path(sys._MEIPASS)
        locale_file = str((base_dir / 'translate' / f'{locale}.qm').resolve())
    else:
        base_dir = Path(__file__).absolute().parent
        locale_file = str((base_dir / 'translate' / f'{locale}.qm').resolve())

    print(f"Try load {locale} locale: {locale_file}")
    if translator.load(locale_file):
        print(f'Localization loaded: {locale}')  # name, dir
    else:
        print("Using default translation")

    app = QtWidgets.QApplication(sys.argv)
    app.installTranslator(translator)

    # Always apply dark mode palette
    dark_palette = QtGui.QPalette()

    # Set dark background color
    dark_palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
    dark_palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
    dark_palette.setColor(QtGui.QPalette.Base, QtGui.QColor(42, 42, 42))
    dark_palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(66, 66, 66))
    dark_palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
    dark_palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
    dark_palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
    dark_palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
    dark_palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
    dark_palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)

    # Highlight colors
    dark_palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(142, 45, 197).lighter())
    dark_palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)

    app.setPalette(dark_palette)

    window = NtscApp()
    window.show()
    sys.exit(app.exec_())

