# Most of this script came from https://scorebot-secure.hltv.org/scorebotClientApi.js?v5, property of HLTV.org
# This is just a simple Telegram bot querying their data, publicly available @ HLTV.org during matches.

from socketIO_client import SocketIO  # instale "socketIO-client" via pip pra funcionar
from reborn import log
import time
import api
import json
import threading
import re


class MessageHandler(object):
    def __init__(self):
        self.is_running = False
        self.received_log_history = False
        self.presented_initial_scoreboard = False
        self.simple_mode = False

        self.alive_tr = []
        self.alive_ct = []
        self.scoreboard_msg_id = 0
        self.log_msg_id = 0

        self.last_score_update = time.time()

        self.chat_id = 0

        self.scoreboard_msg = ""
        self.log_msg = ""

    def set_scoreboard_msg(self, message):
        self.scoreboard_msg = message

    def add_log_msg(self, message):
        self.log_msg += "\n -- " + message

    def resend_messages(self):
        if self.log_msg_id != 0:
            api.delete_message(self.chat_id, self.log_msg_id)
            log("reenviando log...")
            self.log_msg_id = api.send_message(self.chat_id, self.log_msg, parse_mode="")["result"]["message_id"]

        if self.scoreboard_msg_id != 0:
            api.delete_message(self.chat_id, self.scoreboard_msg_id)
            log('reenviando score...')
            self.scoreboard_msg_id = api.send_message(self.chat_id, self.scoreboard_msg, parse_mode="")["result"]["message_id"]

    def clear_log_msg(self):
        self.log_msg = ""

    def update_log(self):
        log("atualizando log...")
        api.edit_message_text(self.chat_id, self.log_msg_id, self.log_msg, parse_mode="")

    def update_scoreboard(self):
        log("atualizando scoreboard...")
        api.edit_message_text(self.chat_id, self.scoreboard_msg_id, self.scoreboard_msg, parse_mode="")


opt = MessageHandler()
socketio = SocketIO("scorebot2.hltv.org", 10022)


def on_log(*args):
    # Se teve atualização de log, com certeza teve atualização de scoreboard.
    opt.update_scoreboard()

    # Evita printar o histórico completo da partida.
    if not opt.received_log_history:
        opt.received_log_history = True
        return

    # Corrige nome de players com caracteres que a API do Telegram não parseia.
    proper_string = str(args[0]).replace("#", "%23").replace("&", "%26")

    entries = json.loads(proper_string)["log"][0]

    for event in entries:
        # Simple Mode só mostra o que aconteceu no fim do round.
        if opt.simple_mode and event != "RoundEnd":
            return

        details = entries[event]

        if event == "Kill":
            hs = ""

            if details["headShot"]:
                hs = " (hs)"

            opt.add_log_msg(details["killerName"] + " (" + details["killerSide"] + ") matou " + details["victimName"] + " (" + details["victimSide"] + ") com " + details["weapon"] + hs)

        elif event == "BombPlanted":
            opt.add_log_msg(details["playerName"] + " plantou a bomba com " + str(details["ctPlayers"]) + " CTs e " + str(details["tPlayers"]) + " TRs")

        elif event == "BombDefused":
            opt.add_log_msg(details["playerName"] + " defusou a bomba")

        elif event == "MatchStarted":
            opt.add_log_msg("PARTIDA INICIANDO...")

        elif event == "RoundStart":
            opt.clear_log_msg()
            opt.add_log_msg("ROUND INICIANDO...")
            opt.resend_messages()

        elif event == "RoundEnd":
            reason = ""

            if details["winType"] == "Target_Bombed":
                reason = " (bomba explodiu)"
            elif details["winType"] == "Bomb_Defused":
                reason = " (bomba defusada)"

            message = "FIM DE ROUND. " + details["winner"] + " GANHOU" + reason + ".\nSCORE DO HALF: TR " + str(details["terroristScore"]) + " - " + str(details["counterTerroristScore"]) + " CT"

            if opt.simple_mode:
                api.send_message(opt.chat_id, message)
                return
            else:
                opt.add_log_msg(message)
        else:
            return

    opt.update_log()


