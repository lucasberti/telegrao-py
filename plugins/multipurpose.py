# Plugin mais feio do mundo, mas é só pra um chat específico.
# Aqui temos comandos que são pequenos demais pra terem seu próprio módulo.

# Como esse plugin é ativado por todas as mensagens, o /stats também funcionará por aqui.

# A maioria é um port bem rápido de https://github.com/lucasberti/telegrao/blob/master/plugins/taup.lua

from api import send_message
from random import randint
import re
import plugins.stats as stats
import plugins.ed as ed


def on_msg_received(msg, matches):
    chat = msg["chat"]["id"]
    text = msg["text"]

    stats.do_statistics(msg)
    ed.run_ed(msg)

    # Precisamos manter log de todas as mensagens pro /xet e /wordcloud
    with open("data/log.txt", "a", encoding='utf-8') as f:
        f.write(text + "\n")

    # /ip
    pattern = re.compile("^[!/]ip(?:@PintaoBot)?$")
    match = pattern.search(text)

    if match:
        send_message(chat, "64.137.208.17")


    # /mps
    pattern = re.compile("^[!/]mps(?:@PintaoBot)?$")
    match = pattern.search(text)

    if match:
        send_message(chat, "ok to calculando aki q esistem " + str(randint(500, 10000)) + "/s por segundo de SUPER MAEMES NESNTE CHAT1")


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
        send_message(chat, "@berti @beaea @getulhao @rauzao @xisteaga @axasdas")


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