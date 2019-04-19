import requests
import json
from api import send_message

ENDPOINT = "https://public-api.tracker.gg/apex/v1/standard/profile/5/"
PLAYERS = {
    14160874: "bertoncio",
    16631085: "beartz",
    85867003: "R3TCH4",
    52451934: "xisteaga",
    10549434: "Axasdas123",
    123123862: "MeroFabio",
    569341881: "burnovisk",
    299335806: "Springl3s",
    77547673: "BeDabul"
}

def get_stats(username):
    headers = {
        "TRN-Api-Key": "987c5b41-5649-4b4e-9d3f-4d58cc904584"
    }

    return requests.get(ENDPOINT + username, headers=headers).json()

def get_string(data):
    data = data["data"]

    legend_on_menu = data["children"][0]["metadata"]["legend_name"]
    username = data["metadata"]["platformUserHandle"]

    hero_stats = ""
    for legend in data["children"]:
        hero_stats += f"{legend['metadata']['legend_name']}\n"

        for stat in legend["stats"]:
            name = stat["metadata"]["name"]
            value = stat["displayValue"]
            percentile = stat["percentile"] if "percentile" in stat.keys() else "desconecidi"
            rank = stat["rank"] if "rank" in stat.keys() else "desconecidi"

            hero_stats += f"{name}: {value} (top {percentile}% rank {rank})\n"
        
        hero_stats += "\n"

    global_stats = ""
    for stat in data["stats"]:
        global_stats += f"{stat['metadata']['name']}: {stat['displayValue']}\n"


    return f"""{username} mt noob rs
ta c {legend_on_menu} selelessiondn

{hero_stats}
globau:
{global_stats}"""

def on_msg_received(msg, matches):
    chat = msg["chat"]["id"]
    user = msg["from"]["id"]

    player = None

    if matches.group(1):
        player = matches.group(1)
    else:
        if user in PLAYERS:
            player = PLAYERS[user]
    
    if player is not None:
        try:
            data = get_stats(player)
            stats = get_string(data)

            print(stats)

            send_message(chat, stats)
        except Exception as e:
            send_message(chat, f"vish deu merda..... {e}")
