from dataclasses import dataclass

@dataclass
class Chat:
    id: int
    type: str
    title: str
    username: str
    first_name: str
    last_name: str