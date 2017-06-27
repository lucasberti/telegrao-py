from reborn import log
import os
import json

plugins = {}
disabled_plugins = {}
config = {}


def load_config():
    """ Carrega o arquivo json e retorna um objeto com as configurações. """
    if os.path.isfile("data/config.json"):
        with open("data/config.json") as fp:
            global config
            config = json.load(fp)
    else:
        log("Arquivo de config não encontrado.")
        exit(6924)


def save_config():
    """ Salva o objeto JSON atual pro arquivo. """
    global config
    config["enabled_plugins"] = plugins
    config["disabled_plugins"] = disabled_plugins

    with open("data/config.json", "w") as fp:
        json.dump(config, fp, indent=4)


def load_plugins():
    global plugins
    global disabled_plugins
    global config

    plugins = config["enabled_plugins"]
    disabled_plugins = config["disabled_plugins"]


load_config()
load_plugins()
