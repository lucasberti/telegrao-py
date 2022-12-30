from dataclasses import dataclass

@dataclass
class Video:
    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    file_name: str
    mime_type: str
    file_size: int