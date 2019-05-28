from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMessageBox
from src.Presenter import Presenter

uiFile = "View/MainWindow/MainWindow.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(uiFile)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self._presenter = Presenter(self,
                                    self.listTablesView,
                                    self.actionConnectToDB,
                                    self.tablesTabs,
                                    self.actionSaveAsSql,
                                    self.actionSaveAsExcel,
                                    self.actionLoadFromSql,
                                    self.actionLoadFromExcel)

        self._set_connections()

    def _set_connections(self):
        self.actionExit.triggered.connect(QCoreApplication.instance().quit)
        self.actionAbout.triggered.connect(self.about)

    def about(self):
        QMessageBox.about(self, "About", "Ametov Pavel\n8-T3O-302B-16")
