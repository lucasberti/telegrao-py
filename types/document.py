from dataclasses import dataclass

@dataclass
class Document:
    file_id: str
    file_unique_id: str
    file_name: str
    mime_type: str
    file_size: int
