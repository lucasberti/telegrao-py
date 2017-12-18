from api import send_message
import markovify

def on_msg_received(msg, matches):
    
    chat = msg["chat"]["id"]

    with open("/root/paitons/telegrao-py/data/log.txt") as f:
        model = markovify.NewlineText(f.read())

    text = None

    if matches.group(1):
        try:
            text = model.make_sentence_with_start(matches.group(1), strict=False, tries=25)
        except:
            send_message(chat, "a olha minha cabeca explsodiu fazendo essa frase tenta otra coisa....")
    else:
        text = model.make_sentence(tries=25)

    if text is not None:
        send_message(chat, text)
    else:
        send_message(chat, "vo fala nd")
