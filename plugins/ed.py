import api
import requests
import re

def talk_to_ed(message):
    strEndpoint = "http://www.ed.conpet.gov.br/mod_perl/bot_gateway.cgi"

    dictParams = {
        "server": "0.0.0.0:8085",
        "charset_post": "utf-8",
        "charset": "utf-8",
        "pure": 1,
        "js": 0,
        "tst": 1,
        "msg": message
    }

    dictHeader = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": str(len(dictParams))
    }

    strResponse = requests.post(url=strEndpoint, data=dictParams, headers=dictHeader)
    strResponse = strResponse.content.decode("utf-8")[:-1]

    strResponse = re.sub(r'<a href=(.*)\">', '', strResponse).replace("</a>", "") 

    return strResponse

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
