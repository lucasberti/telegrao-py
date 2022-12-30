from dataclasses import dataclass
from typing import Optional

@dataclass
class Sticker:
    file_id: str
    file_unique_id: str
    type: str
    width: int
    height: int
    is_animated: bool
    is_video: bool
    emoji: Optional[str] = None
    file_size: Optional[str] = None