from api import send_message, send_photo
from plugins.img import getValidLink

def on_msg_received(msg, matches):
    try:
        chat = msg["chat"]["id"]
        query = matches.group(1)
        top_text = matches.group(2)
        bottom_text = matches.group(3)

        top_text = top_text.replace("?", "~q").replace("%", "~p").replace("#", "~h").replace("/", "~h").replace('"', "''").replace(" ", "_")
        bottom_text = bottom_text.replace("?", "~q").replace("%", "~p").replace("#", "~h").replace("/", "~h").replace('"', "''").replace(" ", "_")
        link = getValidLink(query)["link"]

        image_url = f"https://memegen.link/custom/{top_text}/{bottom_text}.jpg?alt={link}&font=impact"

        send_message(chat, "eh prahja 1 meminho saino do frno......")
        send_photo(chat, image_url)
    except Exception as e:
        print(f"vish: {e}")

        send_message(chat, "afff velho deu problemmam aqui......")