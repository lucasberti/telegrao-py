from dataclasses import dataclass
from typing import Optional

@dataclass
class VideoNote:
    file_id: str
    file_unique_id: str
    length: int
    duration: int
    file_size: Optional[int] = None