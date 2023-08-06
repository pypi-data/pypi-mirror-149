from .cursor import cursor as cursor
from _typeshed import Incomplete

class db:
    conn: Incomplete
    def __init__(self, dbModule, **dbInfo) -> None: ...
    def execute(self, query, vals: Incomplete | None = ..., *args, **kwargs) -> cursor: ...
