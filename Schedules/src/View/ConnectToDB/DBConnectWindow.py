from enum import Enum

from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFileDialog

from src.Model.DataBasesEnum import DataBasesEnum

uiFile = "View/ConnectToDB/DBConnectWindow.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(uiFile)


class DBConnectWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    cancelButtonClicked = pyqtSignal()
    connectButtonClicked = pyqtSignal(dict)

    def __init__(self, parent):
        QtWidgets.QMainWindow.__init__(self, parent)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.hostLE.setText("localhost")
        self._set_connections()

    def _set_connections(self):
        self.cancelButton.clicked.connect(self._on_cancel_button_clicked)
        self.connectButton.clicked.connect(self._on_connect_button_clicked)

        self.sqliteSelectDatabase.clicked.connect(self._on_select_database_clicked)

    def _on_select_database_clicked(self):
        file_path = QFileDialog.getOpenFileName(self, "Select database", "/home//pavel", "*db")[0]
        self.sqliteDataBaseLE.setText(file_path)

    def _on_cancel_button_clicked(self):
        self.cancelButtonClicked.emit()

    def _on_connect_button_clicked(self):
        index = self.databasesTabs.currentIndex()
        database_driver = DataBasesEnum(index)

        configuration = {"database_driver": database_driver}

        if database_driver == DataBasesEnum.Mysql:
            host = self.hostLE.text()
            port = int(self.portLE.text())
            username = self.usernameLE.text()
            password = self.passwordLE.text()
            database = self.databaseNameLE.text()

            configuration = {
                "host": host,
                "port": port,
                "username": username,
                "password": password,
                "database": database,
                "database_driver": database_driver
            }
        elif database_driver == DataBasesEnum.Sqlite:
            database = self.sqliteDataBaseLE.text()
            configuration = {
                "database": database,
                "database_driver": database_driver
            }

        self.connectButtonClicked.emit(configuration)
