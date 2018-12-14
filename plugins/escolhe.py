from api import send_message
import random
import re

options = []

def get_random_item(text):
    pattern = re.compile("(?:entre|de) (\d+) [eaà] (\d+)", flags=re.IGNORECASE)
    match = pattern.search(text)

    if match:
        start = int(match.group(1))
        end = int(match.group(2))

        return f"hummmm vamo ve..... {random.randint(start, end)}"
    
    text = re.split(",+| ou ", text)

    if len(text) > 1:
        return f"hummmm vamo ve..... {random.choice(text)}"
    else:
        return "pora nen etedi o ke vc falo ai kkkk cade as opcao"

def on_msg_received(msg, matches):
    chat = msg["chat"]["id"]
    text = matches.group(1)

    send_message(chat, get_random_item(text))