def on_scoreboard(*args):
    proper_string = str(args[0]).replace("'", '"').replace("True", '"True"').replace("False", '"False"')
    proper_string = proper_string.encode("utf8")

    entries = json.loads(proper_string)

    tr_players = entries["TERRORIST"]
    ct_players = entries["CT"]

    for i in range(0, 5):
        tr_name = tr_players[i]["name"]
        ct_name = ct_players[i]["name"]

        if tr_players[i]["alive"] == "True" and tr_name not in opt.alive_tr:
            opt.alive_tr.append(tr_name)
        elif tr_players[i]["alive"] == "False" and tr_name in opt.alive_tr:
            opt.alive_tr.remove(tr_name)

        if ct_players[i]["alive"] == "True" and ct_name not in opt.alive_ct:
            opt.alive_ct.append(ct_name)
        elif ct_players[i]["alive"] == "False" and ct_name in opt.alive_ct:
            opt.alive_ct.remove(ct_name)

    scoreboard = ""
    scoreboard += entries["terroristTeamName"] + " (TR) " + str(entries["terroristScore"]) + " vs. "
    scoreboard += str(entries["counterTerroristScore"]) + " (CT) " + entries["ctTeamName"] + "\n"
    scoreboard += "\nVIVOS: TR " + str(len(opt.alive_tr)) + " vs. " + str(len(opt.alive_ct)) + " CT"
    scoreboard += "\nMAPA: " + entries["mapName"]
    scoreboard += "\nROUND: " + str(entries["currentRound"])

    if entries["bombPlanted"] == "True":
        scoreboard += "\nBOMBA PLANTADA 🔴"

    opt.scoreboard_msg = scoreboard

    # Faz com que só o primeiro evento de scoreboard atualize a mensagem.
    # Esse evento acontece muitas vezes. É melhor deixar que só o evento de log atualize a mensagem de scoreboard.
    if not opt.presented_initial_scoreboard:
        opt.update_scoreboard()
        opt.presented_initial_scoreboard = True


def on_connect(*args):
    print("Scorebot conectado.")
    opt.is_running = True


def get_infos_from_match(matchid):
    matchid = str(matchid)

    print("Conectando ao scorebot...")

    socketio.on("connect", on_connect)

    socketio.on("scoreboard", on_scoreboard)
    socketio.on("log", on_log)
    socketio.emit("readyForMatch", matchid)
    socketio.wait()


def perform_exit():
    log("Parando de acompanhar...")
    socketio.off("scoreboard")
    socketio.off("log")

    socketio.wait(seconds=1)

    opt.add_log_msg("ae carai to me desligano ta bom tchau")
    opt.update_log()


def on_msg_received(msg, matches):
    opt.chat_id = msg["chat"]["id"]

    # opt.log_msg_id = api.send_message(opt.chat_id, "esperando algo acontecer...")["result"]["message_id"]
    # opt.scoreboard_msg_id = api.send_message(opt.chat_id, "esperando scoreboard...")["result"]["message_id"]

    if re.match("(?:stop|parar?|cancelar?)", matches.group(1)):
        if opt.is_running:
            perform_exit()
        return

    if matches.group(2) is not None:
        if re.match("(?:simples?|clean|resumido)", matches.group(1)):
            opt.simple_mode = True

        thread = threading.Thread(name="hltvThread", target=get_infos_from_match, args=(matches.group(2),))
        # get_infos_from_match(matches.group(2))
    else:
        thread = threading.Thread(name="hltvThread", target=get_infos_from_match, args=(matches.group(1),))
        # get_infos_from_match(matches.group(1))

    opt.scoreboard_msg_id = api.send_message(opt.chat_id, "esperando scoreboard...")["result"]["message_id"]

    # Simple Mode só não vai ter log, mas scoreboard continua sendo atualizado.
    if not opt.simple_mode:
        opt.log_msg_id = api.send_message(opt.chat_id, "esperando algo acontecer...")["result"]["message_id"]

    thread.start()
