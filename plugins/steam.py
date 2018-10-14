from api import send_message
import json
import requests
import os

# Deixando aqui apenas para referência futura.
# steamDict = {
#     14160874: 76561198040339223, # Berti
#     16631085: 76561198079217921, # Bea
#     85867003: 76561198051743480, # Raul
#     80048195: 76561198028549779, # Tiko
#     25919148: 76561198025591944, # Geta
#     52451934: 76561198009059027, # X
#     10549434: 76561198022638940  # Axasdas
# }

def get_ids():
    if os.path.isfile("data/steam.json"):
        id_str = ""
        with open("data/steam.json") as fp:
            steamDict = json.load(fp)

        for tg_id, steam_id in steamDict.items():
            id_str += str(steam_id) + ","

        return id_str

    else:
        raise FileNotFoundError


def translate_persona_state(state):
    if state is 0:
        return "oflain"
    elif state is 1:
        return "omlain"
    elif state is 2:
        return "o cu paod"
    elif state is 3:
        return "auei"
    elif state is 4:
        return "durmino MAS Q DORMINHIOC"
    elif state is 5:
        return "kereno troka"
    elif state is 6:
        return "kereno joga"
    else:
        return "alguam coisa q n sei"


def query_steam():
    url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"

    params = {
        "key": os.environ["STEAMKEY"],
        "steamids": get_ids()
    }

    response = requests.get(url, params)
    response = json.loads(response.content)

    message = ""

    for player in response["response"]["players"]:
        name = player["personaname"]
        state = player["personastate"]

        if "gameextrainfo" in player:
            gamename = player["gameextrainfo"]
        else:
            gamename = "nada"

        if player["personastate"] is not 0:
            message += "{} ta {} i jogno {}\n".format(name, translate_persona_state(state), gamename)
        else:
            message += "{} ta oflain afff\n".format(name)

    return message

def on_msg_received(msg, matches):
    chat = msg["chat"]["id"]
    response = query_steam()

    send_message(chat, response, parse_mode="")
