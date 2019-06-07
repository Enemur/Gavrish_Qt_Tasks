from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QMessageBox
from src.Model.AppModel import AppModel
import os

uiFile = os.getcwd() + "/src/View/Widgets/LoginWidget/LoginWidget.ui"
Ui_Widget, QtBaseClass = uic.loadUiType(uiFile)


class LoginWidget(QWidget, Ui_Widget):
    successfully_login = pyqtSignal(str)
    cancel = pyqtSignal()

    def __init__(self, app_model: AppModel, parent=None):
        QWidget.__init__(self, parent=parent)
        Ui_Widget.__init__(self)

        self._appModel = app_model
        self.setupUi(self)

        self._set_connections()

    def _set_connections(self):
        self.loginButton.clicked.connect(self._on_login_button_clicked)
        self.cancelButton.clicked.connect(self._on_cancel_button_clicked)

    def _on_login_button_clicked(self):
        username = self.loginLE.text()

        if username == "" or\
                username == self._appModel.main_channel or\
                username in self._appModel.list_users:
            self.error("Incorrect username")
            return

        self.successfully_login.emit(username)

    def _on_cancel_button_clicked(self):
        self.cancel.emit()

    @staticmethod
    def error(message: str):
        box = QMessageBox()
        box.setWindowTitle("Error")
        box.setText(message)
        box.exec()
