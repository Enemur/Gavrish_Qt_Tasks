import os

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMessageBox

from src.Model.AppModel import AppModel
from src.View.Widgets.LoginWidget.LoginWidget import LoginWidget
from src.View.Widgets.MainWidget.MainWidget import MainWidget

uiFile = os.getcwd() + "/src/View/MainWindow.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(uiFile)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self._appModel = AppModel()
        self._login_widget = LoginWidget(self._appModel)
        self._main_widget = MainWidget(self._appModel)
        self.destroyed.connect(self._on_distroed)

        self._set_widgets()
        self.stackedWidget.setCurrentWidget(self._login_widget)

        self._set_connections()

    def _on_distroed(self):
        self._appModel.disconnect()

    def _set_widgets(self):
        self.stackedWidget.addWidget(self._login_widget)
        self.stackedWidget.addWidget(self._main_widget)

    def _set_connections(self):
        self.actionExit.triggered.connect(QCoreApplication.instance().quit)
        self.actionAbout.triggered.connect(self.about)

        self._login_widget.successfully_login.connect(self._on_successfully_login)
        self._login_widget.cancel.connect(self._on_cancel)

    def _on_successfully_login(self, username: str):
        self.stackedWidget.setCurrentWidget(self._main_widget)
        self._appModel.login_user(username)
        self.setWindowTitle(username)

    def _on_cancel(self):
        self._appModel.disconnect()
        QCoreApplication.instance().quit()

    def about(self):
        QMessageBox.about(self, "About", "Ametov Pavel\n8-T3O-302B-16")

    @staticmethod
    def error(message: str):
        box = QMessageBox()
        box.setWindowTitle("Error")
        box.setText(message)
        box.exec()