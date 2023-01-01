import json
import logging
import os
from typing import List
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


def _create_message(response) -> Message:
    if "message" in response:
        response_message = response["message"]
    elif "edited_message" in response:
        response_message = response["edited_message"]
    elif "callback_query" in response:
        response_message = response["callback_query"]
    else:
        response_message = response["result"]
    
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
        reply_to_message=DataClassUnpack.instantiate(Message, response_message["reply_to_message"]) if "reply_to_message" in response_message else None,
    )

    return result_message


def _create_update(update) -> Update:
    return Update(
        update_id=update["update_id"],
        message=_create_message(update) if "message" in update else None,
        edited_message=_create_message(update) if "edited_message" in update else None,
        callback_query=_create_message(update) if "callback_query" in update else None
    )


def get_updates(offset=0, timeout=60) -> Update:
    """ Por default, faz longpoll. Retorna uma array de Update """
    url = "https://api.telegram.org/" + os.environ['REBORNKEY'] + "/getUpdates?"
    url += "offset=" + str(offset) + "&"
    url += "timeout=" + str(timeout) + "&"

    try:
        response = requests.get(url)
        response = json.loads(response.content)
    except Exception:
        return None

    if response["ok"]:
        logging.debug(response)
        return [_create_update(msg) for msg in response["result"]]
    else:
        return None


def send_message(chat_id, text, parse_mode="", reply_to_message_id="", reply_markup="", disable_web_page_preview="false") -> Message:
    """ reply_markup não é apenas ID, é uma array com opções. """
 
    #text = text.replace("c", "k").replace("qu", "k")
    url = "https://api.telegram.org/" + os.environ['REBORNKEY'] + "/sendMessage?"
    url += "chat_id=" + str(chat_id) + "&"
    url += "text=" + text + "&"
    url += "disable_web_page_preview=" + disable_web_page_preview + "&" 
    url += "parse_mode=" + parse_mode + "&"
    if reply_to_message_id:
        url += "reply_to_message_id=" + str(reply_to_message_id) + "&"
    if reply_markup:
        url += "reply_markup=" + str(reply_markup)

    response = requests.get(url)
    response = json.loads(response.content)

    return _create_message(response)


def edit_message_text(chat_id, msg_id, text, parse_mode="Markdown", reply_to_message_id="", reply_markup="") -> Message:
    """ reply_markup não é apenas ID, é uma array com opções. """
    url = "https://api.telegram.org/" + os.environ['REBORNKEY'] + "/editMessageText?"
    url += "chat_id=" + str(chat_id) + "&"
    url += "message_id=" + str(msg_id) + "&"
    url += "text=" + text + "&"
    url += "parse_mode=" + parse_mode + "&"
    if reply_to_message_id:
        url += "reply_to_message_id=" + str(reply_to_message_id) + "&"
    if reply_markup:
        url += "reply_markup=" + str(reply_markup)

    response = requests.get(url)
    response = json.loads(response.content)

    return _create_message(response)


def delete_message(chat_id, msg_id) -> bool:
    url = "https://api.telegram.org/" + os.environ['REBORNKEY'] + "/deleteMessage?"
    url += "chat_id=" + str(chat_id) + "&"
    url += "message_id=" + str(msg_id)

    response = requests.get(url)
    response = json.loads(response.content)

    return response


def send_photo(chat_id, photo_url, caption="", reply_to_message_id=0) -> Message:
    """ reply_markup não é apenas ID, é uma array com opções. """
    url = "https://api.telegram.org/" + os.environ['REBORNKEY'] + "/sendPhoto?"
    url += "chat_id=" + str(chat_id) + "&"
    url += "photo=" + photo_url + "&"

    if caption:
        url += "caption=" + caption + "&"
        url += "parse_mode=Markdown&"
    if reply_to_message_id:
        url += "reply_to_message_id=" + str(reply_to_message_id) + "&"

    response = requests.get(url)
    response = json.loads(response.content)

    return _create_message(response)


def send_video(chat_id, video_url, caption="", reply_to_message_id=0) -> Message:
    """ reply_markup não é apenas ID, é uma array com opções. """
    url = "https://api.telegram.org/" + os.environ['REBORNKEY'] + "/sendVideo?"
    url += "chat_id=" + str(chat_id) + "&"
    url += "video=" + video_url + "&"

    if caption:
        url += "caption=" + caption + "&"
        url += "parse_mode=Markdown&"
    if reply_to_message_id:
        url += "reply_to_message_id=" + str(reply_to_message_id) + "&"

    response = requests.get(url)
    response = json.loads(response.content)

    return _create_message(response)


def send_document(chat_id, document_url, caption="", reply_to_message_id=0) -> Message:
    """ reply_markup não é apenas ID, é uma array com opções. """
    url = "https://api.telegram.org/" + os.environ['REBORNKEY'] + "/sendDocument?"
    url += "chat_id=" + str(chat_id) + "&"
    url += "document=" + document_url + "&"

    if caption:
        url += "caption=" + caption + "&"
    if reply_to_message_id:
        url += "reply_to_message_id=" + str(reply_to_message_id) + "&"

    response = requests.get(url)
    response = json.loads(response.content)

    return _create_message(response)


def send_sticker(chat_id, sticker_id) -> Message:
    url = "https://api.telegram.org/" + os.environ['REBORNKEY'] + "/sendSticker?"
    url += "chat_id=" + str(chat_id) + "&"
    url += "sticker=" + sticker_id + "&"

    response = requests.get(url)
    response = json.loads(response.content)

    return _create_message(response)


def send_voice(chat_id, voice_id) -> Message:
    url = "https://api.telegram.org/" + os.environ['REBORNKEY'] + "/sendvoice?"
    url += "chat_id=" + str(chat_id) + "&"
    url += "voice=" + voice_id + "&"

    response = requests.get(url)
    response = json.loads(response.content)

    return _create_message(response)


def send_chat_action(chat_id, action) -> bool:
    url = "https://api.telegram.org/" + os.environ['REBORNKEY'] + "/sendChatAction?"
    url += "chat_id=" + str(chat_id) + "&"
    url += "action=" + action + "&"

    response = requests.get(url)
    response = json.loads(response.content)

    return response


def send_media_group(chat_id, files, reply_to_message_id=0) -> List[Message]:
    url = "https://api.telegram.org/" + os.environ['REBORNKEY'] + "/sendMediaGroup?"
    url += "chat_id=" + str(chat_id) + "&"

    if reply_to_message_id:
        url += "reply_to_message_id=" + str(reply_to_message_id) + "&"

    files_request = {}
    media_arr = []

    for i in range(len(files)):
        media_arr.append({"type": "photo", "media": f"attach://media_{i}"})
        files_request[f"media_{i}"] = files[i]

    url += "media=" + json.dumps(media_arr) + "&"

    logging.debug(files_request)
    logging.debug(url)

    response = requests.get(url, files=files_request)

    if response.status_code != 200:
        return send_message(chat_id, "Erro ao enviar mensagem")
    else:
        response = json.loads(response.content)

        logging.debug(response)

        return [_create_message(resp) for resp in response]