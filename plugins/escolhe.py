from random import choice
from re import split
from api import send_message

options = []

def get_random_item(text):
    text = split(",+| ou ", text)

    if len(text) > 1:
        return "hummmm vamo ve..... " + choice(text)
    else:
        return "pora nen etedi o ke vc falo ai kkkk cade as opcao"

def on_msg_received(msg, matches):
    chat = msg["chat"]["id"]
    text = matches.group(1)

    send_message(chat, get_random_item(text))
