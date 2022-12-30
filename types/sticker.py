from dataclasses import dataclass

@dataclass
class Sticker:
    file_id: str
    file_unique_id: str
    type: str
    width: int
    height: int
    is_animated: bool
    is_video: bool
    emoji: str
    file_size: int