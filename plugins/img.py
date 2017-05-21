import reborn
import requests
import json
import random
from os import environ


def requestGoogle(query):
    url = "https://www.googleapis.com/customsearch/v1?"
    url = url + "cx=006518944303354753471:um8whdniwke"
    url = url + "&searchType=image"
    url = url + "&key=" + environ["googlekey"]

    url = url + "&q=" + query

    response = requests.get(url)
    response = json.loads(response.content)

    index = random.randint(0, len(response["items"]))

    return response["items"][index]


def on_msg_received(msg, matches):
    img = requestGoogle(matches.group(1))

    reborn.send_message(msg["chat"]["id"], "AE pora ta aki a imag......")
    reborn.send_photo(msg["chat"]["id"], img["link"], img["snippet"])
    # print("ae carai: ", matches.group(1))