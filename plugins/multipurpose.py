# Plugin mais feio do mundo, mas é só pra um chat específico.
# Aqui temos comandos que são pequenos demais pra terem seu próprio módulo.

# Como esse plugin é ativado por todas as mensagens, o /stats também funcionará por aqui.

# A maioria é um port bem rápido de https://github.com/lucasberti/telegrao/blob/master/plugins/taup.lua

from api import send_message, send_sticker, send_voice
from random import randint, choice, randrange
import json
import re
from PIL import Image
import requests
import os
from io import BytesIO
import plugins.stats as stats
import plugins.ed as ed
import time

emotes = {}

stickers_loaded = False

def on_msg_received(msg, matches):
    chat = msg["chat"]["id"]
    text = msg["text"]
    now = time.time()

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
        for word in text.split():
            if word == emote:
                send_sticker(chat, sticker)
                break

    # /ip
    pattern = re.compile("^[!/]ip(?:@PintaoBot)?$")
    match = pattern.search(text)

    if match:
        send_message(chat, "167.99.230.113 ou ts.lucasberti.me")


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
        send_message(chat, "@berti @beaea @getulhao @rauzao @xisteaga @axasdas @Garzarella @cravetz @giovannovisk @Gbrlcrrts @geysariri")


    # @doteiros
    pattern = re.compile("(?:@dota|@doteiros)")
    match = pattern.search(text)

    if match:
        send_message(chat, "@getulhao @rauzao @axasdas @Garzarella @giovannovisk @Gbrlcrrts @Geysariri\n\n[clica pra abrir....](lucasberti.me/dota)")


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
        send_voice(chat, "AwADAQADRAADgBaoRzTp0hx182Z7Ag")
       

    # bracket
    pattern = re.compile("^[!/]brackets?(?:@PintaoBot)?$")
    match = pattern.search(text)

    if match:
        send_message(chat, "opa masé cllro pepria ai q jajenvio........")

        url_screenshot = "http://api.screenshotlayer.com/api/capture?access_key=6159278b9290544bda694a44c3b38524&url=https://challonge.com/wwe4f8di&viewport=1440x1024&fullpage=1&force=1"
        url = "https://api.telegram.org/" + os.environ['REBORNKEY'] + "/sendPhoto?"
        url += "chat_id=" + str(chat)

        image = Image.open(BytesIO(requests.get(url_screenshot).content))

        result = BytesIO()

        image.crop((115, 555, 1280, 1060)).save(result, "png")

        result.seek(0)
            
        payload = {"photo": ('camp.png', result.read(), 'image/png')}
        response = requests.post(url, files=payload)

        print(response.content)


    # rau
    pattern = re.compile("^rau$")
    match = pattern.search(text)

    if match:
        send_message(chat, "meu pau no seu cu")


    # retcha
    pattern = re.compile("^retcha$")
    match = pattern.search(text)

    if match:
        send_voice(chat, "AwADAQADOgAD980QR0CE3Nf-ksRuAg")


    # xischupano
    pattern = re.compile("^xischupano$")
    match = pattern.search(text)

    if match:
        send_voice(chat, "AwADAQADEAADK3zfBeb564h2rREyAg")


    # retchagemeno 
    pattern = re.compile("^retchagemeno$")
    match = pattern.search(text)

    if match:
        send_voice(chat, "AwADAQADDgADK3zfBXTMW4j5cqevAg")


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

    pattern = re.compile("^(xis|x)$", re.IGNORECASE)
    match = pattern.search(text)

    if match:
        respostas = ["no churrasco", "no trampo", "no metro", "no churras", "na rua", "no assento do cobrador", "no busão", "no bar", "na academia", "na praia", "chegando"]

        resposta = "to " + choice(respostas)
        send_message(chat, resposta)
