from api import send_message
from datetime import datetime
from reborn import is_sudoer

def on_msg_received(msg, matches):
    chat = msg["chat"]["id"]

    if matches.group(1) and is_sudoer(msg["from"]["id"]):
        if matches.group(1) == "reset":
            with open("data/treta_history.txt", "w") as f:
                f.write(str(datetime.now().timestamp())[:10])

                send_message(chat, "pora mas q desepcsao ja teve treta de novo")
    
    else:
        with open("data/treta_history.txt") as f:
            last_treta = int(f.readline())

        last_treta = datetime.fromtimestamp(last_treta)
        delta = datetime.now() - last_treta

        last_treta = last_treta.strftime("%d/%m/%y as %H:%M:%S")

        response = f"meus aparabes vocs jae stao 100 trta dsd {last_treta}, iso da.......  {delta.days} dias!!!"

        send_message(chat, response)