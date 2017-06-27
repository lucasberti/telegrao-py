from api import send_message, send_photo
import requests

def on_msg_received(msg, matches):
    url = "https://s.dicio.com.br/" + matches.group(1) + ".jpg"
    image = requests.get(url)

    if image:
        send_photo(msg["chat"]["id"], url, "taki qq e " + matches.group(1))
    else:
        send_message(msg["chat"]["id"], "n sei qqe iso n")
