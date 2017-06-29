import config
from api import send_message
from reborn import is_sudoer

def on_msg_received(msg, matches):
    # Checa se o usuário tem permissão e tem a quantidade correta de args no comando

    command = matches.group(2)
    plugin = matches.group(3)

    if command is None and plugin is None:
        string = ""
        string += "atvdos::::: \n"

        if len(config.plugins.items()) == 0:
            string += "neñum rs"
        else:
            for query, plu in config.plugins.items():
                string += plu + "✔️ \n"

        string += "\ndesatvsd::: \n"

        if len(config.disabled_plugins.items()) == 0:
            string += "neñum rs"
        else:
            for query, plu in config.disabled_plugins.items():
                string += plu + "❌ \n"

        send_message(msg["chat"]["id"], string)

    elif is_sudoer(msg["from"]["id"]) and command is not None and plugin is not None:
        if command == "enable":
            for query, plu in config.plugins.items():
                # Se o plugin passado for encontrado nos plugins ativos, avisa e sai da função.
                if plugin == plu:
                    send_message(msg["chat"]["id"], "pora o " + plugin + "ja ta ativado burro")
                    return

            for query, plu in config.disabled_plugins.items():
                # Se o plugin estiver inativo, troca de posição, salva e recarrega.
                if plugin == plu:
                    config.disabled_plugins.pop(query)
                    config.plugins[query] = plu
                    config.save_config()
                    config.load_config()

                    send_message(msg["chat"]["id"], "ae carai o " + plugin + "agr ativado carai.....")
                    return

        elif command == "disable":
            for query, plu in config.disabled_plugins.items():
                # Se o plugin passado for encontrado nos plugins desativados, avisa e sai da função.
                if plugin == plu:
                    send_message(msg["chat"]["id"], "pora o " + plugin + " ja ta disativado burro")
                    return

            for query, plu in config.plugins.items():
                # Se o plugin estiver ativo, troca de posição, salva e recarrega.
                if plugin == plu:
                    config.plugins.pop(query)
                    config.disabled_plugins[query] = plu
                    config.save_config()
                    config.load_config()

                    send_message(msg["chat"]["id"], "ae carai o " + plugin + "agr disisativado carai.....")
                    return