import requests
import urllib.parse
from api import send_message

def calculate(input):
    try:
        input = urllib.parse.quote_plus(input)

        url = f"http://api.mathjs.org/v1/?expr={input}"

        response = requests.get(url).text
    except:
        response = "aff n sei mt difiicio......"

    return response


def on_msg_received(msg, matches):
    response = calculate(matches.group(1))

    send_message(msg["chat"]["id"], response)
