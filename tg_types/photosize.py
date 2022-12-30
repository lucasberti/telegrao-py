from dataclasses import dataclass
from typing import Optional

@dataclass
class PhotoSize:
    file_id: str
    file_unique_id: str
    width: int
    height: int
    file_size: Optional[int] = None