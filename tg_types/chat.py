from dataclasses import dataclass
from typing import Optional

@dataclass
class Chat:
    id: int
    type: str
    first_name: Optional[str] = None
    title: Optional[str] = None
    username: Optional[str] = None
    last_name: Optional[str] = None