from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QCoreApplication, QStringListModel
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QAbstractItemView
from AppModel import AppModel
from Sites import Sites

uiFile = "MainWindow.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(uiFile)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.appModel = AppModel()
        self.listViewModel = QStringListModel(self)
        self.info.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.initTable()
        self.initListSites()

        self.setConnections()

    def initListSites(self):
        for site in Sites:
            self.listViewModel.insertRow(self.listViewModel.rowCount())
            index = self.listViewModel.index(self.listViewModel.rowCount() - 1)
            self.listViewModel.setData(index, site.name)

        self.listSites.setModel(self.listViewModel)

    def initTable(self):
        self.info.setColumnCount(6)
        self.info.setHorizontalHeaderLabels(['Site', 'Author', 'Header', 'Url', 'Count comments', 'Count likes'])
        self.info.resizeColumnsToContents()

    def setConnections(self):
        self.actionExit.triggered.connect(QCoreApplication.instance().quit)
        self.actionAbout.triggered.connect(self.about)
        self.addNewArticleBtn.clicked.connect(self.parseSite)
        self.appModel.changeArticlesSignal.connect(self.onChangedArticled)

    def about(self):
        QMessageBox.about(self, "About", "Ametov Pavel\n8-T3O-302B-16")

    def error(self, message: str):
        box = QMessageBox()
        box.setWindowTitle("Error")
        box.setText(message)
        box.exec()

    def parseSite(self):
        try:
            index = self.listSites.currentIndex().row()
            numberArticle = self.numberArticle.text()

            if index == -1:
                raise Exception('Select site')

            try:
                numberArticle = int(numberArticle)
            except Exception as err:
                raise Exception("Incorrect value of article")

            site = Sites(index)

            self.appModel.parseSite(site, numberArticle)
        except Exception as err:
            self.error(err.args[0])

    def onChangedArticled(self):
        self.info.clear()
        self.initTable()

        articles = self.appModel.articlesModels

        self.info.setRowCount(len(articles))

        for index in range(len(articles)):

            article = articles[index]
            self.info.setItem(index, 0, QTableWidgetItem(article.site.name))
            self.info.setItem(index, 1, QTableWidgetItem(article.author))
            self.info.setItem(index, 2, QTableWidgetItem(article.header))
            self.info.setItem(index, 3, QTableWidgetItem(article.url))
            self.info.setItem(index, 4, QTableWidgetItem(str(article.countComments)))
            self.info.setItem(index, 5, QTableWidgetItem(str(article.countLikes)))

        self.info.resizeColumnsToContents()