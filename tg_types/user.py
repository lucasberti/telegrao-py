from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: int
    is_bot: bool
    language_code: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None