import json
import time
import sched
import dateparser
import datetime

from api import send_message

scheduler = sched.scheduler(time.time, time.sleep)


def load_reminders():
    reminders = {}

    try:
        with open("data/reminders.json") as fp:
            reminders = json.load(fp)
    except Exception:
        with open("data/reminders.json", "w") as fp:
            json.dump(reminders, fp, indent=4)

    return reminders


def save_reminders(reminders):
    with open("data/reminders.json", "w") as fp:
        json.dump(reminders, fp, indent=4)


def list_reminders(chat):
    chat = str(chat)
    reminders = load_reminders()
    msg = ""

    reminders = reminders[chat]

    for reminder in reminders:
        futuretime = time.localtime(float(reminder))
        msg += time.strftime("%d/%m/%y as %H:%M:%S", futuretime) + ": " + reminders[reminder] + "\n"

    return msg



def add_reminder(chat, date, message):
    chat = str(chat)
    reminders = load_reminders()

    assert type(reminders) is dict

    if chat not in reminders:
        reminders[chat] = {}

    reminders[chat][date] = message

    save_reminders(reminders)


def check_time():
    reminders = load_reminders()

    for chat in reminders:
        for date in reminders[chat]:
            if float(date) < time.time():
                send_message(chat, "O  MEU JA DEU ORA D " + reminders[chat][date])
                # print(reminders[chat][date])
                reminders[chat].pop(date)

                save_reminders(reminders)

                break

    scheduler.enter(1, 1, check_time)


def on_msg_received(msg, matches):
    chat = msg["chat"]["id"]

    futuretime = matches.group(1)
    message = matches.group(2)

    print("future", futuretime, "message", message)

    timeoffset = 0
    if futuretime is None and "list" in message:
        response = list_reminders(chat)
        send_message(chat, response)
        return

    if message is not None and futuretime is None:
        send_message(chat, "o vei n tendi n ve teuformato ai....")
        return

    future = dateparser.parse(futuretime, settings={'PREFER_DATES_FROM': 'future'})

    if future is not None and future < datetime.datetime.now():
        future = dateparser.parse("em " + futuretime)

    if future is None:
        send_message(chat, "o vehlilo netendi esa dat ai ~~~n......")
        return

    if "username" in msg["from"]:
        message += " blz @" + msg["from"]["username"]

    add_reminder(chat, future.timestamp(), message)

    futuretime = time.localtime(future.timestamp())

    response = "belesinhaaaaa vo lenbra dia " + time.strftime("%d/%m/%y as %H:%M:%S", futuretime) + " sobr \"" + message + "\""
    send_message(chat, response)


def run():
    scheduler.enter(1, 1, check_time)
    scheduler.run()

