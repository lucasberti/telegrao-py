import os
import re
from api import send_message
from revChatGPT.ChatGPT import Chatbot


config = {
    "session_token": os.getenv("OPENAI_REV_SESSION")
}

chatbot = Chatbot(config, conversation_id=None)

def talk_to_chat(prompt):
    print(f"Generating output for {prompt}")

    response = chatbot.ask(prompt, output="text")
    return response["message"]


def run_chat(msg):
    chat = msg["chat"]["id"]
    msg_text = msg["text"]

    pattern = re.compile("^(?:[Cc]hat,? (.*))|(?:(.*),? [Cc]hat\??)$")
    match = pattern.search(msg_text)

    if match:
        if match.group(1) is not None:
            response = talk_to_chat(match.group(1))
        elif match.group(2) is not None:
            response = talk_to_chat(match.group(2))

        send_message(chat, response)