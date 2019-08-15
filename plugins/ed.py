import api
import requests
import re
import urllib.parse

def talk_to_ed(message):
    print(urllib.parse.quote_plus(message))

    ed_endpoint = f"https://in.bot/api/bot_gateway?pure=1&js=0&bot_id=133&bot_token=AGI-v01-EDo42vk8&user_phrase={urllib.parse.quote_plus(message)}"

    try:
        response = requests.get(ed_endpoint).text
        print(response)
        response = re.sub(r'<a href=(.*)\">', '', response).replace("</a>", "")
        
        return response
    except Exception as e:
        return f"ops o ed moreu........ {e}"

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
