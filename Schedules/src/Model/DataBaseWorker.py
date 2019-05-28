from enum import Enum

from PyQt5 import QtSql
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtSql import QSqlDatabase, QSqlError

from src.Model import Subject, Schedule
from src.Model.DataBasesEnum import DataBasesEnum


class DataBaseTables(Enum):
    Teachers = "teachers"
    Subjects = "subjects"
    Schedule = "schedule"
    Groups = "groups"
    Lectures = "lectures"


class DataBaseWorker(QObject):
    tables_updated = pyqtSignal()

    def __init__(self, _db: QSqlDatabase):
        super().__init__()
        self._db = _db

    def connect_to_database(self, config: {}):
        database = ""
        if config["database_driver"] == DataBasesEnum.Mysql:
            database = "QMYSQL"
        elif config["database_driver"] == DataBasesEnum.Sqlite:
            database = "QSQLITE"

        self._db = QtSql.QSqlDatabase.addDatabase(database)

        if config.get("database") is not None:
            self._db.setDatabaseName(config["database"])

        if config.get("host") is not None:
            self._db.setHostName(config["host"])

        if config.get("port") is not None:
            self._db.setPort(config["port"])

        if config.get("username") is not None:
            self._db.setUserName(config["username"])

        if config.get("password") is not None:
            self._db.setPassword(config["password"])

        is_open = self._db.open()

        if is_open:
            self.tables_updated.emit()

        return is_open

    @staticmethod
    def _check_error(err: QSqlError):
        if not err.isValid():
            return False
        elif err.type() == QtSql.QSqlError.TransactionError:
            raise Exception(f"Transaction error: {err.text()}")
        elif err.type() == QtSql.QSqlError.StatementError:
            raise Exception(f"Statement error: {err.text()}")
        else:
            raise Exception(f"Unknown error: {err.text()}")

    def get_tables(self) -> [str]:
        if self._db.isOpen():
            return self._db.tables()
        return []

    def _add_to_table(self, table, data: dict):
        if table not in self._db.tables():
            raise Exception(f"Unknown table: {table}")

        self._db.transaction()
        query = QtSql.QSqlQuery(self._db)

        keys = ",".join([f"{item}" for item in data.keys()])
        values = ",".join([f"'{item}'" for item in data.values()])

        sql = f"INSERT INTO {table} (id, {keys}) VALUES (NULL, {values})"

        query.exec(sql)
        self._check_error(query.lastError())
        self._db.commit()

    def _get_id(self, table: str, data: dict):
        if table not in self._db.tables():
            return -1

        query = QtSql.QSqlQuery(self._db)

        conditions = []
        for key in data:
            value = data[key]
            conditions.append(f"{key} = '{value}'")

        condition = " and ".join(conditions)

        sql = f"SELECT * FROM {table} WHERE {condition}"

        query.exec(sql)
        self._check_error(query.lastError())

        if query.next():
            return query.value(0)
        else:
            return -1

    def add_new_group(self, name: str):
        data = {
            "name": name
        }
        self._add_to_table(DataBaseTables.Groups.value, data)

    def add_new_teacher(self, name: str):
        data = {
            "name": name
        }
        self._add_to_table(DataBaseTables.Teachers.value, data)

    def add_new_lecture(self, name: str):
        data = {
            "name": name
        }
        self._add_to_table(DataBaseTables.Lectures.value, data)

    def add_new_subject(self, subject: Subject):
        if DataBaseTables.Subjects.value not in self._db.tables():
            raise Exception(f"Unknown table: {DataBaseTables.Subjects.value}")

        teacherId = self._get_id(DataBaseTables.Teachers.value, {"name": subject.teacher})
        if teacherId == -1:
            raise Exception("Unknown teacher")

        lectureId = self._get_id(DataBaseTables.Lectures.value, {"name": subject.lecture})
        if lectureId == -1:
            raise Exception("Unknown lecture")

        data = {
            "name": subject.name,
            "lectureId": lectureId,
            "type": subject.typeSubject,
            "teacherId": teacherId
        }

        self._add_to_table(DataBaseTables.Subjects.value, data)

    def add_new_schedule(self, schedule: Schedule):
        if DataBaseTables.Schedule.value not in self._db.tables():
            raise Exception(f"Unknown table: {DataBaseTables.Schedule.value}")

        groupId = self._get_id(DataBaseTables.Groups.value, {"name": schedule.groupName})
        if groupId == -1:
            self.add_new_group(schedule.groupName)
            groupId = self._get_id(DataBaseTables.Groups.value, {"name": schedule.groupName})

        teacherId = self._get_id(DataBaseTables.Teachers.value, {"name": schedule.subject.teacher})
        if teacherId == -1:
            self.add_new_teacher(schedule.subject.teacher)
            teacherId = self._get_id(DataBaseTables.Teachers.value, {"name": schedule.subject.teacher})

        lectureId = self._get_id(DataBaseTables.Lectures.value, {"name": schedule.subject.lecture})
        if lectureId == -1:
            self.add_new_lecture(schedule.subject.lecture)
            lectureId = self._get_id(DataBaseTables.Lectures.value, {"name": schedule.subject.lecture})

        data = {
            "name": schedule.subject.name,
            "lectureId": lectureId,
            "type": schedule.subject.typeSubject,
            "teacherId": teacherId
        }

        subjectId = self._get_id(DataBaseTables.Subjects.value, data)
        if subjectId == -1:
            self.add_new_subject(schedule.subject)
            subjectId = self._get_id(DataBaseTables.Subjects.value, data)

        data = {
            "idGroup": groupId,
            "numberOfWeek": schedule.numberOfWeek,
            "subjectId": subjectId,
            "day": schedule.day,
            "numberOfSubject": schedule.numberOfSubject
        }

        scheduleId = self._get_id(DataBaseTables.Schedule.value, data)
        if scheduleId == -1:
            self._add_to_table(DataBaseTables.Schedule.value, data)

    def execute_sql(self, sql: str):
        self._db.transaction()
        query = QtSql.QSqlQuery(self._db)
        query.exec(sql)
        self._check_error(query.lastError())

    def is_connected(self) -> bool:
        return self._db.isOpen()

    def get_database_name(self):
        return self._db.databaseName()