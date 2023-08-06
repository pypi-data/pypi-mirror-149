import io
from .auth import Auth as Auth
from typing import BinaryIO, Union

class OneDrive(Auth):
    def upload(self, filename, filebytes: Union[bytes, io.BytesIO, BinaryIO]): ...
