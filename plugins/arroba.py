from api import send_message
import json

arrobas = {}

def load_arrobas():
    global arrobas
    
    with open("data/arrobas.json", "r") as f:
        arrobas = json.load(f)

def save_arroba(arroba, username, chat):
    load_arrobas()

    if arroba not in arrobas:
        arrobas[arroba] = []

    if username not in arrobas[arroba]:
        arrobas[arroba].append(username)
        send_message(chat, "blz ticolokkeei")
    else:
        arrobas[arroba].remove(username)
        send_message(chat, "afff ta bno n kero masi tbn")

    with open("data/arrobas.json", "w") as f:
        json.dump(arrobas, f, sort_keys=True, indent=4)


def on_msg_received(msg, matches):
    chat = msg["chat"]["id"]
    arroba = "@" + matches.group(1).replace("@", "")

    if "username" in msg["from"].keys():
        save_arroba(arroba, "@" + msg["from"]["username"], chat)
    else:
        send_message(chat, "a vehlo vc nem tem arroba........")
