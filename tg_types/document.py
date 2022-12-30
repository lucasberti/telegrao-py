from dataclasses import dataclass
from typing import Optional

@dataclass
class Document:
    file_id: str
    file_unique_id: str
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None
