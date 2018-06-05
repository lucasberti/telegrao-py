# Plugin mais feio do mundo, mas é só pra um chat específico.
# Aqui temos comandos que são pequenos demais pra terem seu próprio módulo.

# Como esse plugin é ativado por todas as mensagens, o /stats também funcionará por aqui.

# A maioria é um port bem rápido de https://github.com/lucasberti/telegrao/blob/master/plugins/taup.lua

from api import send_message, send_sticker
from random import randint, choice, randrange
import json
import re
import plugins.stats as stats
import plugins.ed as ed

emotes = {}

stickers_loaded = False

def on_msg_received(msg, matches):
    chat = msg["chat"]["id"]
    text = msg["text"]

    stats.do_statistics(msg)
    ed.run_ed(msg)

    # Precisamos manter log de todas as mensagens pro /xet e /wordcloud
    with open("data/log.txt", "a", encoding='utf-8') as f:
        f.write(text + "\n")


    if not stickers_loaded:
        try:
            with open("data/emotes.json") as f:
                emotes = json.load(f)
        except Exception as e:
            print(e)

    for emote, sticker in emotes.items():
        if emote in text:
            send_sticker(chat, sticker)
            break


    # /ip
    pattern = re.compile("^[!/]ip(?:@PintaoBot)?$")
    match = pattern.search(text)

    if match:
        send_message(chat, "198.211.102.201")

    # /ultimavez
    pattern = re.compile("^[!/]ultimavez$")
    match = pattern.search(text)

    if match:
        send_message(chat, "hashtag ERVt21tByA")

    # /mps
    pattern = re.compile("^[!/]mps(?:@PintaoBot)?$")
    match = pattern.search(text)

    if match:
        send_message(chat, "ok to calculando aki q esistem " + str(randint(500, 10000)) + "/s por segundo de SUPER MAEMES NESNTE CHAT1")

    # /dougscore
    pattern = re.compile("^[!/]dougscore(?:@PintaoBot)?$")
    match = pattern.search(text)

    if match:
        send_message(chat, "ok to calculando aki q o dougscore é " + str(randint(0, 100)))

    # /stats
    pattern = re.compile("^[!/]stats(?:@PintaoBot)?$")
    match = pattern.search(text)

    if match:
        result = stats.return_statistics(chat)
        send_message(chat, result)


    # @todos
    pattern = re.compile("(?:@todos|@todomundo)")
    match = pattern.search(text)

    if match:
        send_message(chat, "@berti @beaea @getulhao @rauzao @xisteaga @axasdas @Garzarella @cravetz")


    # calma
    pattern = re.compile("^calma$")
    match = pattern.search(text)

    if match:
        send_message(chat, "ok esto mais calmo obrigada")


    # vc esta ai
    pattern = re.compile("^vc esta ai$")
    match = pattern.search(text)

    if match:
        send_message(chat, "SIM, TÔ AQUI PORA")


    # celso
    pattern = re.compile("^[!/]historia(?:@PintaoBot)?$")
    match = pattern.search(text)

    if match:
        send_message(chat, "youtube.com/watch?v=ZkwdNcrIbxs")

 
    # rau
    pattern = re.compile("^rau$")
    match = pattern.search(text)

    if match:
        send_message(chat, "meu pau no seu cu")


    # axasdas
    pattern = re.compile("^axasdas$")
    match = pattern.search(text)

    if match:
        respostas = ["?", "lucas berti viado", "nunca fui sub do phantomlord", "caguei agua no trabalho"]

        send_sticker(chat, "CAADBAAD6wADfrn7B7Y17rsYOjoeAg")
        send_sticker(chat, "CAADBQADgAADDGCzCL91O-bq3xxEAg")
        send_message(chat, choice(respostas))

    # foda
    pattern = re.compile("^foda$")
    match = pattern.search(text)

    if match and msg["from"]["id"] == 10549434:
        send_message(chat, "FODA!!!!")


