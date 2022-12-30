from __future__ import annotations
from typing import List

import api
from user import User
from chat import Chat
from audio import Audio
from document import Document
from video import Video
from photosize import PhotoSize
from sticker import Sticker
from videonote import VideoNote

class Message:
    message_id: int
    _from: User
    date: int
    chat: Chat
    forward_from: User
    forward_from_chat: Chat
    forward_from_message_id: int
    reply_to_message: Message
    text: str
    audio: Audio
    document: Document
    photo: List[PhotoSize]
    sticker: Sticker
    video: Video
    video_note: VideoNote
    voice: Audio

    def reply(self, text):
        api.send_message(self.chat.id, text)