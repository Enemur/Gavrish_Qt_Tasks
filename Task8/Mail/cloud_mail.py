import os
import re
import errno
import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoderMonitor


class PyMailCloud:
    def __init__(self, login, password):
        self.user_agent = "PyMailCloud/(1)"
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.user_agent})
        self.login = login
        self.password = password
        self.downloadSource = None
        self.uploadTarget = None
        self.__recreate_token()

    # ready
    def __get_download_source(self):
        params = {
            "token": self.token
        }
        dispatcher = self.session.get('https://cloud.mail.ru/api/v2/dispatcher', params=params)

        if dispatcher.status_code != 200:
            raise BaseException('Error')

        self.downloadSource = json.loads(dispatcher.content.decode("utf-8"))['body']['get'][0]['url']
        self.uploadTarget = json.loads(dispatcher.content.decode("utf-8"))['body']['upload'][0]['url']

    # ready
    def __recreate_token(self):
        data = {
            "page": "http://cloud.mail.ru/",
            "Login": self.login,
            "Password": self.password
        }
        login_response = self.session.post("https://auth.mail.ru/cgi-bin/auth", data, verify=False)

        if login_response.status_code == requests.codes.ok and login_response.history:
            get_token_response = self.session.post("https://cloud.mail.ru/api/v2/tokens/csrf")

            if get_token_response.status_code != 200:
                raise BaseException('Error')

            self.token = json.loads(get_token_response.content.decode("utf-8"))['body']['token']

            self.__get_download_source()
        else:
            raise BaseException('Error')

    # ready
    def get_folder_contents(self, folder):
        params = {
            "home": folder,
            "token": self.token
        }
        response = self.session.get("https://cloud.mail.ru/api/v2/folder", params=params)

        if response.status_code == 200:
            return response.json()['body']['list']

        raise BaseException('Error')

    def upload_files(self, path, filename):
        try:
            f = open(filename, 'rb')
        except FileNotFoundError:
            raise BaseException('File not found')

        destination = path + os.path.basename(filename)

        monitor = MultipartEncoderMonitor.from_fields(
            fields={'file': ('filename', f, 'application/octet-stream')},
        )

        upload_response = self.session.post(self.uploadTarget, data=monitor,
                                            headers={'Content-Type': monitor.content_type}, verify=False)

        if upload_response.status_code is not 200:
            raise BaseException('Error')

        hash = upload_response.content.decode("utf-8").split(';')[0]
        filesize = upload_response.content.decode("utf-8").split(';')[1][:-2]

        response = self.session.post("https://cloud.mail.ru/api/v2/file/add",
                                     data={
                                         "token": self.token,
                                         "home": destination,
                                         "conflict": 'rename',
                                         "hash": hash,
                                         "size": filesize,
                                     })
        return response.json()

    def download_file(self, file, outfile):
        response = self.session.get(self.downloadSource[:-1] + file, stream=True)
        if response.status_code == 404:
            raise BaseException('File not found')

        with open(outfile, "wb") as handle:
            handle.write(response.content)