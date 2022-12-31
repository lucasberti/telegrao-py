# encoding=utf-8

import importlib
import logging
import re
import sys
import threading
import traceback
from calendar import timegm
from time import gmtime, sleep
from typing import List

import api
import config
from tg_types.message import Message
from tg_types.update import Update

SECS_BEFORE_MSG_IS_TOO_OLD = 10

logging.basicConfig(format='%(asctime)s.%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO, handlers=[
                            logging.FileHandler("log.log", "a", "utf-8"),
                            logging.StreamHandler(sys.stdout)
                        ])


def log(msg: Message):
    if type(msg) is str:
        logging.info(msg)
    else:
        origin = msg.chat.type
        message_type = msg.get_message_type()

        log_str = f"{msg._from.first_name} ({msg._from.id}) enviou {message_type} ({msg.message_id}) "

        if "group" in origin:
            log_str += f"em \"{msg.chat.title}\" "
        elif origin == "private":
            log_str += "em PRIVADO "

        log_str += f"({msg.chat.id})"

        if message_type == "text":
            log_str += f": {msg.text}"

        logging.info(log_str)


def is_sudoer(id):
    return id in config.config["sudoers"]


def is_authorized(msg: Message):
    return msg._from.id in config.config["authorized_users"]


def msg_matches(msg_text):
    for query, plugin in config.plugins.items():
        pattern = re.compile(query, flags=re.IGNORECASE|re.MULTILINE)
        match = pattern.search(msg_text)

        if match:
            if query != "^(.*)$":
                logging.debug("MATCH! Plugin: " + plugin)

            return plugin, match

    return None, None


def on_msg_received(msg: Message):
    """ Callback pra quando uma mensagem é recebida. """

    if is_authorized(msg):
        log(msg)

        if msg.get_message_type() == "text":
            plugin_match, matches = msg_matches(msg.text)

            if plugin_match is not None and matches is not None:
                loaded = importlib.import_module("plugins." + plugin_match)

                loaded.on_msg_received(msg, matches)

    else:
        log("Mensagem não autorizada de " + msg._from.first_name + " (" + str(msg._from.id) + ")")


def on_msg_edited(msg: Message):
    """ Callback que define o que acontecerá quando uma mensagem for editada. """
    pass


def on_callback_query(msg: Message):
    """ Callback que define o que acontecerá quando um dado de um InlineKeyboardButton for recebido. """
    for plugin in config.config["callback_query_plugins"]:
        loaded = importlib.import_module("plugins." + plugin)
        loaded.on_callback_query(msg)


def start_longpoll():
    """ Inicia longpolling do get_updates. """
    most_recent = 0

    while True:
        try:
            updates: List[Update] = api.get_updates(offset=most_recent)

            if updates is not None:
                for update in updates:
                    if update.message and timegm(gmtime()) - update.message.date < SECS_BEFORE_MSG_IS_TOO_OLD:
                        on_msg_received(update.message)
                    elif update.edited_message and timegm(gmtime()) - update.edited_message.date < SECS_BEFORE_MSG_IS_TOO_OLD:
                        on_msg_edited(update.edited_message)
                    elif update.callback_query:
                        on_callback_query(update.callback_query)
                    else:
                        logging.info("Mensagem muito antiga ou desconhecida; ignorando.")

                    most_recent = update.update_id + 1 # TODO
        except KeyboardInterrupt as e:
            sys.exit(0)
        except Exception as e:
            # Hardcodando aviso de erro. Não serve pra prevenir.
            exc_type, exc_value, exc_traceback = sys.exc_info()

            printable = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))

            for sudoer in config.config["sudoers"]:
                api.send_message(sudoer, f"ME CAPOTARO AQUI PORRA \n\n{printable}")
                api.send_message(sudoer, f"ai q sono vo durmi por {SECS_BEFORE_MSG_IS_TOO_OLD}")

            sleep(SECS_BEFORE_MSG_IS_TOO_OLD)
            


def start_plugins():
    for match, plugin in config.plugins.items():
        loaded = importlib.import_module("plugins." + plugin)

        if hasattr(loaded, "run"):
            thread = threading.Thread(name=plugin, target=loaded.run)
            thread.start()


def main():
    """ Entry point né porra. """
    logging.info("Iniciando sessão")
    #start_plugins()
    start_longpoll()


if __name__ == "__main__":
    main()
