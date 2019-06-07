import json
from datetime import datetime

import pika
from PyQt5.QtCore import pyqtSignal, QObject

from src.Model.Actions import Actions


class RabbitMQPublisher(QObject):
    create_room = pyqtSignal(str)
    user_disconnected = pyqtSignal(str)
    user_connected = pyqtSignal(str)
    new_message_received = pyqtSignal(str, str, str, float)
    set_user = pyqtSignal(str)

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
        self._add_new_channel(self.main_channel)

    def _init_connection(self):
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
        self._channel = self._connection.channel()

# region PublicMethods

    def login_user(self, username):
        self.username = username

        data = {
            "send_user": self.username,
            "action": Actions.Login.value,
            "time": datetime.timestamp(datetime.now())
        }

        data = json.dumps(data)
        self._send_message_to_channel(self.main_channel, data)

    def disconnect_user(self):
        data = {
            "send_user": self.username,
            "action": Actions.Disconnect.value,
            "time": datetime.timestamp(datetime.now())
        }
        data = json.dumps(data)

        self._send_message_to_channel(self.main_channel, data)
        self._remove_channel(self.main_channel)

    def send_message_to_room(self, room, message, time):
        data = {
            "send_user": self.username,
            "action": Actions.NewMessage.value,
            "message": message,
            "time": time,
            "room": room
        }
        data = json.dumps(data)
        self._send_message_to_channel(self.main_channel, data)

    def send_username(self, username):
        data = {
            "send_user": username,
            'action': Actions.SendUserName.value,
        }
        data = json.dumps(data)
        self._send_message_to_channel(self.main_channel, data)

    def create_room_with_user(self, with_user):
        data = {
            "send_user": self.username,
            "action": Actions.CreateNewChannel.value,
            "with_user": with_user
        }
        data = json.dumps(data)
        self._send_message_to_channel(self.main_channel, data)

    def get_users(self):
        data = {
            'action': Actions.GetUsersName.value,
        }
        data = json.dumps(data)
        self._send_message_to_channel(self.main_channel, data)
# endregion

# region PrivateMethods

    def _send_message_to_channel(self, channel: str, data: str):
        self._channel.basic_publish(exchange=channel,
                                    routing_key='', body=data,
                                    properties=pika.BasicProperties(delivery_mode=2))

    def _add_new_channel(self, channel: str):
        self._channel.exchange_declare(exchange=channel, exchange_type='fanout')

    def _remove_channel(self, channel: str):
        self._channel.queue_delete(queue=channel)
# endregion
