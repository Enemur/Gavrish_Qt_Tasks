import pika
from PyQt5.QtCore import QObject, pyqtSignal, QThread

from src.Model.RabbitMQConsumer import RabbitMQConsumer
from src.Model.RabbitMQPublisher import RabbitMQPublisher


class AppModel(QObject):
    users_updated = pyqtSignal()
    new_message_received = pyqtSignal(str, str, str, float)
    create_room_with_user = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.main_channel = 'main_channel'
        self.mute_users = []
        self.username = ''

        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
        channel = connection.channel()

        self._rabbitMQConsumer = RabbitMQConsumer(connection, channel, self.main_channel)
        self._rabbitMQPublisher = RabbitMQPublisher(connection, channel, self.main_channel)

        self.list_users = []
        self._thread = QThread()

        self._rabbitMQConsumer.moveToThread(self._thread)
        self._set_connections()
        self._thread.started.connect(self._rabbitMQConsumer.run)
        self._thread.start()

        self._rabbitMQPublisher.get_users()

    def _set_connections(self):
        self._rabbitMQConsumer.user_connected.connect(self._user_connected)
        self._rabbitMQConsumer.user_disconnected.connect(self._user_disconnected)
        self._rabbitMQConsumer.send_username.connect(self._send_user_name)
        self._rabbitMQConsumer.new_message_received.connect(self._new_message_received)
        self._rabbitMQConsumer.create_room.connect(self._create_room_with_user)
        self._rabbitMQConsumer.set_username.connect(self._set_user)

    def mute(self, username):
        if username in self.mute_users:
            self.mute_users.remove(username)
        else:
            self.mute_users.append(username)
        self.users_updated.emit()

    def login_user(self, username):
        self.username = username
        self._rabbitMQConsumer.update_username(username)
        self._rabbitMQPublisher.login_user(username)

    def disconnect(self):
        self._rabbitMQPublisher.disconnect_user()

    def send_message_to_room(self, room, message, time):
        self._rabbitMQPublisher.send_message_to_room(room, message, time)

    def create_room(self, user):
        self._rabbitMQPublisher.create_room_with_user(user)

    def _user_connected(self, username):
        self.list_users.append(username)
        self.users_updated.emit()

    def _user_disconnected(self, username):
        self.list_users.remove(username)
        self.users_updated.emit()

    def _set_user(self, username):
        if username not in self.list_users:
            self.list_users.append(username)

    def _send_user_name(self):
        self._rabbitMQPublisher.send_username(self.username)

    def _new_message_received(self, send_user, to_room, message, time):
        if to_room != self.main_channel and send_user in self.mute_users:
            return

        self.new_message_received.emit(send_user, to_room, message, time)

    def _create_room_with_user(self, send_user):
        self.create_room_with_user.emit(send_user)

    def __del__(self):
        self.disconnect()
