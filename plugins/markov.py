from api import send_message
import markovify

def on_msg_received(msg, matches):
    with open("/root/telegram-bot/wordcloud.txt") as f:
        model = markovify.NewlineText(f.read())

    text = model.make_sentence(tries=25)

    chat = msg["chat"]["id"]
    send_message(chat, text)
