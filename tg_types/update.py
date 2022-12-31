from dataclasses import dataclass
from typing import Optional

from tg_types.message import Message

@dataclass
class Update:
    update_id: int
    message: Optional[Message]
    edited_message: Optional[Message]
    callback_query: Optional[Message]