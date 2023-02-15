import os
import re
import asyncio
import uuid
import json
from api import send_message, send_chat_action

USE_VERSION_2 = False
CONVERSATIONS_FILE = "data/conversations.json"

conversations = None

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


async def talk_to_chat_async(prompt, conversation_id=None):
    result = ""
    print(f"Generating output for {prompt}")

    data_count = 0

    async for line in chatbot.ask(prompt, conversation_id=conversation_id):
        if data_count % 10 == 0:
            send_chat_action(chat, "typing")

        result += line["choices"][0]["text"].replace("<|im_end|>", "")
        print(line["choices"][0]["text"].replace("<|im_end|>", ""), end="")

        data_count += 1

    return result


def talk_to_chat(prompt, chat_id=None):
    if chat_id:
        conversation_id = get_conversation_id(chat_id)

    if prompt.lower() == 'reset':
        conversation_id = reset_conversation_id(chat_id)
        prompt = "Olá, ChatGPT. A partir de agora vamos falar em pt-BR."

    if not USE_VERSION_2:
        result = ""
        data_count = 0

        print(f"Generating output for {prompt}")

        for data in chatbot.ask(prompt, conversation_id=conversation_id):
            if data_count % 10 == 0:
                send_chat_action(chat, "typing")

            data_count += 1

            result = data["message"]

            print(data["message"], end="", flush = True)
            print(data["message"], end="", flush = True)

        print(data["message"], end="", flush = True)

        return result
    else:
        return asyncio.run(talk_to_chat_async(prompt, conversation_id=conversation_id))


def save_conversations_to_file():
    global conversations

    with open(CONVERSATIONS_FILE, "w") as f:
            f.write(json.dumps(conversations))


def get_conversation_id(chat_id):
    global conversations

    if conversations is None:
        if not os.path.exists(CONVERSATIONS_FILE):
            with open(CONVERSATIONS_FILE, "w") as f:
                f.write("{}")
    
        with open(CONVERSATIONS_FILE, "r") as f:
            conversations = json.loads(f.read())

    if chat_id not in conversations:
        conversations[chat_id] = str(uuid.uuid4())

        save_conversations_to_file()
    
    return conversations[chat_id]



def reset_conversation_id(chat_id):
    global conversations

    if conversations is None:
        get_conversation_id(chat_id)

    conversations[chat_id] = str(uuid.uuid4())

    save_conversations_to_file()

    return conversations[chat_id]


def run_chat(msg):
    chat = msg["chat"]["id"]
    msg_text = msg["text"]

    pattern = re.compile("^(?:[Cc]hat,? (.*))|(?:(.*),? [Cc]hat\??)$")
    match = pattern.search(msg_text)

    if match:
        if match.group(1) is not None:
            response = talk_to_chat(match.group(1), chat_id=chat)
        elif match.group(2) is not None:
            response = talk_to_chat(match.group(2), chat_id=chat)

        send_message(chat, response)