from operator import itemgetter
from os import path
import json

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