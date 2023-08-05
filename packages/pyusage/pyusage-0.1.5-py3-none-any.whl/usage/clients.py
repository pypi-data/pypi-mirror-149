import abc
from typing import Generator, Tuple

import requests

from .models import Session


class Client(abc.ABC):
    @abc.abstractmethod
    def upload_session(self, session: Session, package: str) -> None:
        pass

    @abc.abstractmethod
    def download_sessions(
        self, package: str
    ) -> Tuple[Generator[bytes, None, None], int]:
        pass


class FakeClient(Client):
    def upload_session(self, session: Session, package: str) -> None:
        pass

    def download_sessions(
        self, package: str
    ) -> Tuple[Generator[bytes, None, None], int]:
        raise NotImplementedError


class ProductionClient(Client):

    ENDPOINT = "https://backend-qr4qizlmya-uc.a.run.app"
    CHUNK_SIZE = 1024

    def upload_session(self, session: Session, package: str) -> None:
        requests.post(f"{self.ENDPOINT}/packages/{package}", json=session.dict())

    def download_sessions(
        self, package: str
    ) -> Tuple[Generator[bytes, None, None], int]:
        response = requests.get(f"{self.ENDPOINT}/packages/{package}", stream=True)
        size = int(response.headers["Content-Length"])
        content_stream = response.iter_content(chunk_size=self.CHUNK_SIZE)
        return content_stream, size
