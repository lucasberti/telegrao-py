import json
import os
import requests

def get_updates(offset=0, timeout=60):
    """ Por default, faz longpoll. Retorna uma array de Update """
    url = "https://api.telegram.org/" + os.environ['REBORNKEY'] + "/getUpdates?"
    url += "offset=" + str(offset) + "&"
    url += "timeout=" + str(timeout) + "&"

    try:
        response = requests.get(url)
        response = json.loads(response.content)
    except Exception:
        return None

    if response["ok"] is True:
        return response["result"]
    else:
        return None


def send_message(chat_id, text, parse_mode="", reply_to_message_id="", reply_markup="", disable_web_page_preview="false"):
    """ reply_markup não é apenas ID, é uma array com opções. """
 
    #text = text.replace("c", "k").replace("qu", "k")
    url = "https://api.telegram.org/" + os.environ['REBORNKEY'] + "/sendMessage?"
    url += "chat_id=" + str(chat_id) + "&"
    url += "text=" + text + "&"
    url += "disable_web_page_preview=" + disable_web_page_preview + "&" 
    url += "parse_mode=" + parse_mode + "&"
    if reply_to_message_id:
        url += "reply_to_message_id=" + str(reply_to_message_id) + "&"
    if reply_markup:
        url += "reply_markup=" + str(reply_markup)

    response = requests.get(url)
    response = json.loads(response.content)

    print(response)

    return response


def edit_message_text(chat_id, msg_id, text, parse_mode="Markdown", reply_to_message_id="", reply_markup=""):
    """ reply_markup não é apenas ID, é uma array com opções. """
    url = "https://api.telegram.org/" + os.environ['REBORNKEY'] + "/editMessageText?"
    url += "chat_id=" + str(chat_id) + "&"
    url += "message_id=" + str(msg_id) + "&"
    url += "text=" + text + "&"
    url += "parse_mode=" + parse_mode + "&"
    if reply_to_message_id:
        url += "reply_to_message_id=" + str(reply_to_message_id) + "&"
    if reply_markup:
        url += "reply_markup=" + str(reply_markup)

    response = requests.get(url)
    response = json.loads(response.content)

    return response


def delete_message(chat_id, msg_id):
    url = "https://api.telegram.org/" + os.environ['REBORNKEY'] + "/deleteMessage?"
    url += "chat_id=" + str(chat_id) + "&"
    url += "message_id=" + str(msg_id)

    response = requests.get(url)
    response = json.loads(response.content)

    return response


def send_photo(chat_id, photo_url, caption="", reply_to_message_id=0):
    """ reply_markup não é apenas ID, é uma array com opções. """
    url = "https://api.telegram.org/" + os.environ['REBORNKEY'] + "/sendPhoto?"
    url += "chat_id=" + str(chat_id) + "&"
    url += "photo=" + photo_url + "&"

    if caption:
        url += "caption=" + caption + "&"
        url += "parse_mode=Markdown&"
    if reply_to_message_id:
        url += "reply_to_message_id=" + str(reply_to_message_id) + "&"

    response = requests.get(url)
    response = json.loads(response.content)

    return response


def send_video(chat_id, video_url, caption="", reply_to_message_id=0):
    """ reply_markup não é apenas ID, é uma array com opções. """
    url = "https://api.telegram.org/" + os.environ['REBORNKEY'] + "/sendVideo?"
    url += "chat_id=" + str(chat_id) + "&"
    url += "video=" + video_url + "&"

    if caption:
        url += "caption=" + caption + "&"
        url += "parse_mode=Markdown&"
    if reply_to_message_id:
        url += "reply_to_message_id=" + str(reply_to_message_id) + "&"

    response = requests.get(url)
    response = json.loads(response.content)

    return response


def send_document(chat_id, document_url, caption="", reply_to_message_id=0):
    """ reply_markup não é apenas ID, é uma array com opções. """
    url = "https://api.telegram.org/" + os.environ['REBORNKEY'] + "/sendDocument?"
    url += "chat_id=" + str(chat_id) + "&"
    url += "document=" + document_url + "&"

    if caption:
        url += "caption=" + caption + "&"
    if reply_to_message_id:
        url += "reply_to_message_id=" + str(reply_to_message_id) + "&"

    response = requests.get(url)
    response = json.loads(response.content)

    return response


def send_sticker(chat_id, sticker_id): 
    url = "https://api.telegram.org/" + os.environ['REBORNKEY'] + "/sendSticker?"
    url += "chat_id=" + str(chat_id) + "&"
    url += "sticker=" + sticker_id + "&"

    response = requests.get(url)
    response = json.loads(response.content)

    return response


def send_voice(chat_id, voice_id): 
    url = "https://api.telegram.org/" + os.environ['REBORNKEY'] + "/sendvoice?"
    url += "chat_id=" + str(chat_id) + "&"
    url += "voice=" + voice_id + "&"

    response = requests.get(url)
    response = json.loads(response.content)

    return response


def send_chat_action(chat_id, action):
    url = "https://api.telegram.org/" + os.environ['REBORNKEY'] + "/sendChatAction?"
    url += "chat_id=" + str(chat_id) + "&"
    url += "action=" + action + "&"

    response = requests.get(url)
    response = json.loads(response.content)

    return response


def send_media_group(chat_id, files, reply_to_message_id=0):
    url = "https://api.telegram.org/" + os.environ['REBORNKEY'] + "/sendMediaGroup?"
    url += "chat_id=" + str(chat_id) + "&"

    if reply_to_message_id:
        url += "reply_to_message_id=" + str(reply_to_message_id) + "&"

    files_request = {}
    media_arr = []

    for i in range(len(files)):
        media_arr.append({"type": "photo", "media": f"attach://media_{i}"})
        files_request[f"media_{i}"] = files[i]

    url += "media=" + json.dumps(media_arr) + "&"

    print(files_request)
    print(url)

    response = requests.get(url, files=files_request)

    if response.status_code != 200:
        return send_message(chat_id, "Erro ao enviar mensagem")
    else:
        response = json.loads(response.content)

        print(response)

        return response