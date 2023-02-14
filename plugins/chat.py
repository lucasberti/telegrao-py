import os
import re
from api import send_message, send_chat_action
from revChatGPT.V2 import Chatbot
import asyncio

USE_VERSION_2 = False

if USE_VERSION_2:
    from revChatGPT.V2 import Chatbot

    config = {
        "email": os.getenv("OPENAI_REV_EMAIL"),
        "password": os.getenv("OPENAI_REV_PASSWORD")
    }

    chatbot = Chatbot(email=config["email"], password=config["password"])
else:
    from revChatGPT.V1 import Chatbot

    config = {
        "email": os.getenv("OPENAI_REV_EMAIL"),
        "password": os.getenv("OPENAI_REV_PASSWORD")
    }

    chatbot = Chatbot(config=config)


async def talk_to_chat_async(prompt):
    result = ""
    print(f"Generating output for {prompt}")

    async for line in chatbot.ask(prompt):
        result += line["choices"][0]["text"].replace("<|im_end|>", "")
        print(line["choices"][0]["text"].replace("<|im_end|>", ""), end="")

    return result


def talk_to_chat(prompt):
    if not USE_VERSION_2:
        result = ""
        print(f"Generating output for {prompt}")

        for data in chatbot.ask(prompt):
            result = data["message"]
            print(data["message"], end="", flush = True)

        return result
    else:
        return asyncio.run(talk_to_chat_async(prompt))


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