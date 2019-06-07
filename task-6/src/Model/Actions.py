from enum import Enum


class Actions(Enum):
    Login = 'login'
    Disconnect = 'disconnect'
    CreateNewChannel = 'create_new_channel'
    NewMessage = 'new_message'
    GetUsersName = 'get_users_name'
    SendUserName = 'send_user_name'
