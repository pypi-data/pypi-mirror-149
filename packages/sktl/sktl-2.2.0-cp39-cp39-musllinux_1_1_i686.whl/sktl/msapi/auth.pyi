from _typeshed import Incomplete

class Auth:
    GRAPH_API_BASE: str
    token_cache: Incomplete
    token: Incomplete
    headers: Incomplete
    def __init__(self, app_id, scopes, token_cache: Incomplete | None = ..., idx: int = ...) -> None: ...
    @staticmethod
    def login(app_id, scopes): ...
    @staticmethod
    def get_access_token(app_id, scopes, token_cache, idx): ...
