# TODO: Async, !wunder add e talvez descobrir um jeito de não cortar a imagem

import datetime
import json
import requests
import api

gUrlConditions  = "http://api.wunderground.com/api/dbcee4e7c140bb2d/lang:BR/conditions/forecast/q/"
gUrlSatellite   = "http://api.wunderground.com/api/dbcee4e7c140bb2d/animatedsatellite/q/"


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
        json.dump(locations, fp)


def resolve_location(user_id):
    user_id     = str(user_id)
    locations   = load_locations()

    if user_id in locations:
        return locations[user_id]
    else:
        return None


def get_conditions_and_forecast(place):
    url = gUrlConditions
    url += place + ".json"

    response = requests.get(url)
    response = json.loads(response.content)

    return response


def get_satellite_url(place):
    return gUrlSatellite + place + ".gif?basemap=1&timelabel=1&timelabel.y=10&num=5&delay=50&radius=500&radunits=km&borders=1&key=sat_ir4"


def process_conditions(conditions):
    conditions_dict = {
        "": "pora n sei n da pra ve",
        "Bruma": "VEI TA TD BRAMCO",
        "Céu Limpo": "LINPIN LINPJIN",
        "Céu Encoberto": "ceu coberto con 1 endredonm",
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


def generate_string(data):
    conditions  = data["current_observation"]
    forecast    = data["forecast"]["simpleforecast"]["forecastday"]

    cityname    = conditions["display_location"]["full"]
    temp_c      = conditions["temp_c"]
    feels_c     = conditions["feelslike_c"]
    weather     = conditions["weather"]
    station     = conditions["observation_location"]["city"]
    obs_time    = conditions["observation_time_rfc822"]
    humidity    = conditions["relative_humidity"]
    wind_vel    = conditions["wind_kph"]
    wind_from   = conditions["wind_dir"]

    header  = ""
    footer  = ""
    now     = datetime.datetime.now()

    header = "EITA PORA a tenps em " + cityname + " eh d " + str(temp_c)
    header += " con uma sensasaosinha d " + str(feels_c) + "\n"
    header += "a parti da estasao meteurolojics la em " + station + " em " + obs_time[5:] + "\n"
    header += "umanidade di " + humidity + "\n"
    header += "uns veto vino a " + str(wind_vel) + " narizes do retcha/h de " + wind_from + "\n"
    header += "atlamente la ta ó::::::: " + process_conditions(weather)

    # Se já é noite, pegue a previsão do dia seguinte. (index 0 é hoje, 1 é amanhã)
    if now.hour >= 18:
        forecast_max    = forecast[1]["high"]["celsius"]
        forecast_min    = forecast[1]["low"]["celsius"]
        precipitation   = forecast[1]["pop"]
        conditions      = process_conditions(forecast[1]["conditions"])

        footer = "\n\ni sera q vai chove amanh??????\n"
        footer += conditions + " con una prporlbindade d presiispatasao d " + str(precipitation) + "\n"
        footer += "másima d " + forecast_max + " minim d " + forecast_min
    else:
        forecast_max    = forecast[0]["high"]["celsius"]
        forecast_min    = forecast[0]["low"]["celsius"]
        precipitation   = forecast[0]["pop"]
        conditions      = process_conditions(forecast[0]["conditions"])

        footer = "\n\ni sera q vai chove hj????\n"
        footer += conditions + " con una prporlbindade d presiispatasao d " + str(precipitation) + "\n"
        footer += "másima d " + forecast_max + " minim d " + forecast_min

    return header + footer


def on_msg_received(msg, matches):
    chat        = msg["chat"]["id"]
    user        = msg["from"]["id"]
    location    = resolve_location(user)

    if location is None:
        api.send_message(chat, "vei n sei qaltua cdd..... use */wunder add [estacao]* <<<------- botassua eksltaçao ali rs")
        return

    data            = get_conditions_and_forecast(location)
    satellite_img   = get_satellite_url(location)
    message         = generate_string(data)

    api.send_document(chat, satellite_img)
    api.send_message(chat, message)
