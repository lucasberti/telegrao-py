from dataclasses import dataclass
from typing import Optional

@dataclass
class Audio:
    file_id: str
    file_unique_id: str
    duration: int
    performer: Optional[str] = None
    title: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None