import api

def on_msg_received(msg, matches):
    api.send_message("14160874", msg["from"]["first_name"] + " disse: " + matches.group(1))
    api.send_message("-11672208", matches.group(1))
