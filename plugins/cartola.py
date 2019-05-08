import requests
from api import send_message

def get_matches():
    endpoint = "https://api.cartolafc.globo.com/partidas"

    result = ""
    try:
        response = requests.get(endpoint).json()

        result = ""
        for partida in response["partidas"]:
            clube_casa = partida["clube_casa_id"]
            clube_casa_nome = response["clubes"][str(clube_casa)]["nome"]

            clube_visitante = partida["clube_visitante_id"]
            clube_visitante_nome = response["clubes"][str(clube_visitante)]["nome"]
            
            data = partida["partida_data"]
            url = partida["url_transmissao"]

            placar_oficial_mandante = partida["placar_oficial_mandante"]
            placar_oficial_visitante = partida["placar_oficial_visitante"]

            if url != "":
                result += f"[{clube_casa_nome} vs {clube_visitante_nome}: {data}]({url})\n\n"
            else:
                result += f"{clube_casa_nome} vs {clube_visitante_nome}: {data}\n\n"

            if placar_oficial_mandante is not None and placar_oficial_visitante is not None:
                result += f"{clube_casa_nome} {placar_oficial_mandante} vs {placar_oficial_visitante} {clube_visitante_nome}: {data}\n\n"

        print(result)
    except:
        pass

    return result


def get_ranking():
    endpoint = "https://api.cartolafc.globo.com/auth/liga/o-famoso-campeonato-do-peido"

    headers = {
        "X-GLB-Token": "158cf8e32e385eb1670f4f63d89530867747579713076797a79756d756b35356a50556f714471744743626875716b646a5271364a55336744476e7a306d53773646586d4974786557674e306442307833684a6e30434d7141584d583253737749733570534a513d3d3a303a756878666c616d6b6e717278676466726b6f7262"
    }

    result = "-50 | -20 | -15 | -10 | -5 | 0 | +100\n"
    try:
        response = requests.get(endpoint, headers=headers).json()
        for time in response["times"]:
            total_points = time["pontos"]["campeonato"] or 0
            round_points = time["pontos"]["rodada"] or 0

            result += f"{time['nome']} ({time['nome_cartola']}): {time['ranking']['campeonato']}º\n({round_points:.2f} / {total_points:.2f})\n\n"
    except:
        pass

    return result

def on_msg_received(msg, matches):
    chat = msg["chat"]["id"]
    
    resposta = ""
    if matches.group(1):
        match = matches.group(1)

        print(match)
        if match == "partidas":
            print("rs")
            resposta = get_matches()
    else:
        resposta = get_ranking()

    send_message(chat, resposta)
