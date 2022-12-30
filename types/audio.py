from dataclasses import dataclass

@dataclass
class Audio:
    file_id: str
    file_unique_id: str
    duration: int
    performer: str
    title: str
    mime_type: str
    file_size: int