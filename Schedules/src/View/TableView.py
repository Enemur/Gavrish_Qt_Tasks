from PyQt5 import QtSql
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTableView

from src.Model.DataBaseWorker import DataBaseTables


class TableView(QWidget):
    def __init__(self, table_name: str, parent=None):
        super().__init__()
        self.parent = parent

        self.model = QtSql.QSqlRelationalTableModel(parent)
        self.model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.model.setTable(table_name)

        self._init_relations(table_name)

        self.model.select()

        self.view = QTableView(parent)
        self.view.setModel(self.model)
        if table_name == 'schedule' or table_name == 'subjects':
            self.view.setItemDelegate(QtSql.QSqlRelationalDelegate(self.view))

        self.view.resizeColumnsToContents()
        self.view.verticalHeader().setVisible(False)

    def _init_relations(self, table_name: str):
        if table_name == DataBaseTables.Schedule.value:
            self.model.setRelation(
                1,
                QtSql.QSqlRelation(
                    "groups",
                    "id",
                    "name"
                )
            )

            self.model.setHeaderData(
                1,
                Qt.Horizontal,
                'groups.name'
            )

            self.model.setRelation(
                3,
                QtSql.QSqlRelation(
                    "subjects",
                    "id",
                    "name"
                )
            )

            self.model.setHeaderData(
                3,
                Qt.Horizontal,
                'subjects.name'
            )

        elif table_name == DataBaseTables.Subjects.value:
            self.model.setRelation(
                2,
                QtSql.QSqlRelation(
                    "lectures",
                    "id",
                    "name"
                )
            )

            self.model.setHeaderData(
                2,
                Qt.Horizontal,
                'lectures.name'
            )

            self.model.setRelation(
                4,
                QtSql.QSqlRelation(
                    "teachers",
                    "id",
                    "name"
                )
            )

            self.model.setHeaderData(
                4,
                Qt.Horizontal,
                'teachers.name'
            )

