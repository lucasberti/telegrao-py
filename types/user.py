from dataclasses import dataclass

@dataclass
class User:
    id: int
    is_bot: bool
    first_name: str
    last_name: str
    username: str
    language_code: str