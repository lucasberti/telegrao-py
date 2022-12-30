from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional

import api
from tg_types.user import User
from tg_types.chat import Chat
from tg_types.audio import Audio
from tg_types.document import Document
from tg_types.video import Video
from tg_types.photosize import PhotoSize
from tg_types.sticker import Sticker
from tg_types.videonote import VideoNote

@dataclass
class Message:
    message_id: int
    date: int
    chat: Chat
    text: str
    _from: Optional[User] = None
    forward_from: Optional[User] = None
    forward_from_chat: Optional[Chat] = None
    forward_from_message_id: Optional[int] = None
    reply_to_message: Optional[Message] = None
    audio: Optional[Audio] = None
    document: Optional[Document] = None
    photo: Optional[List[PhotoSize]] = None
    sticker: Optional[Sticker] = None
    video: Optional[Video] = None
    video_note: Optional[Video] = None
    voice: Optional[Audio] = None

    def reply(self, text):
        api.send_message(self.chat.id, text)