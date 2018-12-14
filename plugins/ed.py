import api
import requests
import re
import urllib.parse

def talk_to_ed(message):
    ed_endpoint = "https://in.bot/api/bot_gateway"

    params = {
        "url_bot_gateway": "https://in.bot/api/bot_gateway",
        "is_ajax": 1,
        "bot_id": 133,
        "server": "no_host:no_port",
        "bot_admin": "",
        "no_log": 0,
        "json": 1,
        "user_phrase": f"{urllib.parse.quote_plus(message)}",
        "payload": "",
        "gender": "",
        "session_id": "ce16c6a1-d977-4f75-bff5-4a0dd0edcdc8",
        "user_id": "833abe72-e57a-4678-bc87-6e3e635f95ce",
        "username": "",
        "bot_token": "AGI-v01-EDo42vk8",
        "bot_server_type": "",
        "is_test": 0,
        "channel": "web",
        "setvar": "",
        "request_layout": 0
    }

    try:
        response = requests.post(url=ed_endpoint, data=params).json()["resp"]
        response = re.sub(r'<a href=(.*)\">', '', response).replace("</a>", "")
        
        return response
    except:
        return "ops o ed moreu........"

def run_ed(msg):
    chat = msg["chat"]["id"]
    msg_text = msg["text"]

    pattern = re.compile("^(?:[Ee]d,? (.*))|(?:(.*),? [Ee]d\??)$")
    match = pattern.search(msg_text)

    if match:
        if match.group(1) is not None:
            response = talk_to_ed(match.group(1))
        elif match.group(2) is not None:
            response = talk_to_ed(match.group(2))

        api.send_message(chat, response)
