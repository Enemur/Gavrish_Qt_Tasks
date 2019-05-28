import operator

from PyQt5.QtCore import QObject, QStringListModel, QItemSelection, QModelIndex
from PyQt5.QtSql import QSqlRelationalTableModel, QSqlRelationalDelegate
from PyQt5.QtWidgets import QAbstractItemView, QMessageBox, QTableView, QListView, QAction, QTabWidget, QFileDialog
from openpyxl.worksheet.table import Table
from openpyxl.worksheet.worksheet import Worksheet

from src.Model.AppModel import AppModel
from src.View.ConnectToDB.DBConnectWindow import DBConnectWindow
from src.View.MainWindow import MainWindow
from src.View.TableView import TableView


class Presenter(QObject):
    def __init__(self,
                 window: MainWindow,
                 listTablesView: QListView,
                 actionConnectToDB: QAction,
                 tablesTabs: QTabWidget,
                 actionSaveAsSql: QAction,
                 actionSaveAsExcel: QAction,
                 actionLoadFromSql: QAction,
                 actionLoadFromExcel: QAction):
        super().__init__()

        self.window = window
        self.listTablesView = listTablesView
        self.actionConnectToDB = actionConnectToDB
        self.tablesTabs = tablesTabs

        self.actionSaveAsSql = actionSaveAsSql
        self.actionSaveAsExcel = actionSaveAsExcel
        self.actionLoadFromSql = actionLoadFromSql
        self.actionLoadFromExcel = actionLoadFromExcel

        self._appModel = AppModel()
        self._init_list_view()

        self._listViewIndexToTabIndex = {}

        self._dbConnectWindow = DBConnectWindow(self.window)

        self._set_connections()

    def _set_connections(self):
        self.listTablesView.selectionModel().selectionChanged.connect(self._on_selection_changed)
        self.actionConnectToDB.triggered.connect(self._show_connect_db_window)
        self._dbConnectWindow.connectButtonClicked.connect(self._on_action_connect_to_db_triggered)
        self._dbConnectWindow.cancelButtonClicked.connect(self._on_cancel_connect_clicked)
        self._appModel.tables_updated.connect(self._tables_updated)

        self.actionSaveAsSql.triggered.connect(self._on_action_save_as_sql_triggered)
        self.actionSaveAsExcel.triggered.connect(self._on_action_save_as_excel_triggered)
        #self.actionLoadFromSql.triggered.connect(self._on_action_load_from_sql_triggered)
        self.actionLoadFromExcel.triggered.connect(self._on_action_load_from_excel_triggered)

    def _init_list_view(self):
        self.tableListModel = QStringListModel(self)
        self.listTablesView.setModel(self.tableListModel)
        self.listTablesView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableListModel.setStringList(self._appModel.get_tables())

    def _tables_updated(self):
        self.tableListModel.setStringList(self._appModel.get_tables())

    def _show_connect_db_window(self):
        self._dbConnectWindow.show()

    def _on_cancel_connect_clicked(self):
        self._dbConnectWindow.close()

    def _on_action_connect_to_db_triggered(self, configuration):
        is_connection_successfully = self._appModel.connect_to_db(configuration)

        if is_connection_successfully:
            self._dbConnectWindow.close()

    def _create_new_tab(self, table_name: str) -> TableView:
        return TableView(table_name, self.window)

    def update_tabs(self):
        self.tablesTabs.clear()
        tables = self._appModel.get_tables()

        for key, value in sorted(self._listViewIndexToTabIndex.items(), key=lambda item: (item[1], item[0])):
            table = tables[value]
            new_tab = self._create_new_tab(table)
            self.tablesTabs.addTab(new_tab.view, table)

    def _on_selection_changed(self, selection: QItemSelection):
        if len(selection.indexes()) != 0:
            modelIndex: QModelIndex = selection.indexes()[0]
            index = modelIndex.row()
            tables = self._appModel.get_tables()
            if index not in self._listViewIndexToTabIndex:
                table_name = tables[index]
                new_tab = self._create_new_tab(table_name)
                self.tablesTabs.addTab(new_tab.view, table_name)
                self._listViewIndexToTabIndex[index] = self.tablesTabs.count() - 1

            self.tablesTabs.setCurrentIndex(self._listViewIndexToTabIndex[index])

    @staticmethod
    def error(message: str):
        box = QMessageBox()
        box.setWindowTitle("Error")
        box.setText(message)
        box.exec()

    def _on_action_load_from_excel_triggered(self):
        file_path = QFileDialog.getOpenFileName(self.window, "Open excel", "/home/pavel", "*.xls *.xlsx *.xlsm "
                                                                                              "*.xlsb")[0]

        try:
            workbook = self._appModel.load_workbook(file_path)
            schedules = self._appModel.load_data_from_workbook(workbook)
            self._appModel.add_schedules_to_database(schedules)
            self.update_tabs()
        except Exception as error:
            self.error(str(error))

    def _on_action_load_from_sql_triggered(self):
        file_path = QFileDialog.getOpenFileName(self.window, "Open sql", "/home/pavel", "*.sql")[0]
        try:
            if file_path == "":
                raise Exception("Incorrect file path")
            self._appModel.load_database_from_sql(file_path)
        except Exception as error:
            self.error(str(error))

    def _on_action_save_as_sql_triggered(self):
        file_path = QFileDialog.getSaveFileName(self.window, "Save sql", "/home/pavel", "*.sql")[0]
        try:
            if file_path == "":
                raise Exception("Incorrect file path")
            self._appModel.export_database_to_sql(file_path)
        except Exception as error:
            self.error(str(error))

    def _on_action_save_as_excel_triggered(self):
        file_path = QFileDialog.getSaveFileName(self.window, "Save excel", "/home/pavel", "*.xls *.xlsx *.xlsm "
                                                                                              "*.xlsb")[0]
        try:
            if file_path == "":
                raise Exception("Incorrect file path")

        except Exception as error:
            self.error(str(error))
