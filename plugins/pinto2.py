import base64
import requests
import threading
import api
import json
import random
from time import sleep

MAX_TRIES = 10


template = """<!DOCTYPE html>
<html lang="en">
<head>
</head>
<body>
    <section id="images">
    </section>

    <script>
        var result = JSON_GOES_HERE

        var images_section = document.getElementById("images");
        
        for (var i = 0; i < result.images.length; i++) {
            var image = result.images[i];
            var img = document.createElement("img");
            img.src = "data:image/png;base64," + image;

            images_section.appendChild(img);
        }
    </script>
</html>"""


def send_images(images, prompt, chat_id, message_id):
    files = []
    success = False

    file_name = f"{prompt.replace(' ', '_')}.html"

    with open(f"/var/www/html/pinto/{file_name}", "w") as f:
        f.write(template.replace("JSON_GOES_HERE", json.dumps(images)))

    while not success:
        text = f"taki tuas photo cursssadad ad poha ai divirtasse.. https://lberti.me/pinto/{file_name}"
        response = api.send_message(chat_id, text, reply_to_message_id=message_id)

        if response["ok"]:
            success = True
        else:
            timeout = response["parameters"]["retry_after"]
            sleep(timeout)


def get_images(prompt, chat_id, message_id, main_msg_message_id):
    url = "https://bf.dallemini.ai/generate"
    tries = 0
    success = False

    payload = {
        "prompt": prompt
    }

    payload = json.dumps(payload)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0',
        'Accept': 'application/json',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://hf.space/',
        'Content-Type': 'application/json',
        'Origin': 'https://hf.space',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-GPC': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache'
    }

    while not success and tries < MAX_TRIES:
        api.edit_message_text(chat_id, main_msg_message_id, f"comesano tntnetntineitnva {tries + 1},,,")

        response = requests.post(url, headers=headers, data=payload)

        if response.status_code == 200:
            success = True
            
            images = response.json()

            send_images(images, prompt, chat_id, message_id)
            return
        elif response.status_code == 503:
            print(response.text)

            api.edit_message_text(chat_id, main_msg_message_id, f"o poha tetativ {tries + 1} n rolo n.,,")

            tries += 1
            sleep(random.randint(1, 3))
        else:
            print(response.text)

            api.edit_message_text(chat_id, main_msg_message_id, f"vish deu merd...... eror cdigo {response.status_code} testo: {response.text}")
    
    api.edit_message_text(chat_id, main_msg_message_id, "affff safoda tneta dnv ai")


def decode_img(img):
    return base64.b64decode(img)


def on_msg_received(msg, matches):
    chat_id = msg["chat"]["id"]
    message_id = msg["message_id"]

    prompt = matches.group(1)
    main_msg_message_id = api.send_message(chat_id, f"vo tneta {MAX_TRIES} veses se n de serto fodase")["result"]["message_id"]

    thread = threading.Thread(name="dalleThread", target=get_images, args=(prompt, chat_id, message_id, main_msg_message_id,))
    thread.start()
