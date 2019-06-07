import json
import pika
from PyQt5.QtCore import pyqtSignal, QObject

from src.Model.Actions import Actions


class RabbitMQConsumer(QObject):
    create_room = pyqtSignal(str)
    user_disconnected = pyqtSignal(str)
    user_connected = pyqtSignal(str)
    new_message_received = pyqtSignal(str, str, str, float)
    send_username = pyqtSignal()
    set_username = pyqtSignal(str)

    def __init__(self,
                 connection,
                 channel,
                 main_channel: str):
        super().__init__()
        # self._init_connection()

        self._connection = connection
        self._channel = channel

        self.username = ''
        self.main_channel = main_channel

        self._action_to_method = {
            Actions.Login: self._login_new_user,
            Actions.Disconnect: self._disconnect_user,
            Actions.NewMessage: self._new_message,
            Actions.GetUsersName: self._on_get_users_name,
            Actions.CreateNewChannel: self._create_new_channel,
            Actions.SendUserName: self._on_received_username,
        }

        self._add_new_channel(self.main_channel)

    def update_username(self, username):
        self.username = username

    def _init_connection(self):
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
        self._channel = self._connection.channel()

    def run(self):
        self._init_connection()
        self._add_new_channel(self.main_channel)
        self._channel.start_consuming()

    # region PrivateMethods

    def _add_new_channel(self, channel: str):
        self._channel.exchange_declare(exchange=channel, exchange_type='fanout')
        result = self._channel.queue_declare(queue='', durable=True)
        queue_name = result.method.queue
        self._channel.queue_bind(exchange=channel, queue=queue_name)
        self._channel.basic_consume(queue=queue_name, on_message_callback=self._callback)

    def _remove_channel(self, channel: str):
        self._channel.queue_delete(queue=channel)

    def _callback(self, ch, method, properties, body):
        data = json.loads(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)

        send_user = data.get('send_user')
        action = Actions(data.get('action'))

        if send_user == self.username:
            return

        self._action_to_method[action](send_user, data)

    def _login_new_user(self, send_user, data):
        self.user_connected.emit(send_user)

    def _disconnect_user(self, send_user, data):
        self.user_disconnected.emit(send_user)

        if send_user in self._user_to_channel:
            channel = self._user_to_channel.get(send_user)
            self._remove_channel(channel)

            self._user_to_channel.pop(send_user)

    def _create_room_with_user(self, send_user: str, data):
        with_user = data.get("with_user")
        if with_user == self.username:
            self.create_room.emit(send_user)

    def _new_message(self, send_user, data):
        message = data.get('message')
        time = data.get('time')
        to_room = data.get("room")

        if to_room != self.main_channel and to_room != self.username:
            return

        self.new_message_received.emit(send_user, to_room, message, time)

    def _create_new_channel(self, send_user, data):
        self.create_room.emit(send_user)

    def _on_get_users_name(self, send_user, data):
        self.send_username.emit()

    def _on_received_username(self, send_user, data):
        self.set_username.emit(send_user)

# endregion
