import logging
from tg_types.message import Message

def on_msg_received(msg: Message, matches):
    logging.info(f"on_msg_received: {msg}")

    if msg._from.username == "Berti":
        msg.reply("Hello, %s!" % msg._from.first_name)