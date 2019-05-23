from IDrive import IDrive
import requests
import json


class YandexDrive(IDrive):
    def download_file(self, public_url: str):
        download_url = f"https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={public_url}"

        result = requests.get(download_url)

        if result.status_code != 200:
            raise Exception("Error download")

        result_data = json.loads(result.text)

        href = result_data["href"]
        method = result_data["method"]
        templated = result_data["templated"]

        result = requests.get(href)

        if result.status_code != 200:
            raise Exception("Error download")

        return result.content
