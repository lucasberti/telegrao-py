from operator import itemgetter
from os import path
import json
import sqlite3
import time

db = sqlite3.connect("basezinha.db")
c = db.cursor()
c.execute("CREATE TABLE IF NOT EXISTS Tabelinha(msg_id INT, chat_id INT, user_id INT, date DATETIME, user_name TEXT, message TEXT)")

def return_statistics(chat):
    chat = str(chat)
    stats = {}
    total = 0
    result = "PWOERED BU StatTrak™\n\n"

    # Abre e lê o arquivo JSON
    with open("data/stats.json") as fp:
        stats = json.load(fp)

    if chat in stats:
        stats = stats[chat]
    else:
        return "n ten isotirco nesste xet ;()"

    dictofdicts = {}

    # Passa cada usuário do chat pro dictofdicts, onde a chave é o nome e o valor é a qtde.
    for user in stats:
        dictofdicts[stats[user]["name"]] = stats[user]["msg_count"]

    # Ordena a partir dos valores, de forma decrescente.
    for k, v in sorted(dictofdicts.items(), key=itemgetter(1), reverse=True):
        result += k + ": " + str(v) + "\n"
        total += v

    result += "\n\ntootau:::: " + str(total)

    return result


def do_statistics(msg):
    chat_id = str(msg["chat"]["id"])
    from_id = str(msg["from"]["id"])
    name = msg["from"]["first_name"]
    username = msg["from"]["username"] if "username" in msg["from"] else None
    msg_id = msg["message_id"]
    text = msg["text"] or None
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    if text is not None:

        t = (msg_id, chat_id, from_id, timestamp, username, text)

        try:
            with db:
                c.execute("INSERT INTO Tabelinha VALUES (?, ?, ?, ?, ?, ?)", t)
        except Exception as e:
            print(f"Probleminha no banquinho: {e}")


    stats = {}

    # Abre e lê o arquivo JSON
    if path.isfile("data/stats.json"):
        with open("data/stats.json") as fp:
            stats = json.load(fp)

    # Checa se há key do chat no objeto. Se não existir, cria.
    if not chat_id in stats:
        stats[chat_id] = {}

    # Se existir key do usuário no obj do chat, atualiza. Caso contrário, cria.
    if from_id in stats[chat_id]:
        stats[chat_id][from_id]["msg_count"] += 1
    else:
        stats[chat_id][from_id] = {}
        stats[chat_id][from_id]["msg_count"] = 1
        stats[chat_id][from_id]["name"] = name

    # Abre e salva o arquivo JSON
    with open("data/stats.json", "w") as fp:
        json.dump(stats, fp, indent=4, sort_keys=True)
