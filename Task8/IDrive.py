from abc import ABC, abstractmethod


class IDrive(ABC):

    @abstractmethod
    def download_file(self, public_url: str):
        pass
