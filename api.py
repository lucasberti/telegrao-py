import json
import logging
import os
from typing import Any, List
import requests
from utils.utils import DataClassUnpack

from tg_types.audio import Audio
from tg_types.chat import Chat
from tg_types.document import Document
from tg_types.message import Message
from tg_types.photosize import PhotoSize
from tg_types.sticker import Sticker
from tg_types.update import Update
from tg_types.user import User
from tg_types.video import Video
from tg_types.videonote import VideoNote
from tg_types.voice import Voice

class Api:
    def __init__(self, token: str):
        self.api_url = f"https://api.telegram.org/{token}/"


    def _create_message(self, response: dict) -> Message:
        if "message" in response:
            response_message = response["message"]
        elif "edited_message" in response:
            response_message = response["edited_message"]
        elif "callback_query" in response:
            response_message = response["callback_query"]
        elif "result" in response:
            response_message = response["result"]
        else:
            response_message = response
        
        response_chat = response_message["chat"]
        response_from = response_message["from"]
        response_audio = response_message["audio"] if "audio" in response_message else None
        response_document = response_message["document"] if "document" in response_message else None
        response_photo = response_message["photo"] if "photo" in response_message else None
        response_sticker = response_message["sticker"] if "sticker" in response_message else None
        response_video = response_message["video"] if "video" in response_message else None
        response_video_note = response_message["video_note"] if "video_note" in response_message else None
        response_voice = response_message["voice"] if "voice" in response_message else None

        result_chat = DataClassUnpack.instantiate(Chat, response_chat)
        result_from = DataClassUnpack.instantiate(User, response_from)
        result_audio = DataClassUnpack.instantiate(Audio, response_audio) if response_audio else None
        result_document = DataClassUnpack.instantiate(Document, response_document) if response_document else None
        result_photo = [DataClassUnpack.instantiate(PhotoSize, photo) for photo in response_photo] if response_photo else None
        result_sticker = DataClassUnpack.instantiate(Sticker, response_sticker) if response_sticker else None
        result_video = DataClassUnpack.instantiate(Video, response_video) if response_video else None
        result_video_note = DataClassUnpack.instantiate(VideoNote, response_video_note) if response_video_note else None
        result_voice = DataClassUnpack.instantiate(Voice, response_voice) if response_voice else None

        result_message = Message(
            message_id=response_message["message_id"],
            _from=result_from,
            date=response_message["date"],
            chat=result_chat,
            text=response_message["text"] if "text" in response_message else None,
            audio=result_audio,
            document=result_document,
            photo=result_photo,
            sticker=result_sticker,
            video=result_video,
            video_note=result_video_note,
            voice=result_voice,
            reply_to_message=self._create_message(response_message["reply_to_message"]) if "reply_to_message" in response_message else None,
            api=self
        )

        return result_message


    def _create_update(self, update: dict) -> Update:
        return Update(
            update_id=update["update_id"],
            message=self._create_message(update) if "message" in update else None,
            edited_message=self._create_message(update) if "edited_message" in update else None,
            callback_query=self._create_message(update) if "callback_query" in update else None
        )


    def get_updates(self, offset=0, timeout=60) -> Update:
        """ Por default, faz longpoll. Retorna uma array de Update """
        url = self.api_url + "getUpdates"

        params = {
            "timeout": timeout,
            "offset": offset
        }

        try:
            response = requests.get(url, params=params)
            response = json.loads(response.content)
        except Exception:
            return None

        if response["ok"]:
            logging.debug(response)
            return [self. _create_update(msg) for msg in response["result"]]
        else:
            return None


    def send_message(self, chat_id: int, text: str, parse_mode="", reply_to_message_id="", reply_markup="", disable_web_page_preview="false") -> Message:
        """ reply_markup não é apenas ID, é uma array com opções. """
    
        url = self.api_url + "sendMessage"

        params = {
            "chat_id": chat_id,
            "text": text,
            "disable_web_page_preview": disable_web_page_preview,
            "parse_mode": parse_mode,
            "reply_to_message_id": reply_to_message_id,
            "reply_markup": reply_markup
        }


        response = requests.get(url, params=params)
        response = json.loads(response.content)

        logging.info(response)
        return self._create_message(response)


    def edit_message_text(self, chat_id: int, msg_id: int, text: str, parse_mode="Markdown", reply_to_message_id="", reply_markup="") -> Message:
        """ reply_markup não é apenas ID, é uma array com opções. """
        url = self.api_url + "editMessageText"

        params = {
            "chat_id": chat_id,
            "message_id": msg_id,
            "text": text,
            "parse_mode": parse_mode,
            "reply_to_message_id": reply_to_message_id,
            "reply_markup": reply_markup
        }

        response = requests.get(url, params=params)
        response = json.loads(response.content)

        return self._create_message(response)


    def delete_message(self, chat_id: int, msg_id: int) -> bool:
        url = self.api_url + "deleteMessage"

        params = {
            "chat_id": chat_id,
            "message_id": msg_id
        }

        response = requests.get(url, params=params)
        response = json.loads(response.content)

        return response


    def send_photo(self, chat_id: int, photo_url: str, caption="", reply_to_message_id=0) -> Message:
        """ reply_markup não é apenas ID, é uma array com opções. """
        url = self.api_url + "sendPhoto"

        params = {
            "chat_id": chat_id,
            "photo": photo_url,
            "reply_to_message_id": reply_to_message_id,
            "caption": caption,
            "parse_mode": "Markdown"
        }

        response = requests.get(url, params=params)
        response = json.loads(response.content)

        return self._create_message(response)


    def send_video(self, chat_id: int, video_url: str, caption="", reply_to_message_id=0) -> Message:
        """ reply_markup não é apenas ID, é uma array com opções. """
        url = self.api_url + "sendVideo"

        params = {
            "chat_id": chat_id,
            "video": video_url,
            "reply_to_message_id": reply_to_message_id,
            "caption": caption,
            "parse_mode": "Markdown"
        }

        response = requests.get(url, params=params)
        response = json.loads(response.content)

        return self._create_message(response)


    def send_document(self, chat_id: int, document_url: str, caption="", reply_to_message_id=0) -> Message:
        """ reply_markup não é apenas ID, é uma array com opções. """
        url = self.api_url + "sendDocument"

        params = {
            "chat_id": chat_id,
            "document": document_url,
            "reply_to_message_id": reply_to_message_id,
            "caption": caption,
            "parse_mode": "Markdown"
        }

        response = requests.get(url, params=params)
        response = json.loads(response.content)

        return self._create_message(response)


    def send_sticker(self, chat_id: int, sticker_id: str) -> Message:
        url = self.api_url + "sendSticker"

        params = {
            "chat_id": chat_id,
            "sticker": sticker_id
        }

        response = requests.get(url, params=params)
        response = json.loads(response.content)

        return self._create_message(response)


    def send_voice(self, chat_id: int, voice_id: str) -> Message:
        url = self.api_url + "sendVoice"

        params = {
            "chat_id": chat_id,
            "voice": voice_id
        }

        response = requests.get(url, params=params)
        response = json.loads(response.content)

        return self._create_message(response)


    def send_chat_action(self, chat_id: int, action: str) -> bool:
        url = self.api_url + "sendChatAction"

        params = {
            "chat_id": chat_id,
            "action": action
        }

        response = requests.get(url, params=params)
        response = json.loads(response.content)

        return response


    def send_media_group(self, chat_id: int, files: List[Any], reply_to_message_id=0) -> List[Message]:
        url = self.api_url + "sendMediaGroup"

        files_request = {}
        media_arr = []

        for i in range(len(files)):
            media_arr.append({"type": "photo", "media": f"attach://media_{i}"})
            files_request[f"media_{i}"] = files[i]

        params = {
            "chat_id": chat_id,
            "media": json.dumps(media_arr),
            "reply_to_message_id": reply_to_message_id
        }

        logging.debug(files_request)
        logging.debug(url)

        response = requests.get(url, params=params, files=files_request)

        if response.status_code != 200:
            return self.send_message(chat_id, "Erro ao enviar mensagem")
        else:
            response = json.loads(response.content)

            logging.debug(response)

            return [self._create_message(resp) for resp in response]