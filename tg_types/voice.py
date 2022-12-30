from dataclasses import dataclass
from typing import Optional

@dataclass
class Voice:
    file_id: str
    file_unique_id: str
    duration: int
    mime_type: Optional[str] = None
    file_size: Optional[int] = None