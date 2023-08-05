# -*- coding: utf-8 -*-

# Copyright (c) 2020 - 2022 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing a dialog to show some plain text.
"""

from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtWidgets import QDialog, QDialogButtonBox

from .Ui_EricPlainTextDialog import Ui_EricPlainTextDialog


class EricPlainTextDialog(QDialog, Ui_EricPlainTextDialog):
    """
    Class implementing a dialog to show some plain text.
    """
    def __init__(self, title="", text="", parent=None):
        """
        Constructor
        
        @param title title of the window
        @type str
        @param text text to be shown
        @type str
        @param parent reference to the parent widget
        @type QWidget
        """
        super().__init__(parent)
        self.setupUi(self)
        
        self.copyButton = self.buttonBox.addButton(
            self.tr("Copy to Clipboard"),
            QDialogButtonBox.ButtonRole.ActionRole)
        self.copyButton.clicked.connect(self.on_copyButton_clicked)
        
        self.setWindowTitle(title)
        self.textEdit.setPlainText(text)
    
    @pyqtSlot()
    def on_copyButton_clicked(self):
        """
        Private slot to copy the text to the clipboard.
        """
        txt = self.textEdit.toPlainText()
        cb = QGuiApplication.clipboard()
        cb.setText(txt)
