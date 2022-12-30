from dataclasses import dataclass

@dataclass
class VideoNote:
    file_id: str
    file_unique_id: str
    length: int
    duration: int
    file_size: int