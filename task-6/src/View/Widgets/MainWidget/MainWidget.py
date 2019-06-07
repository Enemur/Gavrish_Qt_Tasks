import os
from builtins import set
from datetime import datetime
from PyQt5 import uic
from PyQt5.QtCore import QItemSelection, QModelIndex
from PyQt5.QtWidgets import QWidget, QListWidget
from src.Model.AppModel import AppModel

uiFile = os.getcwd() + "/src/View/Widgets/MainWidget/MainWidget.ui"
Ui_Widget, QtBaseClass = uic.loadUiType(uiFile)


class MainWidget(QWidget, Ui_Widget):

    def __init__(self, app_model: AppModel, parent=None):
        QWidget.__init__(self, parent=parent)
        Ui_Widget.__init__(self)

        self._appModel = app_model
        self.setupUi(self)

        self._current_room = self._appModel.main_channel
        self.listUsers.addItems(self._appModel.list_users)

        self.tab_index_to_user_index = {}
        self._room_to_tab = {self._appModel.main_channel: self.mainRoomMessages}

        self._set_connections()

    def _set_connections(self):
        self.sendButton.clicked.connect(self._on_send_button_clicked)
        self.listUsers.selectionModel().selectionChanged.connect(self._on_user_selected)
        self.listUsers.itemDoubleClicked.connect(self._on_list_users_double_clicked)

        self._appModel.new_message_received.connect(self._on_new_message_received)
        # self._appModel.user_disconnected.connect(self._on_user_disconnected)
        self._appModel.users_updated.connect(self._on_updated_users)
        # self._appModel.user_connected.connect(self._on_user_connected)
        self._appModel.create_room_with_user.connect(self._create_room_with_user)

        self.chatroomsTabs.currentChanged.connect(self._on_current_room_changed)

    def _on_updated_users(self):
        self.listUsers.clear()
        users = self._appModel.list_users
        mutes = self._appModel.mute_users

        for user in users:
            tmp = ""
            if user in mutes:
                tmp = " - muted"
            self.listUsers.addItem(f'{user}{tmp}')

    def _on_list_users_double_clicked(self, item):
        index = self.listUsers.row(item)
        user = self._appModel.list_users[index]
        self._appModel.mute(user)

    def _on_current_room_changed(self, index):
        if index == 0:
            self._current_room = self._appModel.main_channel
        else:
            self._current_room = self._appModel.list_users[self.tab_index_to_user_index[index - 1]]

    def _create_room_with_user(self, room):
        tab = self._create_new_tab(room)
        self._room_to_tab[room] = tab
        self.chatroomsTabs.addTab(tab, room)
        self.tab_index_to_user_index[len(self.tab_index_to_user_index)] = self._appModel.list_users.index(room)

    def _on_send_button_clicked(self):
        message = self.messageLE.text()

        if message == "":
            return

        time = datetime.timestamp(datetime.now())
        self._appModel.send_message_to_room(self._current_room, message, time)
        tab = self._room_to_tab[self._current_room]

        if self._current_room != self._appModel.main_channel:
            tab.addItem(f"[{datetime.fromtimestamp(time)}]: User: {self._appModel.username} send message to {self._current_room}: {message}")
        else:
            tab.addItem(f"[{datetime.fromtimestamp(time)}]: User: {self._appModel.username} send message: {message}")

    def _create_new_tab(self, user):
        tab = QListWidget(self.chatroomsTabs)
        tab.setWindowTitle(user)
        return tab

    def _on_user_selected(self, selection: QItemSelection):
        if len(selection.indexes()) != 0:
            model_index: QModelIndex = selection.indexes()[0]
            index = model_index.row()

            room = self._appModel.list_users[index]

            if index not in self.tab_index_to_user_index.values():
                self._appModel.create_room(room)
                tab = self._create_new_tab(room)
                self._room_to_tab[room] = tab
                self.chatroomsTabs.addTab(tab, room)
                self.tab_index_to_user_index[len(self.tab_index_to_user_index)] =\
                    self._appModel.list_users.index(room)

            self.room = room

    def _on_new_message_received(self, send_user, room, message, time):
        if room == self._appModel.main_channel:
            tab = self._room_to_tab[room]
        else:
            tab = self._room_to_tab[send_user]

        if room != self._appModel.main_channel:
            tab.addItem(f"[{datetime.fromtimestamp(time)}]: User: {send_user} send message to {self._appModel.username}: {message}")
        else:
            tab.addItem(f"[{datetime.fromtimestamp(time)}]: User: {send_user} send message: {message}")

    def _on_user_disconnected(self, username: str):
        self.listUsers.clear()
        users = self._appModel.list_users
        self.listUsers.addItems(users)

    def _on_user_connected(self, username: str):
        self.listUsers.addItem(username)
