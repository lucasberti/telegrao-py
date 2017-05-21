# encoding=utf-8

import json
import importlib
import logging
import requests
import os
import re
from time import gmtime
from calendar import timegm


logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler("log.log", "a", "utf-8")])


class Config:

    def __init__(self):
        self.plugins = {}
        self.config = None

        self.load_config()
        self.load_plugins()

    def load_config(self):
        """ Carrega o arquivo json e retorna um objeto com as configurações. """
        if os.path.isfile("data/config.json"):
            with open("data/config.json") as fp:
                self.config = json.load(fp)
        else:
            logging.info("Arquivo de config não encontrado.")
            exit(6924)

    def save_config(self):
        """ Salva o objeto JSON atual pro arquivo. """
        with open("data/config.json") as fp:
            json.dump(self.config, fp)

    def load_plugins(self):
        """ Carrega os plugins contidos em "data/config.json" e retorna uma lista com todos eles importados. """
        self.plugins = self.config["enabled_plugins"]


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
    elif "video_note" in msg:
        return "video note"


def msg_origin(msg):
    """ Mensagem privada ou mensagem de grupo"""
    return msg["chat"]["type"]


def log(msg):
    """ Loga pra arquivo tudo o que acontecer. """

    if type(msg) is str:
        logging.info(msg)
        print(msg)
    else:
        origin = msg_origin(msg)
        message_type = msg_type(msg)

        log_str = ""
        log_str += msg["from"]["first_name"] + " enviou " + message_type + " "

        if origin == "group":
            log_str += "em \"" + msg["chat"]["title"] + "\""
        elif origin == "private":
            log_str += "em PRIVADO"

        if message_type == "text":
            log_str += ": " + msg["text"]

        logging.info(log_str)
        print(log_str)


def is_authorized(msg):
    if msg["from"]["id"] in config.config["authorized_users"]:
        return True
    else:
        return False


def msg_matches(msg_text):
    for query, plugin in config.plugins.items():
        pattern = re.compile(query)
        match = pattern.search(msg_text)

        if match:
            log("MATCH! Plugin: " + plugin)
            return plugin, match

    return None, None


def on_msg_received(msg):
    """ Callback pra quando uma mensagem é recebida. """

    if is_authorized(msg):
        log(msg)

        if msg_type(msg) == "text":
            plugin_match, matches = msg_matches(msg["text"])

            if plugin_match is not None and matches is not None:
                loaded = importlib.import_module("plugins." + plugin_match)
                loaded.on_msg_received(msg, matches)

    else:
        log("Mensagem não autorizada de " + msg["from"]["first_name"])


def on_msg_edited(msg):
    """ Callback que define o que acontecerá quando uma mensagem for editada. """
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


def send_photo(chat_id, photo_url, caption, reply_to_message_id=0):
    """ reply_markup não é apenas ID, é uma array com opções. """
    url = "https://api.telegram.org/" + os.environ['REBORNKEY'] + "/sendPhoto?"
    url += "chat_id=" + str(chat_id) + "&"
    url += "photo=" + photo_url + "&"

    if caption:
        url += "caption=" + caption + "&"
    if reply_to_message_id:
        url += "reply_to_message_id=" + str(reply_to_message_id) + "&"

    response = requests.get(url)
    response = json.loads(response.content)

    return response["ok"]


def start_longpoll():
    """ Inicia longpolling do get_updates. """
    most_recent = 0

    while True:
        updates = get_updates(offset=most_recent)

        if updates is not None:
            for update in updates:
                if timegm(gmtime()) - update["message"]["date"] < 10:
                    if "message" in update:
                        on_msg_received(update["message"])
                    elif "edited_message" in update:
                        on_msg_edited(update["edited_message"])
                else:
                    log("Mensagem muito antiga; ignorando.")

                most_recent = update["update_id"] + 1


def main():
    """ Entry point né porra. """
    log("Iniciando sessão")
    start_longpoll()


if __name__ == "__main__":
    config = Config()
    main()
