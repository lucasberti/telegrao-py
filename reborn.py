# encoding=utf-8

import json
import requests
import logging
import os

logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler("log.log", "a", "utf-8")])


def msg_type(msg):
    """ Retorna se é texto, foto, áudio, vídeo """
    if "text" in msg:
        return "text"
    elif "photo" in msg:
        return "photo"
    elif "voice" in msg:
        return "voice"
    elif "video" in msg:
        return "video"
    elif "document" in msg:
        return "document"
    elif "audio" in msg:
        return "audio"
    elif "sticker" in msg:
        return "sticker"


def msg_origin(msg):
    """ Mensagem privada ou mensagem de grupo"""
    return msg["chat"]["type"]


def log(msg):
    log_str = ""

    log_str += msg["from"]["first_name"] + " enviou " + msg_type(msg) + " "

    if msg_origin(msg) == "group":
        log_str += "em " + msg["chat"]["title"]
    elif msg_origin(msg) == "private":
        log_str += " em PRIVADO"

    if msg_type(msg) == "text":
        log_str += ": " + msg["text"]

    logging.info(log_str)
    print(log_str)


def on_msg_received(msg):
    """ Callback pra quando uma mensagem é recebida. """
    log(msg)


def on_msg_edited(msg):
    pass


def get_updates(offset=0, timeout=60):
    """ Por default, faz longpoll. Retorna uma array de Update """
    url = "https://api.telegram.org/" + os.environ['REBORNKEY'] + "/getUpdates?"
    url += "offset=" + str(offset) + "&"
    url += "timeout=" + str(timeout) + "&"

    response = requests.get(url)
    response = json.loads(response.content)

    if response["ok"] is True:
        return response["result"]
    else:
        return None


def send_message(chat_id, text, parsemode="Markdown", reply_to_message_id=0, reply_markup=0):
    """ reply_markup não é apenas ID, é uma array com opções. """
    url = "https://api.telegram.org/" + os.environ['REBORNKEY'] + "/sendMessage?"
    url += "chat_id=" + str(chat_id) + "&"
    url += "text=" + text + "&"
    url += "parsemode=" + parsemode + "&"
    if reply_to_message_id:
        url += "reply_to_message_id=" + str(reply_to_message_id) + "&"

    response = requests.get(url)
    response = json.loads(response.content)

    return response["ok"]


def start_longpoll():
    """ Inicia longpolling do get_updates"""
    most_recent = 0

    while True:
        updates = get_updates(offset=most_recent)

        if updates is not None:
            for update in updates:
                if "message" in update:
                    on_msg_received(update["message"])
                elif "edited_message" in update:
                    on_msg_edited(update["edited_message"])

                most_recent = update["update_id"] + 1


def main():
    """ Entry point né porra"""
    start_longpoll()


if __name__ == "__main__":
    main()
