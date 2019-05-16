# Plugin mais feio do mundo, mas é só pra um chat específico.
# Aqui temos comandos que são pequenos demais pra terem seu próprio módulo.

# Como esse plugin é ativado por todas as mensagens, o /stats também funcionará por aqui.

# A maioria é um port bem rápido de https://github.com/lucasberti/telegrao/blob/master/plugins/taup.lua

from api import send_message, send_sticker, send_document, send_photo, send_voice
from random import randint, choice, randrange
from datetime import datetime
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
arrobas = {}

stickers_loaded = False
arrobas_loaded = False


def on_msg_received(msg, matches):
    chat = msg["chat"]["id"]
    text = msg["text"]
    now = time.time()

    stats.do_statistics(msg)
    ed.run_ed(msg)

    dicionario = {
    "^[!/]ip(?:@PintaoBot)?$": {
        "text": ["167.99.230.113 ou ts.lucasberti.me"]
    },
    "^[!/]mps(?:@PintaoBot)?$": {
        "text": [f"ok to calculando aki q esistem {str(randint(500, 10000))}/s por segundo de SUPER MAEMES NESNTE CHAT1"]
    },
    "^[!/]dougscore(?:@PintaoBot)?$": {
        "text": [f"ok to calculando aki q o dougscore é {str(randint(0, 100))}"]
    },
    "^[!/]stats(?:@PintaoBot)?$": {
        "text": [stats.return_statistics(chat)]
    },
    "^[!/]cartola(?:@PintaoBot)?$": {
        "text": ["-50 | -20 | -15 | -10 | -5 | 0 | +100"]
    },
    "^[!/]historia(?:@PintaoBot)?$": {
        "text": ["youtube.com/watch?v=ZkwdNcrIbxs"],
        "voice": ["AwADAQADRAADgBaoRzTp0hx182Z7Ag", "AwADAQADTwADRojZRSmcrD6Nylp7Ag"]
    },
    "^\?$": {
        "text": ["?"]
    },
    "^calma$": {
        "text": ["ok esto mais calmo obrigada"]
    },
    "^vc esta ai$": {
        "text": ["SIM, TÔ AQUI PORA"]
    },
    "^indignada$": {
        "voice": ["AwADAQADVwADMWFARkEqR2T39LDpAg"]
    },
    "^burn$": {
        "voice": ["AwADAQADPwADdMhpRu8AAd9hgtCNFwI", "AwADAQADQAADdMhpRusXWyvZVk-5Ag"]
    },
    "^axasdas$": {
        "text": [choice(["?", "!escolhe berti lixo ou berti top", "nunca fui sub do phantomlord"])],
        "sticker": ["CAADAQADOwADaXQpRqZjRHmRgc2XAg"]
    },
    "^geta$": {
        "sticker": ["CAADAQADRAADl6BoRbfstbst5IT7Ag"],
        "document": ["CQADAQADfwADx7KpRxytpuyVqkkJAg"],
        "photo": ["https://i.imgur.com/O5Ihe8x.png"]
    },
    "^rau$": {
        "text": ["meu pau no seu cu"],
        "voice": ["AwADAQADOgAD980QR0CE3Nf-ksRuAg"]
    },
    "^retcha$": {
        "voice": ["AwADAQADOgAD980QR0CE3Nf-ksRuAg"]
    },
    "^retchagemeno$": {
        "voice": ["AwADAQADDgADK3zfBXTMW4j5cqevAg"]
    },
    "^xischupano$": {
        "voice": ["AwADAQADEAADK3zfBeb564h2rREyAg"]
    }
}


    # Precisamos manter log de todas as mensagens pro /xet e /wordcloud
    with open("data/log.txt", "a", encoding='utf-8') as f:
        f.write(text + "\n")

    if chat == -1001299644323:
        with open("/var/www/html/xet.txt", "a", encoding='utf-8') as f:
            f.write(f"{msg['from']['username']}: {text}\n")


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


    if not arrobas_loaded:
        try:
            with open("data/arrobas.json") as f:
                arrobas = json.load(f)
        except Exception as e:
            print(e)

    for arroba in arrobas.keys():
        if arroba in text:
            send_message(chat, " ".join(arrobas[arroba]))


    for pat in dicionario:
        pattern = re.compile(pat)
        match = pattern.search(text)

        if match:
            if "text" in dicionario[pat].keys():
                for entry in dicionario[pat]["text"]:
                    send_message(chat, entry)

            if "photo" in dicionario[pat].keys():
                for entry in dicionario[pat]["photo"]:
                    send_photo(chat, entry)

            if "voice" in dicionario[pat].keys():
                for entry in dicionario[pat]["voice"]:
                    send_voice(chat, entry)

            if "sticker" in dicionario[pat].keys():
                for entry in dicionario[pat]["sticker"]:
                    send_sticker(chat, entry)

            if "document" in dicionario[pat].keys():
                for entry in dicionario[pat]["document"]:
                    send_document(chat, entry)

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


    # foda
    pattern = re.compile("^foda$")
    match = pattern.search(text)

    if match and msg["from"]["id"] == 10549434:
        send_message(chat, "FODA!!!!")

    # fé
    pattern = re.compile("(.*) fé$", re.IGNORECASE)
    match = pattern.search(text)

    if match:
        verbo = match.group(1)
        
        dicio = {
            "boto": "botada",
            "adiciono": "adicionada",
            "acrescento": "acrescentada",
            "ponho": "posta",
            "introduzo": "introduzida",
            "coloco": "colocada",
            "insiro": "inserida",
            "meto": "metida",
            "somo": "somada",
            "agrego": "agregada",
            "incorporo": "incorporada",
            "aplico": "aplicada",        
            "incluo": "incluída",
            "atribuo": "atribuída",
            "atiro": "atirada",
            "arrumo": "arrumada",
            "posiciono": "posicionada",
            "instalo": "instalada",
            "estabeleço": "estabelecida"        
        }

        if verbo in dicio:
            with open("data/fesdepositadas.txt", "r+") as f:
                fes = int(f.readline())
                f.seek(0)
                f.write(str(fes+1))
                send_message(chat, f"fé nº {fes} {dicio[verbo]} com sucesso")    
        else:
            send_message(chat, "eh muinto pra min naum consigo faser isso com a fé")                         
                    
    # encontro
    pattern = re.compile("^[!/]encontro$")
    match = pattern.search(text)

    if match:
        encontro = datetime.fromtimestamp(1562900400)
        delta = encontro - datetime.now()

        send_message(chat, f"fautão {delta.days} dias pro encontronrn!!!!!!!")


    # x
    pattern = re.compile("^(xis|x)$", re.IGNORECASE)
    match = pattern.search(text)

    if match:
        respostas = ["no churrasco", "no trampo", "no metro", "no churras", "na rua", "no assento do cobrador", "no busão", "no bar", "na academia", "na praia", "chegando"]

        resposta = "to " + choice(respostas)
        send_message(chat, resposta)
