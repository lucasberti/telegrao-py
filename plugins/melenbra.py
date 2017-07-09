import json
import time
import sched

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

    days    = matches.group(1)
    hours   = matches.group(2)
    minutes = matches.group(3)
    seconds = matches.group(4)

    message = matches.group(5)

    timeoffset = 0

    if days is not None:
        days = days.replace("d", "")
        timeoffset += 86400 * int(days)

    if hours is not None:
        hours = hours.replace("h", "")
        timeoffset += 3600 * int(hours)

    if minutes is not None:
        minutes = minutes.replace("m", "")
        timeoffset += 60 * int(minutes)

    if seconds is not None:
        seconds = seconds.replace("s", "")
        timeoffset += int(seconds)

    if days is None and hours is None and minutes is None and seconds is None and message is None:
        response = list_reminders(chat)
        send_message(chat, response)
        return


    futuretime = time.time() + timeoffset

    if "username" in msg["from"]:
        message += " blz @" + msg["from"]["username"]

    add_reminder(chat, futuretime, message)

    futuretime = time.localtime(futuretime)

    response = "belesinhaaaaa vo lenbra dia " + time.strftime("%d/%m/%y as %H:%M:%S", futuretime) + " sobr \"" + message + "\""
    send_message(chat, response)


def run():
    scheduler.enter(1, 1, check_time)
    scheduler.run()

