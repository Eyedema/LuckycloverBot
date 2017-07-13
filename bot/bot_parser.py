# encoding=utf8
import sys
from datetime import datetime, timedelta
import calendar
import unicodedata

reload(sys)
sys.setdefaultencoding('utf8')

def build_string(suffix):
    suffix = suffix.upper()
    appendix = suffix.rsplit(None, 1)[-1]
    return appendix.split("'")[-1]

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])+"'"

def hours_alert(date):
    d1 = datetime.strptime(date, '%Y-%m-%d')
    d2 = d1 - timedelta(days=1)
    hours = (datetime.now().hour) - 7
    return abs((d2 - datetime.today()).days*24 - hours)

def get_schedule(dayN, nthDay):
    this_month_schedule = calendar.Calendar(dayN).monthdatescalendar(datetime.today().year, datetime.today().month)[nthDay][0]
    next_month_schedule = calendar.Calendar(dayN).monthdatescalendar(datetime.today().year, datetime.today().month+1)[nthDay][0]
    return str(this_month_schedule) if this_month_schedule > datetime.today().date() else str(next_month_schedule)

def parse_update(update):
    return update["message"]["text"], update["message"]["chat"]["id"], update["message"]["from"]["first_name"]
    #testo, id, nome

def write_broadcast(text):
    if text not in open("/home/Eyedema/luckycloverbot/broadcast").read():
        with open("/home/Eyedema/luckycloverbot/broadcast", "a") as myfile:
            myfile.write(text)

def add_to_broadcast(update):
    username = "---"
    try:
        username = update["message"]["from"]["username"]
    except Exception:
        pass
    text, chat_id, name = parse_update(update)
    message = ""
    if update["message"]["chat"]["type"] == 'private':
        message += "{} {} @{}\n".format(str(chat_id), name, username)
        write_broadcast(message)
    else:
        name = update["message"]["chat"]["title"]
        username = '---'
        message += "{} {} @{}\n".format(str(chat_id), name, username)
        write_broadcast(message)

def get_broadcast():
    message = ""
    with open("/home/Eyedema/luckycloverbot/broadcast", 'r') as myfile:
        message = myfile.read()
    if message:
        return message
    return "Broadcast list empty."

def write_log(update):
    username = "---"
    try:
        username = update["message"]["from"]["username"]
    except Exception:
        pass
    text, chat_id, name = bot_parser.parse_update(update)
    with open('/home/Eyedema/luckycloverbot/obj/botlog.log', 'a+') as file:
        file.write(':: {:%Y-%b-%d %H:%M:%S} {} @{} (ID:{}) searched for {}\n'.format(datetime.now(),name, username, str(chat_id), text)
    add_to_broadcast(update)