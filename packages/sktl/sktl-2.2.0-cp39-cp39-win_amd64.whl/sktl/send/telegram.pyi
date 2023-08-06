from .send import _base_send_class
from _typeshed import Incomplete

class telegram(_base_send_class):
    BOT_TOKEN: Incomplete
    CHAT_ID: Incomplete
    TG_API_HOST: Incomplete
    def __init__(self, BOT_TOKEN, CHAT_ID, TG_API_HOST=...) -> None: ...
    def send(self, msg): ...
