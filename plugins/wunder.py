# TODO: Async, !wunder add e talvez descobrir um jeito de não cortar a imagem

import datetime
import json
import requests
import api
import os

base_url        = "https://api.weather.com/v2/pws/observations/current"
conditions_url  = "https://api.weather.com/v3/wx/observations/current" # só pra pegar o texto de current
api_key = os.getenv("OPENAI_REV_PASSWORD")


def load_locations():
    locations = None

    with open("data/wunder.json") as fp:
        locations = json.load(fp)

    return locations


def add_entry(user_id, location):
    user_id     = str(user_id)
    locations   = load_locations()

    locations[user_id] = location

    with open("data/wunder.json", "w") as fp:
        json.dump(locations, fp, indent=2)


def resolve_location(user_id):
    user_id     = str(user_id)
    locations   = load_locations()

    if user_id in locations:
        return locations[user_id]
    else:
        return None


def get_additional_info(info):
    geocode = str(info["lat"])[:7] + "," + str(info["lon"])[:7]
    
    params = {
        "apiKey": api_key,
        "units": "m",
        "geocode": geocode,
        "language": "pt-BR",
        "format": "json"
    }

    return requests.get(conditions_url, params=params).json()


def get_current_conditions(place):
    params = {
        "apiKey": api_key,
        "units": "m",
        "format": "json"
    }

    if len(place) == 4:
        params['icaoCode'] = place
        params['language'] = "pt-BR"

        response = requests.get(conditions_url, params=params).json()
    else:
        params['stationId'] = place
        
        response = requests.get(base_url, params=params).json()["observations"][0]

    return response


def process_conditions(conditions):
    conditions_dict = {
        "": "pora n sei n da pra ve",
        "Bruma": "VEI TA TD BRAMCO",
        "Limpo": "LINPIN LINPJIN",
        "Encoberto": "ceu coberto con 1 endredonm",
        "Chuva": "i vai chove em",
        "Chuva Fraca": "una chuvinia lvevina",
        "Chuviscos Fracos": "una chuvinia fraquinia hummmmmmmmm",
        "Muito Nublado": "muitas nuve",
        "Neblina": "presemsa d esnop dog",
        "Nuvens Dispersas": "umas nove espalhada",
        "Parcialmente Nublado": "1as nuve por ai",
        "Possibilidade de Chuva": "vix tauves vai cai umas agua",
        "Possibilidade de Trovoada": "i tauves vai da us trovao em",
        "Trovoada": "vei vai da ums trovao mASA",
        "Trovoadas com Chuva": "1s trovao c chuv",
        "Trovoadas Fracas e Chuva": "troamvãoiizn i xhuvaaaaa"
    }

    if conditions in conditions_dict:
        return conditions_dict[conditions]
    else:
        return conditions


def generate_string(data, additional):
    if 'metric' in data.keys():
        cityname    = data["neighborhood"]
        temp_c      = data["metric"]["temp"]
        feels_c     = data["metric"]["heatIndex"]
        wind_vel    = data["metric"]["windSpeed"]
        station     = data["neighborhood"]
        obs_time    = data["obsTimeLocal"]
        humidity    = data["humidity"]
        weather     = additional["cloudCoverPhrase"]
    else:
        cityname    = ""
        temp_c      = data["temperature"]
        feels_c     = data["temperatureFeelsLike"]
        wind_vel    = data["windSpeed"]
        station     = ""
        obs_time    = data["validTimeLocal"]
        humidity    = data["relativeHumidity"]
        weather     = data["cloudCoverPhrase"]

    header  = ""

    if cityname != "":
        header += "EITA PORA a tenps em {} eh d {} con uma sensasaosinha d {}\n".format(cityname, temp_c, feels_c)
        header += "a parti da estasao meteurolojics la em {} em {}\n".format(station, obs_time)
    else:
        header += "EITA PORA a tenps eh d {} con uma sensasaosinha d {}\n".format(temp_c, feels_c)

    header += "umanidade di {}\n".format(humidity)
    header += "uns veto vino a {} narizes do retcha/h\n".format(wind_vel)
    header += "atlamente la ta ó::::::: {}".format(process_conditions(weather))

    return header


def on_msg_received(msg, matches):
    chat        = msg["chat"]["id"]
    user        = msg["from"]["id"]

    args = matches.group(1)

    if len(args) > 0:
        args = args.split(" ")
        if args[0] != "add":
            location = args
        else:
            add_entry(user, " ".join(args[1:]))
            api.send_message(chat, "aewwwwww agr sei ondnd q peoga as info =]\nagr r voc epode ffzere /wunder ok")
            return

    else:
        location = resolve_location(user)

    if location is None:
        api.send_message(chat, "vei n sei qaltua cdd..... use */wunder add [estacao]* <<<------- botassua eksltaçao ali rs")
        return

    try:
        data = get_current_conditions(location)

        if len(location) != 4:
            additional = get_additional_info(data)
        else:
            additional = None

        message = generate_string(data, additional) 

        print(data, message)

        api.send_message(chat, message)
        
    except Exception as e:
        api.send_message(chat, f"ops deu pobreminha rsrsrs: {e}")
        pass

# location = "SBDN"
# data            = get_current_conditions(location)
# if len(location) != 4:
#     additional  = get_additional_info(data)
# else:
#     additional = None

# message         = generate_string(data, additional) 

# print(data, message)
