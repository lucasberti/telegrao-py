import os
import re
import json
import openai

from api import send_message, send_chat_action


class Conversation:
    CONVERSATIONS_FILE = "data/conversations.json"
    DEFAULT_PROMPT = "Você está em um chat do Telegram. Fale em pt-BR. Responda de forma concisa e informal."
    MAX_TOKEN_CONTEXT_LENGTH = 1800
    
    conversations = None

    @staticmethod
    def save_conversations_to_file():
        with open(Conversation.CONVERSATIONS_FILE, "w") as f:
            f.write(json.dumps(Conversation.conversations, indent=4))


    @staticmethod
    def get_conversation(chat_id):
        chat_id = str(chat_id)

        if Conversation.conversations is None:
            if not os.path.exists(Conversation.CONVERSATIONS_FILE):
                with open(Conversation.CONVERSATIONS_FILE, "w") as f:
                    f.write("{}")

            with open(Conversation.CONVERSATIONS_FILE, "r") as f:
                Conversation.conversations = json.loads(f.read())

        if chat_id not in Conversation.conversations:
            Conversation.reset(chat_id)

            Conversation.save_conversations_to_file()

        return Conversation.conversations[chat_id]


    @staticmethod
    def append_message(chat_id, message):
        chat_id = str(chat_id)
        conversation = Conversation.get_conversation(chat_id)

        if "messages" not in conversation:
            Conversation.reset(chat_id)

            conversation = Conversation.get_conversation(chat_id)

        conversation["messages"].append(message)

        Conversation.save_conversations_to_file()

        return conversation


    @staticmethod
    def reset(chat_id):
        chat_id = str(chat_id)

        if Conversation.conversations is not None:
            Conversation.conversations[chat_id] = {}

            Conversation.conversations[chat_id]["messages"] = [
                {"role": "system", "content": Conversation.DEFAULT_PROMPT}
            ]

            Conversation.save_conversations_to_file()

    
    @staticmethod
    def remove_oldest_non_base_message(chat_id):
        chat_id = str(chat_id)

        if len(Conversation.conversations[chat_id]["messages"]) > 1:
            Conversation.conversations[chat_id]["messages"].pop(1)

            Conversation.save_conversations_to_file()


def get_chatgpt_response(conversation, chat_id):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        request_timeout=60.0
    )

    print(response)

    if response['usage']['total_tokens'] > Conversation.MAX_TOKEN_CONTEXT_LENGTH:
        Conversation.remove_oldest_non_base_message(chat_id)

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
    
    result = get_chatgpt_response(conversation["messages"], chat_id)
    print("result", result)

    Conversation.append_message(chat_id, result)

    return result["content"]


def run_chat(msg):
    chat_id = msg["chat"]["id"]
    msg_text = msg["text"]

    pattern = re.compile("^(?:[Cc]hat,? (.*))|(?:(.*),? [Cc]hat\??)$")
    match = pattern.search(msg_text)

    if match:
        try:
            if match.group(1) is not None:
                response = talk_to_chat(match.group(1), chat_id)
            elif match.group(2) is not None:
                response = talk_to_chat(match.group(2), chat_id)

            send_message(chat_id, response)
        except Exception as e:
            print(str(e))
            send_message(chat_id, f"ops deu probreminha rsrs {str(e)}")
