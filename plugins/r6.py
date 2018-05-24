from api import send_message
import requests
import json

PLAYERS = {
    14160874: "bertoncio",
    16631085: "beaea",
    85867003: "raulg0bbi",
    52451934: "xthedgehog",
    10549434: "axasdas",
    123123862: "MeroFabio"
}


def extract_overall_stats(payload):
    payload = payload["overall"]
    text    = "overau...\n"

    try:
        revives         = payload["revives"] or 0
        reinforcements  = payload["reinforcements_deployed"] or 0
        barricades      = payload["barricades_built"] or 0
        headshots       = payload["headshots"] or 0
        assists         = payload["assists"] or 0
    except Exception as e: 
        return "ops... extract_overall_stats: " + str(e)

    text += "revivel {} amicos\n".format(revives)
    text += "reforso {} pareds...\n".format(reinforcements)
    text += "barriko {} passajes\n".format(barricades)
    text += "deu {} headshovers\n".format(headshots)
    text += "fes {} asists\n\n".format(assists)

    return text


def extract_gamemode_stats(payload, mode):
    text = mode + "\n" 
    
    try:
        has_played  = payload[mode]["has_played"] or 0
        wins        = payload[mode]["wins"] or 0
        losses      = payload[mode]["losses"] or 0
        kills       = payload[mode]["kills"] or 0
        deaths      = payload[mode]["deaths"] or 0
        playtime    = payload[mode]["playtime"] / 60 / 60
    except Exception as e:
        return "ops... extract_gamemode_stats: " + str(e)

    if not has_played:
        text += "nunca jogo\n"
    else:
        text += "ja jogo {:.2f} oras\n".format(playtime)
        text += "ja ganho {} i perdeu {} pratidas ({:.2f} wlr)\n".format(wins, losses, wins / losses)
        text += "ja mato {} i moreu {} veses (kd {:.2f})\n".format(kills, deaths, kills / deaths)

    return text + "\n"


def get_operator_stats(player):
    url = "https://api.r6stats.com/api/v1/players/{}/operators?platform=uplay".format(player)
    stats = "``` "

    try:
        response = json.loads(requests.get(url).content)["operator_records"]
    except Exception as e:
        return "ops deu errinho aki rsrsrs get_operator_stats: " + str(e)

    for operator in response:
        try:
            op_name  = operator["operator"]["name"] + " (" + operator["operator"]["role"] + ")"

            operator = operator["stats"]

            played      = operator["played"] or 0
            wins        = operator["wins"] or 0
            losses      = operator["losses"] or 0
            kills       = operator["kills"] or 0
            deaths      = operator["deaths"] or 0
            playtime    = operator["playtime"]

            if deaths is 0:
                kdr = "n sei qnts"
            else:
                kdr = "{:.2f}".format(kills / deaths)

            if losses is 0:
                wlr = "n sei"
            else:
                wlr = "{:.2f}".format(wins / losses)

            stats += op_name + "\n"
            stats += "ja jogo {} raudes ".format(played)
            stats += "({} segudos q da {:.2f} oras)...\n".format(playtime, playtime / 60 / 60)
            stats += "ganho {} i perdeu {} ({} wlr)...\n".format(wins, losses, wlr)
            stats += "mato {} i moru {} (kdr {})...\n".format(kills, deaths, kdr)
            stats += "\n"
        except Exception as e:
            return "deu pobreminha ao pega os dado get_operator_stats: " + str(e)

    stats += "```"

    return stats


def get_stats(player):
    url = "https://api.r6stats.com/api/v1/players/{}?platform=uplay".format(player)

    try:
        response = json.loads(requests.get(url).content)["player"]
    except Exception as e:
        return "ops deu errinho aki rsrsrs get_stats: " + str(e)

    try:
        playername  = response["username"]

        response    = response["stats"]

        casual_stats    = extract_gamemode_stats(response, "casual")
        ranked_stats    = extract_gamemode_stats(response, "ranked")
        overall_stats   = extract_overall_stats(response)

        level   = response["progression"]["level"] or 0
        xp      = response["progression"]["xp"] or 0

        stats = "``` "
        stats += "{} ta leveu {} c {} d xp (lol nub da poha)...\n\n".format(playername, level, xp)
        stats += casual_stats
        stats += ranked_stats
        stats += overall_stats
        stats += "```"
    except Exception as e:
        return "deu pobreminha ao pega os dado get_stats: " + str(e)

    return stats


def on_msg_received(msg, matches):
    send_message(msg["chat"]["id"], "perai vamo ve....")

    is_looking_for_operators = False
    player = None

    if matches.group(1):
        if matches.group(1) == "op":
            is_looking_for_operators = True

            if msg["from"]["id"] in PLAYERS:
                player = PLAYERS[msg["from"]["id"]]
        else:
            player = matches.group(1)
    else:
        if msg["from"]["id"] in PLAYERS:
            player = PLAYERS[msg["from"]["id"]]

    if player is not None:
        if is_looking_for_operators:
            stats = get_operator_stats(player)
        else:
            stats = get_stats(player)
    else:
        stats = "vc nem tem r6 kkkkk"

    print(stats)

    send_message(msg["chat"]["id"], stats)
