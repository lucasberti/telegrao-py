import json
import os
import requests
import config
from collections import namedtuple

class Msg(object):
    def __init__(self, obj):
        self.raw = obj
        self.update_id = obj.update_id
        self.message = obj.message
        self.id = self.message.message_id

        self.from_user = self.message.from_user
        self.chat = self.message.chat

        self.user_id = self.from_user.id
        self.user_first_name = self.from_user.first_name
        self.user_last_name = self.from_user.last_name if "last_name" in self.from_user._fields else None
        self.user_name = self.from_user.username if "username" in self.from_user._fields else None

        self.chat_id = self.chat.id
        self.chat_type = self.chat.type
        self.chat_title = self.chat.title if "private" not in self.chat_type else "privado"

        self.text = self.message.text if "text" in self.message._fields else None

        self.is_text = "text" in self.message._fields
        self.is_sticker = "sticker" in self.message._fields
        self.is_photo = "photo" in self.message._fields
        self.is_audio = "audio" in self.message._fields

        self.is_private = "private" in self.chat_type
        self.is_group = not self.is_private

        self.is_admin = self.user_id in config.config["admins"]


    def reply(self, content, type="text", reply_to_message=False):
        if content is str:
            if type == "text":
                if reply_to_message:
                    send_message(self.chat_id, content, reply_to_message_id=self.message.id)
                else:
                    send_message(self.chat_id, content)


    def __repr__(self):
        if self.text is not None:
            return f"Mensagem de {self.user_name} ao chat {self.chat_title}:   {self.text}"
        else:
            return f"Mensagem de {self.user_name} ao chat {self.chat_title}"
        

def get_updates(offset=0, timeout=60):
    """ Por default, faz longpoll. Retorna uma array de Update """
    url = "https://api.telegram.org/" + os.environ['REBORNKEY'] + "/getUpdates?"
    url += "offset=" + str(offset) + "&"
    url += "timeout=" + str(timeout) + "&"

    updates = requests.get(url)
    updates = updates.text.replace("from", "from_user")
    updates = json.loads(updates)

    for update in updates["result"]:
        message = json.loads(json.dumps(update), object_hook=lambda d: namedtuple('Msg', d.keys())(*d.values()))
        message = Msg(message)
        print(message)

        if message.text == "blabla":
            message.reply("blublu", True)

        yield message


def send_message(chat_id, text, parse_mode="Markdown", reply_to_message_id="", reply_markup=""):
    """ reply_markup não é apenas ID, é uma array com opções. """
    url = "https://api.telegram.org/" + os.environ['REBORNKEY'] + "/sendMessage?"
    url += "chat_id=" + str(chat_id) + "&"
    url += "text=" + text + "&"
    url += "parse_mode=" + parse_mode + "&"
    if reply_to_message_id:
        url += "reply_to_message_id=" + str(reply_to_message_id) + "&"
    if reply_markup:
        url += "reply_markup=" + str(reply_markup)

    response = requests.get(url)
    response = json.loads(response.content)

    return response


def edit_message_text(chat_id, msg_id, text, parse_mode="Markdown", reply_to_message_id="", reply_markup=""):
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

    return response


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


def send_chat_action(chat_id, action):
    url = "https://api.telegram.org/" + os.environ['REBORNKEY'] + "/sendChatAction?"
    url += "chat_id=" + str(chat_id) + "&"
    url += "action=" + action + "&"

    response = requests.get(url)
    response = json.loads(response.content)

    return response