class Runner:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class JellyfinOptions:
    endpoint: str
    username: str
    password: str
    ssl: bool

    def __init__(
        self, endpoint: str, username: str, password: str, ssl: bool = False
    ) -> None:
        self.endpoint = endpoint
        self.username = username
        self.password = password
        self.ssl = ssl


class NotionOptions:
    api_key: str
    database_id: str

    def __init__(self, api_key: str, database_id: str) -> None:
        self.api_key = api_key
        self.database_id = database_id
