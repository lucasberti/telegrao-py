import json
import os
import requests
import utils.unpacker

from .types.message import Message
from .types.user import User
from .types.chat import Chat
from .types.audio import Audio
from .types.document import Document
from .types.photosize import PhotoSize
from .types.sticker import Sticker
from .types.video import Video
from .types.videonote import VideoNote


def _create_message(result) -> Message:
    response = response["result"]

    response_message = response["message"]
    response_chat = response_message["chat"]
    response_from = response_message["from"]
    response_audio = response_message["audio"] if "audio" in response_message else None
    response_document = response_message["document"] if "document" in response_message else None
    response_photo = response_message["photo"] if "photo" in response_message else None
    response_sticker = response_message["sticker"] if "sticker" in response_message else None
    response_video = response_message["video"] if "video" in response_message else None
    response_video_note = response_message["video_note"] if "video_note" in response_message else None
    response_voice = response_message["voice"] if "voice" in response_message else None

    result_chat = Chat(
        id=response_chat["id"],
        type=response_chat["type"],
        title=response_chat["title"] or None,
        username=response_chat["username"] or None,
        first_name=response_chat["first_name"] or None,
        last_name=response_chat["last_name"] or None
    )

    result_from = User(
        id=response_from["id"],
        is_bot=response_from["is_bot"],
        first_name=response_from["first_name"] or None,
        last_name=response_from["last_name"] or None,
        username=response_from["username"] or None
    )

    if response_audio:
        result_audio = Audio(
            file_id=response_audio["file_id"],
            file_unique_id=response_audio["file_unique_id"],
            duration=response_audio["duration"] or None,
            performer=response_audio["performer"] or None,
            title=response_audio["title"] or None,
            mime_type=response_audio["mime_type"] or None,
            file_size=response_audio["file_size"] or None
        )
    else:
        result_audio = None

    if response_document:
        result_document = Document(
            file_id=response_document["file_id"],
            file_unique_id=response_document["file_unique_id"],
            thumb=PhotoSize(
                file_id=response_document["thumb"]["file_id"],
                file_unique_id=response_document["thumb"]["file_unique_id"],
                width=response_document["thumb"]["width"],
                height=response_document["thumb"]["height"],
                file_size=response_document["thumb"]["file_size"]
            ) if "thumb" in response_document else None,
            file_name=response_document["file_name"] or None,
            mime_type=response_document["mime_type"] or None,
            file_size=response_document["file_size"] or None
        )
    else:
        result_document = None

    if response_photo:
        result_photo = PhotoSize(
            file_id=response_photo["file_id"],
            file_unique_id=response_photo["file_unique_id"],
            width=response_photo["width"],
            height=response_photo["height"],
            file_size=response_photo["file_size"]
        )
    else:
        result_photo = None

    if response_sticker:
        result_sticker = Sticker(
            file_id=response_sticker["file_id"],
            file_unique_id=response_sticker["file_unique_id"],
            width=response_sticker["width"],
            height=response_sticker["height"],
            file_size=response_sticker["file_size"]
        )
    else:
        result_sticker = None

    if response_video:
        result_video = Video(
            file_id=response_video["file_id"],
            file_unique_id=response_video["file_unique_id"],
            width=response_video["width"],
            height=response_video["height"],
            duration=response_video["duration"] or None,
            thumb=PhotoSize(
                file_id=response_video["thumb"]["file_id"],
                file_unique_id=response_video["thumb"]["file_unique_id"],
                width=response_video["thumb"]["width"],
                height=response_video["thumb"]["height"],
                file_size=response_video["thumb"]["file_size"]
            ) if "thumb" in response_video else None,
            mime_type=response_video["mime_type"] or None,
            file_size=response_video["file_size"] or None
        )
    else:
        result_video = None

    if response_video_note:
        result_video_note = VideoNote(
            file_id=response_video_note["file_id"],
            file_unique_id=response_video_note["file_unique_id"],
            length=response_video_note["length"] or None,
            duration=response_video_note["duration"] or None,
            thumb=PhotoSize(
                file_id=response_video_note["thumb"]["file_id"],
                file_unique_id=response_video_note["thumb"]["file_unique_id"],
                width=response_video_note["thumb"]["width"],
                height=response_video_note["thumb"]["height"],
                file_size=response_video_note["thumb"]["file_size"]
            ) if "thumb" in response_video_note else None,
            file_size=response_video_note["file_size"] or None
        )
    else:
        result_video_note = None

    if response_voice:
        result_voice = Voice(
            file_id=response_voice["file_id"],
            file_unique_id=response_voice["file_unique_id"],
            duration=response_voice["duration"] or None,
            mime_type=response_voice["mime_type"] or None,
            file_size=response_voice["file_size"] or None
        )
    else:
        result_voice = None

    result_message = Message(
        message_id=response_message["message_id"],
        _from=result_from,
        date=response_message["date"],
        chat=result_chat,
        text=response_message["text"] or None,
        audio=result_audio,
        document=result_document,
        photo=result_photo,
        sticker=result_sticker,
        video=result_video,
        video_note=result_video_note,
        voice=result_voice
        reply_to_message=response_message["reply_to_message"] or None
    )

    return result_message

def get_updates(offset=0, timeout=60) -> Message:
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
        return _create_message(response)
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


def delete_message(chat_id, msg_id):
    url = "https://api.telegram.org/" + os.environ['REBORNKEY'] + "/deleteMessage?"
    url += "chat_id=" + str(chat_id) + "&"
    url += "message_id=" + str(msg_id)

    response = requests.get(url)
    response = json.loads(response.content)

    return response


def send_photo(chat_id, photo_url, caption="", reply_to_message_id=0):
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

    return response


def send_video(chat_id, video_url, caption="", reply_to_message_id=0):
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

    return response


def send_document(chat_id, document_url, caption="", reply_to_message_id=0):
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

    return response


def send_sticker(chat_id, sticker_id): 
    url = "https://api.telegram.org/" + os.environ['REBORNKEY'] + "/sendSticker?"
    url += "chat_id=" + str(chat_id) + "&"
    url += "sticker=" + sticker_id + "&"

    response = requests.get(url)
    response = json.loads(response.content)

    return response


def send_voice(chat_id, voice_id): 
    url = "https://api.telegram.org/" + os.environ['REBORNKEY'] + "/sendvoice?"
    url += "chat_id=" + str(chat_id) + "&"
    url += "voice=" + voice_id + "&"

    response = requests.get(url)
    response = json.loads(response.content)

    return response


def send_chat_action(chat_id, action):
    url = "https://api.telegram.org/" + os.environ['REBORNKEY'] + "/sendChatAction?"
    url += "chat_id=" + str(chat_id) + "&"
    url += "action=" + action + "&"

    response = requests.get(url)
    response = json.loads(response.content)

    return response


def send_media_group(chat_id, files, reply_to_message_id=0):
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

    print(files_request)
    print(url)

    response = requests.get(url, files=files_request)

    if response.status_code != 200:
        return send_message(chat_id, "Erro ao enviar mensagem")
    else:
        response = json.loads(response.content)

        print(response)

        return response