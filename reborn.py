# encoding=utf-8

import api
import importlib
import logging
import re
import config
import threading
import traceback
import sys
from time import gmtime
from calendar import timegm


logging.basicConfig(format='%(asctime)s.%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%d-%m-%Y:%H:%M:%S',
                    level=logging.INFO, handlers=[logging.FileHandler("log.log", "a", "utf-8")])


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
    else:
        return "outra coisa"


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


def is_sudoer(id):
    return id in config.config["sudoers"]


def is_authorized(msg):
    return msg["from"]["id"] in config.config["authorized_users"]


def msg_matches(msg_text):
    for query, plugin in config.plugins.items():
        pattern = re.compile(query)
        match = pattern.search(msg_text)

        if match:
            if query != "^(.*)$":
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
                try:
                    loaded.on_msg_received(msg, matches)
                except:
                    # Hardcodando aviso de erro. Não serve pra prevenir.
                    exc_type, exc_value, exc_traceback = sys.exc_info()

                    printable = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))

                    for sudoer in config.config["sudoers"]:
                        api.send_message(sudoer, "ME CAPOTARO AQUI PORRA \n\n" + printable)

                    raise

    else:
        log("Mensagem não autorizada de " + msg["from"]["first_name"] + " (" + str(msg["from"]["id"]) + ")")


def on_msg_edited(msg):
    """ Callback que define o que acontecerá quando uma mensagem for editada. """
    pass


def on_callback_query(msg):
    """ Callback que define o que acontecerá quando um dado de um InlineKeyboardButton for recebido. """
    for plugin in config.config["callback_query_plugins"]:
        loaded = importlib.import_module("plugins." + plugin)
        loaded.on_callback_query(msg)


def start_longpoll():
    """ Inicia longpolling do get_updates. """
    most_recent = 0

    while True:
        updates = api.get_updates(offset=most_recent)

        if updates is not None:
            for update in updates:
                if "message" in update and timegm(gmtime()) - update["message"]["date"] < 10:
                    on_msg_received(update["message"])
                elif "edited_message" in update and timegm(gmtime()) - update["edited_message"]["date"] < 10:
                    on_msg_edited(update["edited_message"])
                elif "callback_query" in update:
                    on_callback_query(update["callback_query"])
                else:
                    log("Mensagem muito antiga ou desconhecida; ignorando.")

                most_recent = update["update_id"] + 1


def start_plugins():
    for match, plugin in config.plugins.items():
        loaded = importlib.import_module("plugins." + plugin)

        if hasattr(loaded, "run"):
            thread = threading.Thread(target=loaded.run)
            thread.start()


def main():
    """ Entry point né porra. """
    log("Iniciando sessão")
    start_plugins()
    start_longpoll()


if __name__ == "__main__":
    main()
