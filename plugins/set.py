import json
import urllib.parse
from api import send_message

values = {}

def load_values():
    global values
    with open("data/values.json", "r") as f:
        values = json.load(f)

def get_item(item):
    load_values()

    if item in values:
        return f"{item} = {values[item]}"
    else:
        return "ixi n sei n"

def get_all_items():
    load_values()

    text = ""

    for item in values.keys():
        text += f"{item} = {values[item]}\n"

    with open("/var/www/html/get.txt", "w") as f:
        f.write(text)

    text = urllib.parse.quote(text)

    for chunk in range(0, len(text), 4096):
        yield text[chunk:chunk+4096]


def save_item(item, value):
    load_values()

    values[item] = value
    with open("data/values.json", "w") as f:
        json.dump(values, f, sort_keys=True, indent=4)


def on_msg_received(msg, matches):
    chat = msg["chat"]["id"]
    is_get = "get" in matches.group(1)
    content = matches.group(2)

    if not is_get:
        if content:
            item, value = content.split(", ")
            save_item(item, value)

            send_message(chat, f"ok sauvei aq q {item} = {value}")
        else:
            send_message(chat, "a veloh vc precisiasa m e falala qqq vc ke grava.....")
    else:
        if content:
            text = get_item(content)
            send_message(chat, text)
        else:
            for item in get_all_items(): 
                send_message(chat, item, parse_mode="")
            