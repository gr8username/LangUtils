import re
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from anki import hooks
from aqt import gui_hooks
from aqt.utils import showInfo, qconnect
from aqt import mw
from aqt.qt import *
import aqt
import FieldReaderHandler
import subprocess

def add_editor_buttons(buttons, editor):
    addMe = editor.addButton(None, "LangUtils", FieldReaderHandler.translate_addon_button_clicked, tip="LangUtils")
    buttons.append(addMe)

def main():
    aqt.gui_hooks.editor_did_init_buttons.append(add_editor_buttons)

main()
