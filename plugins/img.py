from api import send_photo, send_message
from reborn import log
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

    index = random.randint(0, len(response["items"]) - 1)

    log("Imagem escolhida: " + response["items"][index]["link"])

    return response["items"][index]


def getValidLink(query):
    supportedFormats = ["jpg", "jpeg", "png", "gif"]

    valid = False

    google_img = requestGoogle(query)
    url = google_img["link"]

    while not valid:
        for format in supportedFormats:
            if url[-5:].find(format) != -1:
                valid = True
                break

        if not valid:
            log("Formato inválido, tentando novamente...")
            google_img = requestGoogle(query)
            url = google_img["link"]

    return google_img

def on_msg_received(msg, matches):
    img = getValidLink(matches.group(1))

    send_message(msg["chat"]["id"], "AE pora ta aki a imag......")
    sent = send_photo(msg["chat"]["id"], img["link"], img["snippet"])

    while sent["ok"] == "false":
        log("sendPhoto retornou false, rentando novamente...")
        img = getValidLink(matches.group(1))
        sent = send_photo(msg["chat"]["id"], img["link"], img["snippet"])
