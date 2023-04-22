import os
import re
import asyncio
import uuid
import json
import openai

from api import send_message, send_chat_action

CONVERSATIONS_FILE = "data/conversations.json"

class Conversation(object):
    conversations = None
    base_prompt = "Você está em um chat do Telegram. Fale em pt-BR. Responda de forma concisa e informal."

    @staticmethod
    def save_conversations_to_file():
        print("save")

        with open(CONVERSATIONS_FILE, "w") as f:
            f.write(json.dumps(Conversation.conversations, indent=4))


    @staticmethod
    def get_conversation(chat_id):
        chat_id = str(chat_id)
        print("get")

        if Conversation.conversations is None:
            print("if 1 get")

            if not os.path.exists(CONVERSATIONS_FILE):
                with open(CONVERSATIONS_FILE, "w") as f:
                    f.write("{}")
        
            with open(CONVERSATIONS_FILE, "r") as f:
                print("with 3 get")

                Conversation.conversations = json.loads(f.read())

        if str(chat_id) not in Conversation.conversations:
            print(Conversation.conversations)

            print("if 2 get")

            Conversation.reset(chat_id)

            Conversation.save_conversations_to_file()
        
        return Conversation.conversations[chat_id]

    
    @staticmethod
    def append_message(chat_id, message):
        print("append")
        conversation = Conversation.get_conversation(chat_id)

        if "messages" not in conversation:
            print("if append")

            Conversation.reset(chat_id)
            
            conversation = Conversation.get_conversation(chat_id)
        
        conversation["messages"].append(message)

        Conversation.save_conversations_to_file()

        return conversation


    @staticmethod
    def reset(chat_id):
        print("reset")

        Conversation.conversations[chat_id] = {}

        Conversation.conversations[chat_id]["messages"] = [
            {"role": "system", "content": Conversation.base_prompt}
        ]

        Conversation.save_conversations_to_file()



def get_chatgpt_response(conversation):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=conversation,
        request_timeout=30.0
    )

    print(response)

    return response['choices'][0]['message']


def talk_to_chat(prompt, chat_id):
    if prompt.lower() == 'reset':
        Conversation.reset(chat_id)

    message = {
        "role": "user",
        "content": prompt
    }

    conversation = Conversation.append_message(chat_id, message)
    print(f"Generating output for {prompt}")
    
    send_chat_action(chat_id, "typing")
    
    result = get_chatgpt_response(conversation["messages"])
    print("result", result)

    Conversation.append_message(chat_id, result)

    return result["content"]


def run_chat(msg):
    chat = msg["chat"]["id"]
    msg_text = msg["text"]

    pattern = re.compile("^(?:[Cc]hat,? (.*))|(?:(.*),? [Cc]hat\??)$")
    match = pattern.search(msg_text)

    if match:
        try:
            if match.group(1) is not None:
                response = talk_to_chat(match.group(1), chat_id=chat)
            elif match.group(2) is not None:
                response = talk_to_chat(match.group(2), chat_id=chat)

            send_message(chat, response)
        except Exception as e:
            send_message(chat, f"ops deu probreminha rsrs {str(e)}")